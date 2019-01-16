import inspect
import sys
from inspect import Parameter, Signature
from typing import Optional

from AI.datatypes import UnknownType
from AI.operations import register_operation


def parse_arg(arg: str):
    kind = Parameter.POSITIONAL_OR_KEYWORD

    if arg.rfind('=') == -1:
        last_equals = len(arg) - 1
    else:
        last_equals = arg.rfind('=')

    if arg.find(':') == -1:
        first_colon = last_equals
    else:
        first_colon = arg.find(':')

    name_offset = 0
    if arg.find('**') != -1 and arg.find('**') < first_colon:
        kind = Parameter.VAR_KEYWORD
        name_offset = 2
    elif arg.find('*') != -1 and arg.find('*') < first_colon:
        kind = Parameter.VAR_POSITIONAL
        name_offset = 1
    return Parameter(name=arg[name_offset:first_colon:],
                     annotation=arg[first_colon + 1:last_equals:],
                     default=arg[last_equals + 1::], kind=kind)


def gen_sig_from_str(s: str):
    return Signature.from_callable(eval("def " + s + ":\n\tpass\n"))


builtins_class_func_signatures = {
    "__new__":           "__new__(cls:type,  *args:object) -> object",
    "__init__":          "__init__(self,  *args:object) -> Self",
    "__del__":           "__del__(self) -> None",
    "__repr__":          "__repr__(self) -> str",
    "__str__":           "__str__(self) -> str",
    "__bytes__":         "__bytes__(self) -> bytes",
    "__format__":        "__format__(self, format_spec) -> str",
    "__lt__":            "__lt__(self, other:object) -> Optional[bool]",
    "__le__":            "__le__(self, other:object) -> Optional[bool]",
    "__eq__":            "__eq__(self, other:object) -> Optional[bool]",
    "__ne__":            "__ne__(self, other:object) -> Optional[bool]",
    "__gt__":            "__gt__(self, other:object) -> Optional[bool]",
    "__ge__":            "__ge__(self, other:object) -> Optional[bool]",
    "__hash__":          "__hash__(self) -> Optional[int]",
    "__bool__":          "__bool__(self) -> bool",
    "__getattr__":       "__getattr__(self, name:str) -> Optional[object]",
    "__getattribute__":  "__getattribute__(self, name:str) -> Optional[object]",
    "__setattr__":       "__setattr__(self, name:str, value:object) -> None",
    "__delattr__":       "__delattr__(self, name:str) -> None",
    "__dir__":           "__dir__(self) -> [str]",
    "__get__":           "__get__(self, instance:object, owner:type) -> Optional[object]",
    "__set__":           "__set__(self, instance:object, value:object) -> None",
    "__delete__":        "__delete__(self, instance:object) -> None",
    "__set_name__":      "__set_name__(self, owner:type, name:str) -> None",
    "__init_subclass__": "__init_subclass__(cls:type) -> object",
    "__instancecheck__": "__instancecheck__(self, instance:object) -> bool",
    "__subclasscheck__": "__subclasscheck__(self, subclass:type) -> bool",
    "__class_getitem__": "__class_getitem__(cls, key) -> Optional[object]",
    "__call__":          "__call__(self,  *args:object) -> None",
    "__len__":           "__len__(self) -> int",
    "__length_hint__":   "__length_hint__(self) -> int",
    "__getitem__":       "__getitem__(self, key:object) -> Optional[object]",
    "__setitem__":       "__setitem__(self, key:object, value:object) -> None",
    "__delitem__":       "__delitem__(self, key:object) -> None",
    "__missing__":       "__missing__(self, key:object) -> bool",
    "__iter__":          "__iter__(self) -> Iterator",
    "__reversed__":      "__reversed__(self) -> Self",
    "__contains__":      "__contains__(self, item:object) -> bool",
    "__add__":           "__add__(self, other:object) -> Self",
    "__sub__":           "__sub__(self, other:object) -> Self",
    "__mul__":           "__mul__(self, other:object) -> Self",
    "__matmul__":        "__matmul__(self, other:object) -> Self",
    "__truediv__":       "__truediv__(self, other:object) -> Self",
    "__floordiv__":      "__floordiv__(self, other:object) -> Self",
    "__mod__":           "__mod__(self, other:object) -> Self",
    "__divmod__":        "__divmod__(self, other:object) -> Self",
    "__pow__":           "__pow__(self, other:object, modulo:Optional[object]) -> Self",
    "__lshift__":        "__lshift__(self, other:object) -> Self",
    "__rshift__":        "__rshift__(self, other:object) -> Self",
    "__and__":           "__and__(self, other:object) -> Self",
    "__xor__":           "__xor__(self, other:object) -> Self",
    "__or__":            "__or__(self, other:object) -> Self",
    "__radd__":          "__radd__(self, other:object) -> Self",
    "__rsub__":          "__rsub__(self, other:object) -> Self",
    "__rmul__":          "__rmul__(self, other:object) -> Self",
    "__rmatmul__":       "__rmatmul__(self, other:object) -> Self",
    "__rtruediv__":      "__rtruediv__(self, other:object) -> Self",
    "__rfloordiv__":     "__rfloordiv__(self, other:object) -> Self",
    "__rmod__":          "__rmod__(self, other:object) -> Self",
    "__rdivmod__":       "__rdivmod__(self, other:object) -> Self",
    "__rpow__":          "__rpow__(self, other:object) -> Self",
    "__rlshift__":       "__rlshift__(self, other:object) -> Self",
    "__rrshift__":       "__rrshift__(self, other:object) -> Self",
    "__rand__":          "__rand__(self, other:object) -> Self",
    "__rxor__":          "__rxor__(self, other:object) -> Self",
    "__ror__":           "__ror__(self, other:object) -> Self",
    "__iadd__":          "__iadd__(self, other:object) -> Self",
    "__isub__":          "__isub__(self, other:object) -> Self",
    "__imul__":          "__imul__(self, other:object) -> Self",
    "__imatmul__":       "__imatmul__(self, other:object) -> Self",
    "__itruediv__":      "__itruediv__(self, other:object) -> Self",
    "__ifloordiv__":     "__ifloordiv__(self, other:object) -> Self",
    "__imod__":          "__imod__(self, other:object) -> Self",
    "__idivmod__":       "__idivmod__(self, other:object) -> Self",
    "__ipow__":          "__ipow__(self, other:object, modulo:Optional[object]) -> Self",
    "__ilshift__":       "__ilshift__(self, other:object) -> Self",
    "__irshift__":       "__irshift__(self, other:object) -> Self",
    "__iand__":          "__iand__(self, other:object) -> Self",
    "__ixor__":          "__ixor__(self, other:object) -> Self",
    "__neg__":           "__neg__(self) -> Self",
    "__pos__":           "__pos__(self) -> Self",
    "__abs__":           "__abs__(self) -> Self",
    "__invert__":        "__invert__(self) -> Self",
    "__complex__":       "__complex__(self) -> complex",
    "__int__":           "__int__(self) -> int",
    "__float__":         "__float__(self) -> float",
    "__index__":         "__index__(self) -> int",
    "__round__":         "__round__(self, ndigits:Optional[int]) -> object",
    "__trunc__":         "__trunc__(self) -> int",
    "__floor__":         "__floor__(self) -> int",
    "__ceil__":          "__ceil__(self) -> int",
    "__await__":         "__await__(self) -> Iterator",
    "__enter__":         "__enter__(self) -> None",
    "__exit__":          "__exit__(self, exc_type:type, exc_value:object, "
                         "traceback:str) -> None",
    "send":              "send(value:Optional[object]) -> Iterator",
    "throw":             "throw(type:type, value:Optional[object], traceback:Optional[str]) -> "
                         "object",
    "close":             "close() -> None",
    "__aiter__":         "__aiter__(self) -> AsyncIterator",
    "__anext__":         "__anext__(self) -> StopAsyncIteration",
    "__aenter__":        "__aenter__(self) -> Awaitable",
    "__aexit__":         "__aexit__(self, exc_type:type, exc_value:object, "
                         "traceback:str) -> Awaitable"
}


