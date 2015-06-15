
from . import request
from . import option

class Environment(object):
    """Environement provides option preset for `Request`. `default` is default"""

    def __init__(self, **kwargs):
        self.use_production = True
        self.use_sandbox = False

        option.override(self, **kwargs)

    def Request(self, receipt_data, password=None, **kwargs):
        return request.Request(receipt_data, password=password, env=self, **kwargs)

    def verify(self, receipt_data, password=None, **kwargs):
        request = self.Request(receipt_data, password=password, **kwargs)
        return request.verify()


default = Environment(use_production=True, use_sandbox=False)
production = Environment(use_production=True, use_sandbox=False)
sandbox = Environment(use_production=False, use_sandbox=True)
review = Environment(use_production=False, use_sandbox=True)
