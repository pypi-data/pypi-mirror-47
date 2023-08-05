import copy
import logging
import os
from functools import cmp_to_key

import requests
from cryptojwt import jwe
from cryptojwt.jws.jws import SIGNER_ALGS
from cryptojwt.key_jar import KeyJar
from cryptojwt.key_jar import init_key_jar
from jinja2 import Environment
from jinja2 import FileSystemLoader
from oidcmsg.oidc import IdToken
from oidcmsg.oidc import SCOPE2CLAIMS

from oidcendpoint import authz
from oidcendpoint import rndstr
from oidcendpoint import util
from oidcendpoint.client_authn import CLIENT_AUTHN_METHOD
from oidcendpoint.exception import ConfigurationError
from oidcendpoint.id_token import IDToken
from oidcendpoint.session import create_session_db
from oidcendpoint.sso_db import SSODb
from oidcendpoint.template_handler import Jinja2TemplateHandler
from oidcendpoint.user_authn.authn_context import populate_authn_broker
from oidcendpoint.util import build_endpoints

logger = logging.getLogger(__name__)

CAPABILITIES = {
    "response_types_supported": [
        "code", "token", "id_token", "code token", "code id_token",
        "id_token token", "code id_token token", 'none'],
    "token_endpoint_auth_methods_supported": [
        "client_secret_post", "client_secret_basic",
        "client_secret_jwt", "private_key_jwt"],
    "response_modes_supported": ['query', 'fragment', 'form_post'],
    "subject_types_supported": ["public", "pairwise"],
    "grant_types_supported": [
        "authorization_code", "implicit",
        "urn:ietf:params:oauth:grant-type:jwt-bearer", "refresh_token"],
    "claim_types_supported": ["normal", "aggregated", "distributed"],
    "claims_parameter_supported": True,
    "request_parameter_supported": True,
    "request_uri_parameter_supported": True
}

SORT_ORDER = {'RS': 0, 'ES': 1, 'HS': 2, 'PS': 3, 'no': 4}


def sort_sign_alg(alg1, alg2):
    if SORT_ORDER[alg1[0:2]] < SORT_ORDER[alg2[0:2]]:
        return -1
    elif SORT_ORDER[alg1[0:2]] > SORT_ORDER[alg2[0:2]]:
        return 1
    else:
        if alg1 < alg2:
            return -1
        elif alg1 > alg2:
            return 1
        else:
            return 0


def add_path(url, path):
    if url.endswith('/'):
        if path.startswith('/'):
            return '{}{}'.format(url, path[1:])
        else:
            return '{}{}'.format(url, path)
    else:
        if path.startswith('/'):
            return '{}{}'.format(url, path)
        else:
            return '{}/{}'.format(url, path)


def init_user_info(conf, cwd):
    try:
        kwargs = conf['kwargs']
    except KeyError:
        kwargs = {}

    if 'db_file' in kwargs:
        kwargs['db_file'] = os.path.join(cwd, kwargs['db_file'])

    if isinstance(conf['class'], str):
        return util.importer(conf['class'])(**kwargs)
    else:
        return conf['class'](**kwargs)


def init_service(conf, endpoint_context=None):
    try:
        kwargs = conf['kwargs']
    except KeyError:
        kwargs = {}

    if endpoint_context:
        kwargs['endpoint_context'] = endpoint_context

    if isinstance(conf['class'], str):
        return util.importer(conf['class'])(**kwargs)
    else:
        return conf['class'](**kwargs)


