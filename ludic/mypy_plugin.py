"""This module is designed specifically for use with the mypy plugin."""

from collections.abc import Callable
from typing import TypeVar

from mypy.nodes import ARG_STAR, ARG_STAR2, Argument, TypeInfo, Var
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins.common import add_method
from mypy.types import (
    AnyType,
    Instance,
    NoneTyp,
    TupleType,
    Type,
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


def _find_valid_base(node: TypeInfo) -> Instance | None:
    for base in node.bases:
        if not hasattr(base, "type") or not isinstance(base.type, TypeInfo):
            continue
        if not hasattr(base, "args") or not isinstance(base.args, list | tuple):
            continue
        if is_component_base(base.type) and any(
            not isinstance(arg, TypeVarType) for arg in base.args
        ):
            return base
    return None


def _extract_args_type(ctx: ClassDefContext, base: Instance) -> Type | None:  # noqa
    if not hasattr(base, "type") or not isinstance(base.type, TypeInfo):
        ctx.api.fail(f"Base class {base} does not have a valid TypeInfo.", ctx.cls)
        return None
    if not hasattr(base, "args") or not isinstance(base.args, list | tuple):
        ctx.api.fail(f"Base class {base} does not have valid args.", ctx.cls)
        return None
    if not hasattr(base.type, "name"):
        ctx.api.fail(f"Base class {base} type does not have a name attribute.", ctx.cls)
        return None
    if len(base.args) == 0:
        ctx.api.fail(f"Base class {base} has no type arguments.", ctx.cls)
        return None
    try:
        match base.type.name:
            case "Element" | "Component":
                arg = base.args[0]
                if isinstance(arg, Type):
                    return arg
                ctx.api.fail(
                    f"Base class {base} first arg is not a Type.",
                    ctx.cls,
                )
                return None
            case "ElementStrict" | "ComponentStrict":
                if len(base.args) < 1:
                    ctx.api.fail(
                        f"Base class {base} does not have enough type arguments.",
                        ctx.cls,
                    )
                    return None
                tuple_instance = ctx.api.builtin_type("builtins.tuple")
                return UnpackType(
                    TupleType(
                        list(base.args[:-1]),
                        tuple_instance,
                    )
                )
            case _:
                return None
    except Exception as exc:
        ctx.api.fail(f"Error processing base class {base}: {exc}", ctx.cls)
        return None


def _extract_kwargs_type(ctx: ClassDefContext, base: Instance) -> Type | None:
    if len(base.args) == 0:
        ctx.api.fail(f"Base class {base} has no type arguments for kwargs.", ctx.cls)
        return None
    try:
        last_arg = base.args[-1]
        if isinstance(last_arg, TypeVarType):
            return AnyType(TypeOfAny.special_form)
        return UnpackType(last_arg)
    except Exception as exc:
        ctx.api.fail(
            f"Error processing kwargs type for base class {base}: {exc}",
            ctx.cls,
        )
        return None


class LudicPlugin(Plugin):
    def get_base_class_hook(self, fullname: str) -> "CB[ClassDefContext]":
        sym = self.lookup_fully_qualified(fullname)
        if sym and isinstance(sym.node, TypeInfo):
            if is_component_base(sym.node):
                return add_init_hook
        return None


def add_init_hook(ctx: ClassDefContext) -> None:
    """Add a dummy __init__() to a model and record it is generated."""
    node = ctx.cls.info
    if "__init__" in node.names or node.fullname in BLACKLISTED_ELEMENTS:
        return
    base = _find_valid_base(node)
    if base is None:
        return
    args_type = _extract_args_type(ctx, base)
    if args_type is None:
        return
    kwargs_type = _extract_kwargs_type(ctx, base)
    if kwargs_type is None:
        return
    args_var = Var("args", args_type)
    args_arg = Argument(
        variable=args_var,
        type_annotation=args_type,
        initializer=None,
        kind=ARG_STAR,
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
