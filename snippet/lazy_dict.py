def get_structure(lazy_object):
    """Get lazy_object's structure by recursively getting attributes' key without evaluating their real value
    Args:
        lazy_object: object to inspect
    Returns:
        dict
    """
    structure = {}
    for key in dir(lazy_object):
        if not key.startswith('_'):
            if lazy_object._is_subset(key):
                structure[key] = get_structure(getattr(lazy_object, key))
            else:
                structure[key] = None
    return structure


def to_dict(lazy_object):
    """Convert lazy_object to a dictionary by recursively expanding.
    Sub-level child will still remain untouched.
    Args:
        lazy_object: object to convert
    Returns:
        dict
    """
    result = {}
    for key in dir(lazy_object):
        if not key.startswith('_'):
            if lazy_object._is_subset(key):
                result[key] = to_dict(getattr(lazy_object, key))
            else:
                result[key] = getattr(lazy_object, key)
    return result


class lazy_property(object):
    """decorator for lazy evaluation of an object attribute.
    property should represent non-mutable data, as it replaces itself.
    """

    def __init__(self, fget):
        self.fget = fget
        self.func_name = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return None
        value = self.fget(obj)
        setattr(obj, self.func_name, value)
        return value


class LazyDict(object):
    """Base class for lazy dictionary.
    Customize dictionary should extend this class and define its own property
    See test_lazy_dict for example
    """
    def __init__(self):
        self.__subset__ = set()

    def _is_subset(self, key):
        return key in self.__subset__

    def _get_structure(self):
        return get_structure(self)

    def _keys(self):
        keys = set()
        for key in dir(self):
            if not key.startswith('_'):
                keys.add(key)
        return keys

    def _to_dict(self):
        return to_dict(self)

    def __getitem__(self, index):
        try:
            value = getattr(self, index)
        except:
            value = None
        return value

    def __setitem__(self, index, value):
        setattr(self, index, value)