class EndpointContext(object):
    def __init__(self, conf, keyjar=None, client_db=None, session_db=None,
                 cwd='', cookie_dealer=None, httpc=None, cookie_name=None,
                 jwks_uri_path=None):
        self.conf = conf
        self.keyjar = keyjar or KeyJar()
        self.cwd = cwd

        # client database
        self.cdb = client_db or {}

        try:
            self.seed = bytes(conf['seed'], 'utf-8')
        except KeyError:
            self.seed = bytes(rndstr(16), 'utf-8')

        # Default values, to be changed below depending on configuration
        self.endpoint = {}
        self.issuer = ''
        self.httpc = httpc or requests
        self.verify_ssl = True
        self.jwks_uri = None
        self.sso_ttl = 14400  # 4h
        self.symkey = rndstr(24)
        self.id_token_schema = IdToken
        self.endpoint_to_authn_method = {}
        self.cookie_dealer = cookie_dealer
        self.login_hint_lookup = None

        if cookie_name:
            self.cookie_name = cookie_name
        elif 'cookie_name' in conf:
            self.cookie_name = conf['cookie_name']
        else:
            self.cookie_name = {
                'session': "oidcop", 'register': 'oidc_op_rp',
                'session_management': "sman"
            }

        for param in ['verify_ssl', 'issuer', 'sso_ttl',
                      'symkey', 'client_authn', 'id_token_schema']:
            try:
                setattr(self, param, conf[param])
            except KeyError:
                pass

        try:
            self.template_handler = conf['template_handler']
        except KeyError:
            try:
                loader = conf['template_loader']
            except KeyError:
                template_dir = conf["template_dir"]
                loader = Environment(loader=FileSystemLoader(template_dir))
            self.template_handler = Jinja2TemplateHandler(loader)

        self.setup = {}
        if not jwks_uri_path:
            try:
                jwks_uri_path = conf['jwks']['uri_path']
            except KeyError:
                pass

        try:
            if self.issuer.endswith('/'):
                self.jwks_uri = '{}{}'.format(self.issuer, jwks_uri_path)
            else:
                self.jwks_uri = '{}/{}'.format(self.issuer, jwks_uri_path)
        except KeyError:
            self.jwks_uri = ''

        if self.keyjar is None or self.keyjar.owners() == []:
            args = {k: v for k, v in conf['jwks'].items() if k != 'uri_path'}
            self.keyjar = init_key_jar(**args)

        try:
            _conf = conf['cookie_dealer']
        except KeyError:
            pass
        else:
            if self.cookie_dealer:  # already defined
                raise ValueError('Cookie Dealer already defined')
            self.cookie_dealer = init_service(_conf)

        try:
            _conf = conf['sub_func']
        except KeyError:
            sub_func = None
        else:
            sub_func = {}
            for key, args in _conf.items():
                if 'class' in args:
                    sub_func[key] = init_service(args)
                elif 'function' in args:
                    if isinstance(args['function'], str):
                        sub_func[key] = util.importer(args['function'])
                    else:
                        sub_func[key] = args['function']

        if session_db:
            self.sdb = session_db
        else:
            try:
                _th_args = conf['token_handler_args']
            except KeyError:
                # create 3 keys
                keydef = [
                    {"type": "oct", "bytes": "24", 'use': ['enc'], 'kid': 'code'},
                    {"type": "oct", "bytes": "24", 'use': ['enc'], 'kid': 'token'},
                    {"type": "oct", "bytes": "24", 'use': ['enc'], 'kid': 'refresh'}
                ]

                jwks_def = {
                    'private_path': 'private/token_jwks.json',
                    'key_defs': keydef, 'read_only': False
                }

                _th_args = {'jwks_def': jwks_def}
                for typ, tid in [('code', 600), ('token', 3600), ('refresh', 86400)]:
                    _th_args[typ] = {'lifetime': tid}

            self.sdb = create_session_db(self, _th_args, db=None,
                                         sso_db=SSODb(), sub_func=sub_func)

        self.endpoint = build_endpoints(conf['endpoint'],
                                        endpoint_context=self,
                                        client_authn_method=CLIENT_AUTHN_METHOD,
                                        issuer=conf['issuer'])
        try:
            _cap = conf['capabilities']
        except KeyError:
            _cap = {}

        for endpoint, endpoint_instance in self.endpoint.items():
            if endpoint_instance.provider_info:
                _cap.update(endpoint_instance.provider_info)

            if endpoint in ['webfinger', 'provider_info']:
                continue

            _cap[endpoint_instance.endpoint_name] = '{}'.format(
                endpoint_instance.endpoint_path)

        try:
            authz_spec = conf['authz']
        except KeyError:
            self.authz = authz.Implicit(self)
        else:
            self.authz = init_service(authz_spec, self)

        try:
            _authn = conf['authentication']
        except KeyError:
            self.authn_broker = None
        else:
            self.authn_broker = populate_authn_broker(_authn, self,
                                                      self.template_handler)

        try:
            _conf = conf['id_token']
        except KeyError:
            self.idtoken = IDToken(self)
        else:
            self.idtoken = init_service(_conf, self)

        try:
            _conf = conf['userinfo']
        except KeyError:
            pass
        else:
            self.userinfo = init_user_info(_conf, self.cwd)
            self.sdb.userinfo = self.userinfo

        try:
            _conf = conf['login_hint_lookup']
        except KeyError:
            pass
        else:
            self.login_hint_lookup = init_service(_conf)
            if self.userinfo:
                self.login_hint_lookup.user_info = self.userinfo

        try:
            _conf = conf['login_hint2acrs']
        except KeyError:
            self.login_hint2acrs = None
        else:
            self.login_hint2acrs = init_service(_conf)

        self.provider_info = self.create_providerinfo(_cap)

        # which signing/encryption algorithms to use in what context
        self.jwx_def = {}

        # special type of logging
        self.events = None

    def package_capabilities(self):
        _provider_info = copy.deepcopy(CAPABILITIES)
        _provider_info["issuer"] = self.issuer
        _provider_info["version"] = "3.0"

        _claims = []
        for _cl in SCOPE2CLAIMS.values():
            _claims.extend(_cl)
        _provider_info["claims_supported"] = list(set(_claims))

        _scopes = list(SCOPE2CLAIMS.keys())
        _provider_info["scopes_supported"] = _scopes

        # Sort order RS, ES, HS, PS
        sign_algs = list(SIGNER_ALGS.keys())
        sign_algs = sorted(sign_algs, key=cmp_to_key(sort_sign_alg))

        for typ in ["userinfo", "id_token", "request_object"]:
            _provider_info["%s_signing_alg_values_supported" % typ] = sign_algs

        # Remove 'none' for token_endpoint_auth_signing_alg_values_supported
        # since it is not allowed
        sign_algs = sign_algs[:]
        sign_algs.remove('none')
        _provider_info[
            "token_endpoint_auth_signing_alg_values_supported"] = sign_algs

        algs = jwe.SUPPORTED["alg"]
        for typ in ["userinfo", "id_token", "request_object"]:
            _provider_info["%s_encryption_alg_values_supported" % typ] = algs

        encs = jwe.SUPPORTED["enc"]
        for typ in ["userinfo", "id_token", "request_object"]:
            _provider_info["%s_encryption_enc_values_supported" % typ] = encs

        # acr_values
        if self.authn_broker:
            acr_values = self.authn_broker.get_acr_value_string()
            if acr_values is not None:
                _provider_info["acr_values_supported"] = acr_values

        return _provider_info

    def create_providerinfo(self, capabilities):
        """
        Dynamically create the provider info response

        :param capabilities:
        :return:
        """

        _pinfo = self.package_capabilities()
        not_supported = {}
        for key, val in capabilities.items():
            try:
                allowed = _pinfo[key]
            except KeyError:
                _pinfo[key] = val
            else:
                if isinstance(allowed, bool):
                    if allowed is False:
                        if val is True:
                            not_supported[key] = True
                    else:
                        _pinfo[key] = val
                elif isinstance(allowed, str):
                    if val != allowed:
                        not_supported[key] = val
                elif isinstance(allowed, list):
                    if isinstance(val, str):
                        sv = {val}
                    else:
                        try:
                            sv = set(val)
                        except TypeError:
                            if key == 'response_types_supported':
                                sv = set()
                                for v in val:
                                    v.sort()
                                    sv.add(' '.join(v))
                            else:
                                raise
                        else:
                            sv = set()
                            for v in val:
                                vs = v.split(' ')
                                vs.sort()
                                sv.add(' '.join(vs))

                    sa = set(allowed)

                    if (sv & sa) == sv:
                        _pinfo[key] = list(sv)
                    else:
                        not_supported[key] = list(sv - sa)

        if not_supported:
            _msg = "Server doesn't support the following features: {}".format(
                not_supported)
            logger.error(_msg)
            raise ConfigurationError(_msg)

        if self.jwks_uri and self.keyjar:
            _pinfo["jwks_uri"] = self.jwks_uri

        for name, instance in self.endpoint.items():
            if name not in ['webfinger', 'provider_info']:
                _pinfo[instance.endpoint_name] = instance.full_path

        return _pinfo
