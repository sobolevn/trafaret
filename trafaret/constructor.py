import trafaret as t
from trafaret.lib import py3, py3metafix


class ConstructMeta(type):
    def __or__(self, other):
        return construct(other)

    def __and__(self, other):
        return construct(other)


@py3metafix
class C(object):
    __metaclass__ = ConstructMeta


def construct(arg):
    if isinstance(arg, t.Trafaret):
        return arg
    elif isinstance(arg, tuple) or (isinstance(arg, list) and len(arg) > 1):
        return t.Tuple(*(construct(a) for a in arg))
    elif isinstance(arg, list):
        # if len(arg) == 1
        return t.List(construct(arg[0]))
    elif isinstance(arg, dict):
        return t.Dict({construct_key(key): construct(value) for key, value in arg.items()})
    elif isinstance(arg, str):
        return t.Atom(arg)
    elif isinstance(arg, type):
        if arg is int:
            return t.Int()
        elif arg is float:
            return t.Float()
        elif arg is str:
            return t.String()
        elif arg is bool:
            return t.Bool()
        else:
            return t.Type(arg)
    elif callable(arg):
        return t.Call(arg)
    else:
        return arg


def construct_key(key):
    if isinstance(key, t.Key):
        return key
    elif isinstance(key, str):
        if key.endswith('?'):
            return t.Key(key[:-1], optional=True)
        return t.Key(key)
    raise ValueError()
