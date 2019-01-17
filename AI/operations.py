from collections import Collection

from AI.caching import operations
from AI.datatypes import getobjectmodulename
from AI.structures import Structure


# all operations names regrouped by common datatypes


def register_operation(module: str, version: str, class_: str, method: str,
                       type_name: str,
                       var_name: str = "self") -> None:
    if type_name == "self":
        type_name = class_
    elif type_name is None:
        type_name = "None"

    from AI.caching import register_operation_into_cache
    register_operation_into_cache(module, version, class_, method, var_name,
                                  type_name)
    from AI.caching import load_operation_from_cache
    load_operation_from_cache(module, version, class_, method, var_name)
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
