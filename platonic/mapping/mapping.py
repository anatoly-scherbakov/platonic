import typing
from abc import ABC

from platonic import Model


KeyType = typing.TypeVar('KeyType')
ValueType = typing.TypeVar('ValueType')


class Mapping(Model, typing.Mapping[KeyType, ValueType], ABC):
    KeyType: typing.Type = typing.Any
    ValueType: typing.Type = typing.Any

    def __class_getitem__(cls, args: tuple) -> type:
        if (
            args is None
            or not isinstance(args, tuple)
            or len(args) != 2
        ):
            raise TypeError(
                f'Class {cls.__name__} requires exactly two type arguments, '
                f'Key type and Value type. For example:'
                f'\n'
                f'  {cls.__name__}[str, int]\n'
                f'\n'
                f'means a mapping from strings to integers. Instead, the type '
                f'arguments are: {args}.'
            )

        key_type, value_type = args

        if not isinstance(key_type, type):
            raise ValueError(
                f'Key type {key_type} is a {type(key_type)} value; '
                f'a type expected.'
            )

        if not isinstance(value_type, type):
            raise ValueError(
                f'Value type {value_type} is a {type(value_type)} value; '
                f'a type expected.'
            )

        return type(
            f'{cls.__name__}[{key_type.__name__}, {value_type.__name__}]',
            (cls, ),
            {
                'KeyType': key_type,
                'ValueType': value_type
            }
        )