# as defined here: https://docs.python.org/3.7/reference/datamodel.html


def get_builtin_func_signature(name: str) -> Signature:
    s = builtins_class_func_signatures[name]
    try:
        exec("def explorator_" + s + ":\n\tpass\n")
    except Exception as e:
        print(name, e)
        exit()
    func = locals()["explorator_" + name]
    sig = Signature.from_callable(func)
    del locals()["explorator_" + name]
    return sig


def get_function_signature(func: classmethod) -> Signature:
    try:
        if func.__module__ == "builtins":
            sig = get_builtin_func_signature(func.__name__)
        else:
            sig = inspect.signature(func)
    except ValueError as ve:
        raise Exception(func.__name__, "doesn't have a signature. Skipping it")
    return sig


def get_function_return_type(func: classmethod) -> type:
    return get_function_return_type_from_sig(get_function_signature(func))


def get_function_param_types(func: classmethod) -> {
    str: type
}:
    return get_function_param_types_from_sig(get_function_signature(func))


def get_function_return_type_from_sig(sig: Signature) -> Optional[type]:
    type_ = sig.return_annotation
    if type_ is None:
        return None
    elif type_ is sig.empty:
        return sig.empty
    elif not inspect.isclass(type_) or not isinstance(type_, type):
        return UnknownType
    else:
        return type_


