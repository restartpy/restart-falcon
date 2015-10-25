from __future__ import absolute_import

import types

from six import iteritems
from restart.adapter import Adapter
from falcon import API as FalconAPI

from .request import FalconRequest


class FalconResource(object):
    pass


class FalconAdapter(Adapter):

    def __init__(self, *args, **kwargs):
        super(FalconAdapter, self).__init__(*args, **kwargs)
        self.falcon_api = FalconAPI()
        # Add Falcon-specific URI routes
        for uri, resource in self.get_embedded_rules():
            self.falcon_api.add_route(uri, resource)

    def adapt_handler(self, handler, resource, request,
                      response, *args, **kwargs):
        """Adapt the request object and the response object for
        the `handler` function.

        :param handler: the handler function to be adapted.
        :param resource: the Falcon resource object.
        :param request: the Falcon request object.
        :param response: the Falcon response object.
        :param args: a list of positional arguments that will be passed
                     to the handler.
        :param kwargs: a dictionary of keyword arguments that will be passed
                       to the handler.
        """
        adapted_request = FalconRequest(request)
        api_response = handler(adapted_request, *args, **kwargs)

        # Convert the RESTArt response object to a Falcon response object
        response.body = api_response.data
        response.status = api_response.status
        response.set_headers(api_response.headers)

    def wsgi_app(self, environ, start_response):
        """The actual Falcon-specific WSGI application.

        See :meth:`~restart.seving.Service.wsgi_app` for the
        meanings of the parameters.
        """
        return self.falcon_api(environ, start_response)

    def get_embedded_rules(self):
        """Get the Falcon-specific rules used to be embedded into
        an existing or legacy application.

        Usage:

            # The existing Falcon API
            import falcon
            app = falcon.API()
            ...

            # The RESTArt API
            from restart.api import RESTArt
            api = RESTArt()
            ...

            # Embed RESTArt into Falcon
            from restart.serving import Service
            from restart.ext.falcon.adapter import FalconAdapter
            service = Service(api, FalconAdapter)
            for uri, resource in service.embedded_rules:
                app.add_route(ui, resource)
        """
        rules = []
        for endpoint, rule in iteritems(self.adapted_rules):
            resource = FalconResource()
            for method in rule.methods:
                on_method = types.MethodType(rule.handler, resource)
                setattr(resource, 'on_' + method.lower(), on_method)
            # Convert URI style from RESTArt's `<arg>` to Falcon's `{arg}`
            uri = rule.uri.replace('<', '{').replace('>', '}')
            assert ':' not in uri, (
                'Werkzeug-style converters (with the separator ":") is '
                'not supported in `RESTArt-Falcon`. Captured parameters '
                'in URI can only be specified in the form of "<arg>"'
            )
            rules.append((uri, resource))
        return tuple(rules)
