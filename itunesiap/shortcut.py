
from . import environment

def verify(*args, **kwargs):
    return environment.default.verify(*args, **kwargs)
