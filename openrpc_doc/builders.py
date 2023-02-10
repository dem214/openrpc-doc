import dataclasses
import inspect
import types
import typing
from typing import Self, Literal, Type, Union

json_types = Literal['string', 'number', 'object', 'array', 'boolean', 'null']


@dataclasses.dataclass(frozen=True)
class Schema:
    type: json_types | frozenset[json_types]


PRIMITIVE_TYPE_MAPPING: dict[Type, json_types] = {
    str: 'string',
    int: 'number',
    float: 'number',
    None: 'null',

}


def schema(type_) -> Schema:
    if type_ in PRIMITIVE_TYPE_MAPPING:
        return Schema(type=PRIMITIVE_TYPE_MAPPING[type_])
    if isinstance(type_, types.UnionType):
        return Schema(type=frozenset(PRIMITIVE_TYPE_MAPPING[arg] for arg in type_.__args__))
    raise ValueError


class Param:

    def __init__(self, name: str, type_, positional_only: bool = False, required: bool = False):
        self.name = name
        self.type_ = type_
        self.required = required
        self.positional_only = positional_only


class Method:

    def __init__(self, name, params, return_type=None):
        self.name = name
        self.params = params
        self.return_type = return_type

    @classmethod
    def from_func(cls, func: typing.Callable):
        name = func.__name__
        signature = inspect.signature(func)

        params = [Param(
            name=name,
            type_=parameter.annotation,
            required=parameter.default is parameter.empty,
            positional_only=parameter.kind is parameter.POSITIONAL_ONLY
        ) for name, parameter in signature.parameters.items()]
        return_type = signature.return_annotation if signature.return_annotation is not signature.empty else None
        return cls(name=name, params=params, return_type=return_type)


class OpenRPCBuilder:

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.methods = []

    def add_method(self, method: Method) -> Self:
        self.methods.append(method)
        return self
