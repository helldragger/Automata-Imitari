from typing import Collection, Iterable, Sized


class Structure(type, Collection):
    content_type: type = None

    def __init__(self, o: object):
        super().__init__(o)
        assert isinstance(o, Sized)
        assert isinstance(o, Iterable)
        self.content_type = type(o)


# abstract structures datatypes
structures: {type} = {}


def register_structure(struct: type) -> None:
    if struct in structures.keys():
        raise Exception("Already exists")
    structures[struct] = [method_name for method_name in dir(struct) if
                          callable(getattr(struct, method_name))]


def get_struct_attributes(name: str) -> type:
    return structures.get(name)


def get_structs_names():
    return structures.keys()


def get_all_structs():
    return dict(structures)
