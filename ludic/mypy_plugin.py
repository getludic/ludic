"""This module is designed specifically for use with the mypy plugin."""

from collections.abc import Callable
from typing import TypeVar

from mypy.nodes import ARG_STAR, ARG_STAR2, Argument, TypeInfo, Var
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import add_method
from mypy.types import (
    AnyType,
    NoneTyp,
    TupleType,
    TypeOfAny,
    TypeVarType,
    UnpackType,
)

T = TypeVar("T")
CB = Callable[[T], None] | None

BLACKLISTED_ELEMENTS = {
    "ludic.components.Component",
    "ludic.components.ComponentStrict",
    "ludic.web.endpoints.Endpoint",
}


def is_component_base(info: TypeInfo) -> bool:
    """Check if this is a subclass of a Ludic element."""
    return info.fullname in (
        "ludic.base.Element",
        "ludic.base.ElementStrict",
        "ludic.components.Component",
        "ludic.components.ComponentStrict",
    )


class LudicPlugin(Plugin):
    def get_base_class_hook(self, fullname: str) -> "CB[ClassDefContext]":
        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo):
            if is_component_base(sym.node):
                return add_init_hook
        return None


def add_init_hook(ctx: ClassDefContext) -> None:
    """Add a dummy __init__() to a model and record it is generated.

    Instantiation will be checked more precisely when we inferred types
    (using get_function_hook and model_hook).
    """
    node = ctx.cls.info

    if "__init__" in node.names or node.fullname in BLACKLISTED_ELEMENTS:
        # Don't override existing definition.
        return

    for base in node.bases:
        if is_component_base(base.type) and any(
            not isinstance(arg, TypeVarType) for arg in base.args
        ):
            break
    else:
        return

    match base.type.name:
        case "Element" | "Component":
            args_type = base.args[0]
        case "ElementStrict" | "ComponentStrict":
            args_type = UnpackType(
                TupleType(
                    list(base.args[:-1]),
                    ctx.api.builtin_type("builtins.tuple"),
                )
            )
        case _:
            return

    args_var = Var("args", args_type)
    args_arg = Argument(
        variable=args_var,
        type_annotation=args_type,
        initializer=None,
        kind=ARG_STAR,
    )

    kwargs_type = (
        AnyType(TypeOfAny.special_form)
        if isinstance(base.args[-1], TypeVarType)
        else UnpackType(base.args[-1])
    )
    kwargs_var = Var("kwargs", kwargs_type)
    kwargs_arg = Argument(
        variable=kwargs_var,
        type_annotation=kwargs_type,
        initializer=None,
        kind=ARG_STAR2,
    )

    add_method(ctx, "__init__", [args_arg, kwargs_arg], NoneTyp())
    ctx.cls.info.metadata.setdefault("ludic", {})["generated_init"] = True


def plugin(version: str) -> type[LudicPlugin]:
    return LudicPlugin
