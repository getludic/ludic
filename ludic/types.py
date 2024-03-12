from collections.abc import Iterable, Mapping
from typing import TypedDict

from .base import (
    AnyChildren,
    Attrs,
    BaseElement,
    Blank,
    ComplexChildren,
    Component,
    ComponentStrict,
    Element,
    ElementStrict,
    GlobalStyles,
    JavaScript,
    NoAttrs,
    NoChildren,
    PrimitiveChildren,
    Safe,
    TAttrs,
    TChildren,
    TChildrenArgs,
)

JSONType = (
    Mapping[str, "JSONType"] | Iterable["JSONType"] | str | int | float | bool | None
)
Headers = Mapping[str, JSONType]
HXHeaders = TypedDict(
    "HXHeaders",
    {
        "HX-Location": JSONType,
        "HX-Push-Url": str,
        "HX-Redirect": str,
        "HX-Refresh": bool,
        "HX-Replace-Url": str,
        "HX-Reswap": str,
        "HX-Retarget": str,
        "HX-Reselect": str,
        "HX-Trigger": JSONType,
        "HX-Trigger-After-Settle": JSONType,
        "HX-Trigger-After-Swap": JSONType,
    },
    total=False,
)

__all__ = (
    "AnyChildren",
    "Attrs",
    "BaseElement",
    "ComplexChildren",
    "Component",
    "ComponentStrict",
    "Element",
    "ElementStrict",
    "GlobalStyles",
    "Headers",
    "HXHeaders",
    "JavaScript",
    "NoAttrs",
    "NoChildren",
    "PrimitiveChildren",
    "Safe",
    "TAttrs",
    "TChildren",
    "TChildrenArgs",
    "Blank",
)
