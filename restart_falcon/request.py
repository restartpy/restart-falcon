from __future__ import absolute_import

from restart.request import Request


class FalconRequest(Request):
    """The Falcon-specific request class."""

    def get_stream(self):
        """Get the request stream from the Falcon-specific
        request object.
        """
        return self.initial_request.stream

    def get_method(self):
        """Get the request method from the Falcon-specific
        request object.
        """
        return self.initial_request.method

    def get_uri(self):
        """Get the request URI from the Falcon-specific
        request object.
        """
        return self.initial_request.url

    def get_path(self):
        """Get the request path from the Falcon-specific
        request object.
        """
        return self.initial_request.path

    def get_args(self):
        """Get the request URI parameters from the Falcon-specific
        request object.
        """
        return self.initial_request.params

    def get_auth(self):
        """Get the request authorization data from the Falcon-specific
        request object.
        """
        return self.initial_request.auth

    def get_scheme(self):
        """Get the request scheme from the Falcon-specific
        request object.
        """
        return self.initial_request.protocol

    def get_headers(self):
        """Get the request headers from the Falcon-specific
        request object.
        """
        return dict(self.initial_request.headers)

    def get_environ(self):
        """Get the WSGI environment from the Falcon-specific
        request object.
        """
        return self.initial_request.env
