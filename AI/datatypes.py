datatypes = {}


def getobjectmodulename(o) -> (str, str):
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.
    module = o.__class__.__module__
    if module is None:
        raise Exception("Unknown module")
    return (module, o.__class__.__name__)


UnknownType = type('UnknownType', (object,), dict())
setattr(UnknownType, "__str__", lambda self: "UnknownType")
Self = type('Self', (object,), dict())
setattr(Self, "__str__", lambda self: "self")


class Data(type):
    inherent_type: type = None
    value: object = None

    def __init__(self, o: object):
        super().__init__(o)
        self.inherent_type = type(o)
        self.value = o

    def gettype(self):
        return self.inherent_type

    def getvalue(self):
        return self.value


def register_type(name: type) -> None:
    if name in datatypes.keys():
        raise Exception("Already exists")
    datatypes[name] = [method_name for method_name in dir(name) if
                       callable(getattr(name, method_name))]


def get_type_attributes(name: str):
    return datatypes.get(name)


def get_types_names():
    return datatypes.keys()


def get_all_types():
    return dict(datatypes)
