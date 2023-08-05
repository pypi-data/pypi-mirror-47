import logging
from typing import List

from bottle import request, response

log = logging.getLogger(__name__)


def enable_cors(callback):
    callback.enable_cors = True
    return callback


class CorsPlugin(object):
    name = 'cors'
    api = 2

    def __init__(self, origins: List[str] = None, headers: List[str] = None, credentials: bool = False):
        self.allow_credentials = credentials
        self.allowed_headers = headers
        self.allowed_origins = origins
        self.cors_url_rules = {}

    def setup(self, app):
        if not app.routes:
            raise Exception('No routes found. Please be sure to install CorsPlugin after declaring *all* your routes!')

        for route in app.routes:
            if not self._is_cors_enabled(route.callback):
                continue
            if route.rule not in self.cors_url_rules:
                self.cors_url_rules[route.rule] = set()
            self.cors_url_rules[route.rule].add(str(route.method).upper())
        if not self.cors_url_rules:
            return  # no CORS-enabled routes defined

        @enable_cors
        def generic_cors_route():
            return None

        for rule, methods in self.cors_url_rules.items():
            if 'OPTIONS' not in methods:
                log.info('Adding OPTIONS route for %s' % rule)
                methods.add('OPTIONS')
                app.route(rule, 'OPTIONS', generic_cors_route, skip=['api_auth'])

    def apply(self, callback, context):
        if not self._is_cors_enabled(callback):
            return callback  # do not even touch

        print('should enable cors <3')

        def wrapper(*args, **kwargs):
            origin = request.get_header('origin')
            headers = ','.join(self.allowed_headers) if self.allowed_headers else '*'
            methods = ','.join(self.cors_url_rules.get(context.rule, [context.method, 'OPTIONS']))
            response.add_header('Access-Control-Allow-Origin', origin)
            response.add_header('Access-Control-Allow-Headers', headers)
            response.add_header('Access-Control-Allow-Methods', methods)
            response.add_header('Access-Control-Allow-Credentials', str(self.allow_credentials).lower())
            return callback(*args, **kwargs)

        return wrapper

    @staticmethod
    def _is_cors_enabled(callback):
        return hasattr(callback, 'enable_cors') and callback.enable_cors
