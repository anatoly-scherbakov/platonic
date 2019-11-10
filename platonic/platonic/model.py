from abc import ABC


PROXY_CLASS_ATTRIBUTE = '__is_proxy_class'


def create_proxy_class(cls):
    concrete_class = cls.__backend__
    abstract_class = cls

    if concrete_class is None:
        raise TypeError(
            f'{abstract_class} does not have a backend defined. Please use '
            f'platonic.register() decorator to assign one.'
        )

    bases = (
        concrete_class,
        abstract_class
    )

    class_name = f'{abstract_class.__name__} via {concrete_class.__name__}'

    # noinspection PyTypeChecker
    return type(class_name, bases, {
        PROXY_CLASS_ATTRIBUTE: True,
        '__type_args__': abstract_class.__validate_type_args__(
            abstract_class.__type_args__
        )
    })


class Model(ABC):
    __backend__: type = None
    proxy_class: type = None
    __type_args__ = None

    @classmethod
    def __validate_type_args__(cls, args):
        return args

    # noinspection PyUnresolvedReferences
    def __class_getitem__(cls, params):
        cls.__type_args__ = params
        return super(Model, cls).__class_getitem__(params)

    def __new__(cls, *args, **kwargs):
        if getattr(cls, PROXY_CLASS_ATTRIBUTE, False):
            return super().__new__(cls, *args, **kwargs)

        if cls.proxy_class is None:
            cls.proxy_class = create_proxy_class(cls)

        concrete_class = cls.__backend__

        return concrete_class.__new__(cls.proxy_class, *args, **kwargs)
