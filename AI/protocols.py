import inspect
from abc import abstractmethod
from inspect import Signature
from typing import Collection, Set


class IAProtocol():
    def __init__(self):
        ia_protocols.add(self.__class__)

    def is_protocol(self) -> bool:
        return True

    @staticmethod
    def is_applicable(protocol: object, obj: object) -> bool:
        assert issubclass(protocol, IAProtocol)
        from AI.explorator import check_object_is_function
        obj_attr_list = inspect.getmembers(obj,
                                           predicate=check_object_is_function)
        pro_attr_list = inspect.getmembers(protocol,
                                           predicate=check_object_is_function)
        for pro_attr_name, pro_attr_data in pro_attr_list:
            is_present = False
            for obj_attr_name, obj_attr_data in obj_attr_list:
                if pro_attr_name == obj_attr_name:
                    is_present = True
                    break
            if not is_present:
                return False
        return True


ia_protocols: Set[IAProtocol] = set()

ia_protocols.add(IAProtocol)


class Sortable(IAProtocol):
    @abstractmethod
    def __eq__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __ne__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __le__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __lt__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __gt__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __ge__(self, other):
        raise NotImplementedError

    @abstractmethod
    def __abs__(self, other):
        raise NotImplementedError


ia_protocols.add(Sortable)


class Sorted(Collection, IAProtocol):
    @abstractmethod
    def sort(self, data: Collection[Sortable], *args: Collection[object],
             **kwargs: Collection[object]) -> Collection[Sortable]:
        raise NotImplementedError

    def sorted_by(self) -> classmethod:
        return self.sort

    def __str__(self):
        return Signature(self.sort)


ia_protocols.add(Sorted)


def is_protocol(type_: IAProtocol) -> bool:
    try:
        return type_.is_protocol()
    except Exception as e:
        return False


def get_applicable_protocols(obj: object) -> Set[IAProtocol]:
    protocols: Set[IAProtocol] = set()
    for protocol in ia_protocols:
        if IAProtocol.is_applicable(protocol, obj):
            protocols.add(protocol)
    return protocols
