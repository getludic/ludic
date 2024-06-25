from collections.abc import Iterable, Mapping
from typing import Never, TypeAlias, TypedDict, TypeVar, TypeVarTuple

from .attrs import Attrs, NoAttrs, URLType
from .base import BaseElement
from .styles import CSSProperties, GlobalStyles


class Safe(str):
    """Marker for a string that is safe to use as is without HTML escaping.

    That means the content of the string is not escaped when rendered.

    Usage:

        >>> div(Safe("Hello <b>World!</b>")).to_html()
        '<div>Hello <b>World!</b></div>'
    """

    escape = False


class JavaScript(Safe):
    """Marker for a JavaScript string.

    The content of this string is not escaped when rendered.

    Usage:

        js = JavaScript("alert('Hello World!')")
    """


JSONType = (
    Mapping[str, "JSONType"] | Iterable["JSONType"] | str | int | float | bool | None
)
Headers = Mapping[str, JSONType]
HXHeaders = TypedDict(
    "HXHeaders",
    {
        "HX-Location": JSONType,
        "HX-Push-Url": URLType | bool,
        "HX-Redirect": str,
        "HX-Refresh": bool,
        "HX-Replace-Url": URLType,
        "HX-Reswap": str,
        "HX-Retarget": str,
        "HX-Reselect": str,
        "HX-Trigger": JSONType,
        "HX-Trigger-After-Settle": JSONType,
        "HX-Trigger-After-Swap": JSONType,
    },
    total=False,
)

NoChildren: TypeAlias = Never
"""Type alias for elements that are not allowed to have children."""

PrimitiveChildren: TypeAlias = str | bool | int | float
"""Type alias for elements that are allowed to have only primitive children.

Primitive children are ``str``, ``bool``, ``int`` and ``float``.
"""

ComplexChildren: TypeAlias = BaseElement
"""Type alias for elements that are allowed to have only non-primitive children."""

AnyChildren: TypeAlias = PrimitiveChildren | ComplexChildren | Safe
"""Type alias for elements that are allowed to have any children."""

TChildren = TypeVar("TChildren", bound=AnyChildren, covariant=True)
"""Type variable for elements representing type of children (the type of *args).

See also: :class:`ludic.types.Component`.
"""

TChildrenArgs = TypeVarTuple("TChildrenArgs")
"""Type variable for strict elements representing type of children (the type of *args).

See also: :class:`ludic.types.ComponentStrict`.
"""

TAttrs = TypeVar("TAttrs", bound=Attrs | NoAttrs, covariant=True)
"""Type variable for elements representing type of attributes (the type of **kwargs)."""


__all__ = (
    "AnyChildren",
    "ComplexChildren",
    "CSSProperties",
    "GlobalStyles",
    "Headers",
    "HXHeaders",
    "URLType",
    "JavaScript",
    "NoChildren",
    "PrimitiveChildren",
    "Safe",
    "TAttrs",
    "TChildren",
    "TChildrenArgs",
)
