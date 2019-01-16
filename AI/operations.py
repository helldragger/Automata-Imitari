from collections import Collection

from AI.datatypes import getobjectmodulename
from AI.structures import Structure


operations: {
    (str, str, str, str): set
} = {}


# all operations names regrouped by common datatypes


def register_operation(module: str, class_: str, method: str, type_name: str,
                       var_name: str = "self") -> None:
    if type_name == "self":
        type_name = class_
    elif type_name is None:
        type_name = "None"
    if (module, class_, method, var_name) in operations.keys():
        operations[(module, class_, method, var_name)].add(type_name)
    else:
        operations[(module, class_, method, var_name)] = {type_name}
    return


def content_has_attribute(o: Collection, method_name: str) -> bool:
    if len(o) == 0:
        raise Exception("EMPTY STRUCTURE")
    module, class_ = getobjectmodulename(o.__iter__().__next__())

    if (module, class_, method_name, "self") in operations.keys():
        return type(o.__iter__().__next__()).__name__ in operations[
            (module, class_, method_name, "self")]
    return False


def mean(data: Structure) -> float:
    assert content_has_attribute(data, "__add__")
    assert content_has_attribute(data, "__divmod__")
    value: type(data.content_type) = None
    for i in data:
        if value is None:
            value = i
        else:
            value += i
    return value / len(data)
