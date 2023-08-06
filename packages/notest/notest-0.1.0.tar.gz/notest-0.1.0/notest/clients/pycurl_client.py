import pycurl
import os
import sys
import copy
from io import BytesIO
from .http_auth_type import HttpAuthType
from .http_response import HttpResponse


base_dir = os.path.abspath(os.path.dirname(__file__))
libcurl_crt_file = os.path.join(base_dir, "..", "..", "tools", "curl-ca-bundle.crt")


DEFAULT_TIMEOUT = 10  # Seconds
# Map HTTP method names to curl methods
# Kind of obnoxious that it works this way...
HTTP_METHODS = {'GET': pycurl.HTTPGET,
                'PUT': pycurl.UPLOAD,
                'PATCH': pycurl.POSTFIELDS,
                'POST': pycurl.POST,
                'HEAD': "",
                'DELETE': 'DELETE'}


HttpAuthType_Map = {
    HttpAuthType.HTTP_AUTH_BASIC: pycurl.HTTPAUTH_BASIC
}


class PyCurlClient:
    def __init__(self, handler=None):
        if not handler or not isinstance(handler, pycurl.Curl):
            self.handler = pycurl.Curl()
        else:
            self.handler = handler
        self.response = None

    def get_handler(self):
        return self.handler

    @staticmethod
    def close_handler(handler):
        if handler:
            handler.close()

    def close(self):
        if self.handler:
            self.handler.close()

    def send_request(self, test_obj, timeout=DEFAULT_TIMEOUT, context=None,
                     handler=None, ssl_insecure=True, verbose=False):
        """ Create and mostly configure a curl object for test, reusing existing if possible """

        if handler:
            curl = handler

            try:  # Check the curl handle isn't closed, and reuse it if possible
                curl.getinfo(curl.HTTP_CODE)
                # Below clears the cookies & curl options for clean run
                # But retains the DNS cache and connection pool
                curl.reset()
                curl.setopt(curl.COOKIELIST, "ALL")
            except pycurl.error:
                curl = pycurl.Curl()

        else:
            curl = self.handler

        curl.setopt(curl.URL, str(test_obj.url))
        curl.setopt(curl.TIMEOUT, timeout)

        is_unicoded = False
        _body = test_obj.body
        if isinstance(_body, str):  # Encode unicode
            _body = _body.encode('UTF-8')
            is_unicoded = True

        # Set read function for post/put bodies
        if _body and len(_body) > 0:
            curl.setopt(curl.READFUNCTION, BytesIO(_body).read)

        if test_obj.auth_username and test_obj.auth_password:
            auth_username = test_obj.auth_username
            auth_password = test_obj.auth_password
            if isinstance(auth_username, str):
                auth_username = auth_username.encode()
            if isinstance(auth_password, str):
                auth_password = auth_password.encode()
            curl.setopt(pycurl.USERPWD, auth_username + b':' + auth_password)
            if test_obj.auth_type:
                auth_type = HttpAuthType_Map[test_obj.auth_type]
                curl.setopt(pycurl.HTTPAUTH, auth_type)

        if test_obj.method == u'POST':
            curl.setopt(pycurl.POST, 1)
            # Required for some servers
            if _body is not None:
                curl.setopt(pycurl.POSTFIELDSIZE, len(_body))
            else:
                curl.setopt(pycurl.POSTFIELDSIZE, 0)
        elif test_obj.method == u'PUT':
            curl.setopt(pycurl.UPLOAD, 1)
            # Required for some servers
            if _body is not None:
                curl.setopt(pycurl.INFILESIZE, len(_body))
            else:
                curl.setopt(pycurl.INFILESIZE, 0)
        elif test_obj.method == u'PATCH':
            curl.setopt(curl.POSTFIELDS, _body)
            curl.setopt(curl.CUSTOMREQUEST, 'PATCH')
            # Required for some servers
            # I wonder: how compatible will this be?  It worked with Django but feels iffy.
            if _body is not None:
                curl.setopt(pycurl.INFILESIZE, len(_body))
            else:
                curl.setopt(pycurl.INFILESIZE, 0)
        elif test_obj.method == u'DELETE':
            curl.setopt(curl.CUSTOMREQUEST, 'DELETE')
            if _body is not None:
                curl.setopt(pycurl.POSTFIELDS, _body)
                curl.setopt(pycurl.POSTFIELDSIZE, len(_body))
        elif test_obj.method == u'HEAD':
            curl.setopt(curl.NOBODY, 1)
            curl.setopt(curl.CUSTOMREQUEST, 'HEAD')
        elif test_obj.method and test_obj.method.upper() != 'GET':  # Alternate HTTP methods
            curl.setopt(curl.CUSTOMREQUEST, test_obj.method.upper())
            if _body is not None:
                curl.setopt(pycurl.POSTFIELDS, _body)
                curl.setopt(pycurl.POSTFIELDSIZE, len(_body))

        # Template headers as needed and convert headers dictionary to list of header entries
        head = test_obj.get_headers(context=context)
        head = copy.copy(head)  # We're going to mutate it, need to copy

        # Set charset if doing unicode conversion and not set explicitly
        # TESTME
        if is_unicoded and u'content-type' in head.keys():
            content = head[u'content-type']
            if u'charset' not in content:
                head[u'content-type'] = content + u' ; charset=UTF-8'

        if head:
            headers = [str(headername) + ':' + str(headervalue)
                       for headername, headervalue in head.items()]
        else:
            headers = list()
        # Fix for expecting 100-continue from server, which not all servers
        # will send!
        headers.append("Expect:")
        headers.append("Connection: close")
        curl.setopt(curl.HTTPHEADER, headers)

        # reset the body, it holds values from previous runs otherwise
        headers = BytesIO()
        body = BytesIO()
        if sys.platform.find("win") > -1:
            curl.setopt(pycurl.CAINFO, libcurl_crt_file)
        curl.setopt(pycurl.WRITEFUNCTION, body.write)
        curl.setopt(pycurl.HEADERFUNCTION, headers.write)
        if verbose:
            curl.setopt(pycurl.VERBOSE, True)
        if ssl_insecure is True:
            curl.setopt(pycurl.SSL_VERIFYPEER, 0)
            curl.setopt(pycurl.SSL_VERIFYHOST, 0)

        curl.perform()  # Run the actual call

        response_body = body.getvalue()
        body.close()
        response_headers = headers.getvalue()
        headers.close()
        response_code = curl.getinfo(pycurl.RESPONSE_CODE)
        response = HttpResponse(
            body=response_body,
            headers=response_headers,
            status_code=response_code
        )
        self.response = response

        return response