def get_function_param_types_from_sig(sig: Signature) -> {
    str: type
}:
    args = {}
    params = sig.parameters
    for param in params.values():
        type_ = param.annotation
        if type_ is param.empty and not inspect.isclass(type_):
            args[param.name] = UnknownType()
        elif param.default is not param.empty:
            args[param.name] = type(param.default)
        elif type_ is inspect._empty:
            continue
        else:
            args[param.name] = type_
    return args


def discover_function_from_sig(module: str, class_: str, method: str,
                               sig: Signature) -> None:
    assert module in sys.modules
    register_operation(module, class_, method, class_)
    try:
        paramtypes = get_function_param_types_from_sig(sig)
        returntype = get_function_return_type_from_sig(sig)
    except Exception as e:
        print(module, class_, e)

        return
    for param_name in paramtypes.keys():
        register_operation(module, class_, method, paramtypes[param_name],
                           var_name=param_name)
    if returntype != None:
        register_operation(module, class_, method, returntype.__name__,
                           var_name="__return_type__")
    return


def discover_function(module: str, class_: str, method) -> None:
    assert inspect.isfunction(method) or inspect.ismethod(
        method) or inspect.ismethoddescriptor(method)
    assert module in sys.modules
    register_operation(module, class_, method.__name__, class_)
    try:
        paramtypes = get_function_param_types(method)
        returntype = get_function_return_type(method)
    except Exception as e:
        print(module, class_, e)

        return
    for param_name in paramtypes.keys():
        register_operation(module, class_, method.__name__,
                           paramtypes[param_name], var_name=param_name)
    if returntype != None:
        register_operation(module, class_, method.__name__, returntype.__name__,
                           var_name="__return_type__")
    return


def choose_class_name(class_: type, obj: object) -> str:
    if obj.__class__.__name__ == "wrapper_descriptor":
        return class_.__name__
    else:
        return obj.__class__.__name__


def check_object_is_function(obj: object):
    return inspect.isfunction(obj) or inspect.ismethod(
        obj) or inspect.ismethoddescriptor(obj)


def discover_object_functions(module: str, class_: type,
                              parents: [type]) -> None:
    assert inspect.isclass(class_)
    assert module in sys.modules

    for children_name, children in inspect.getmembers(class_):
        if inspect.isclass(children):
            if children in parents:
                continue
            parents.append(class_)
            discover_object_functions(module, children, parents)
            parents.pop()
        elif check_object_is_function(children):
            name = choose_class_name(class_, children)

            if module == "builtins" and children_name in builtins_class_func_signatures.keys():
                discover_function_from_sig(module, name, children_name,
                                           get_builtin_func_signature(
                                               children_name))
            else:
                discover_function(module, name, children)
        else:
            # TODO implement more data exploration
            continue


def discover_module(module: str) -> None:
    assert module in sys.modules
    for name, children in inspect.getmembers(sys.modules[module]):
        if inspect.isclass(children):
            discover_object_functions(module, children)
        elif check_object_is_function(children):
            if module == "builtins" and name in builtins_class_func_signatures.keys():
                discover_function_from_sig(module, children.__class__.__name__,
                                           name,
                                           get_builtin_func_signature(name))
            else:
                discover_function(module, children.__class__.__name__, children)
        else:
            # TODO implement more data exploration
            continue


def init_exploration():
    discover_module("builtins")
    for type_ in [int, float, complex, bool, str, list, set, dict, tuple, range,
                  frozenset, str, bytes, bytearray, memoryview]:
        discover_object_functions("builtins", type_, [])
