
import contextlib
import json

import requests

from . import receipt, option
from .tools import lazy_property, deprecated
from six import u
from . import exceptions


RECEIPT_PRODUCTION_VALIDATION_URL = "https://buy.itunes.apple.com/verifyReceipt"
RECEIPT_SANDBOX_VALIDATION_URL = "https://sandbox.itunes.apple.com/verifyReceipt"


class Request(object):
    """Validation request with raw receipt. Receipt must be base64 encoded string.
    Use `verify` method to try verification and get Receipt or exception.
    """
    def __init__(self, receipt_data, password=None, env=None, **kwargs):
        self.receipt_data = receipt_data
        self.password = password

        if env is None:
            from . import environment
            env = environment.default
        option.copy(self, env)
        option.override(self, **kwargs)


    def __repr__(self):
        return u'<Request({1}...)>'.format(self.receipt_data[:20])

    @property
    def request_content(self):
        if self.password is not None:
            request_content = {'receipt-data': self.receipt_data, 'password': self.password}
        else:
            request_content = {'receipt-data': self.receipt_data}
        return request_content

    def verify_from(self, url):
        """Try verification from given url."""
        # If the password exists from kwargs, pass it up with the request, otherwise leave it alone
        http_response = requests.post(url, json.dumps(self.request_content), verify=False)
        if http_response.status_code != 200:
            raise exceptions.ItunesServerNotAvailable(http_response.status_code, http_response.content)

        response = receipt.Response(json.loads(http_response.content.decode('utf-8')))
        if response.status != 0:
            raise exceptions.InvalidReceipt(response.status, response=response)
        return response

    def verify(self):
        """Try verification with settings. Returns a `Receipt` object if succeed.
        Otherwise raise an exception.
        """
        response = None
        assert (self.use_production or self.use_sandbox)

        e = None
        if self.use_production:
            try:
                response = self.verify_from(RECEIPT_PRODUCTION_VALIDATION_URL)
            except exceptions.InvalidReceipt as ee:
                e = ee

        if not response and self.use_sandbox:
            try:
                response = self.verify_from(RECEIPT_SANDBOX_VALIDATION_URL)
            except exceptions.InvalidReceipt as ee:
                if not self.use_production:
                    e = ee

        if not response:
            raise e  # raise production error if possible

        return response

    @contextlib.contextmanager
    def options(self, env=None, **kwargs):
        previous_options = option.extract(self)
        if env:
            option.copy(self, env)
        option.override(self, **kwargs)
        yield
        option.override(self, **previous_options)
