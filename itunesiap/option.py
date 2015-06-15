
OPTION_ITEMS = ['use_production', 'use_sandbox']


def override(self, **kwargs):
    """Override options in kwargs to given object `self`."""
    for item in OPTION_ITEMS:
        if item in kwargs:
            setattr(self, item, kwargs[item])


def extract(self):
    """Extract options from `self` and merge to `kwargs` and return new object."""
    options = {}
    for item in OPTION_ITEMS:
        options[item] = getattr(self, item)
    return options


def copy(self, env):
    """Copy options from `env` to `self`."""
    for item in OPTION_ITEMS:
        value = getattr(env, item)
        setattr(self, item, value)
