from collections.abc import Iterable, Mapping
from typing import TypedDict

from .attrs import URLType as URLType
from .base import (
    AnyChildren,
    Attrs,
    BaseElement,
    ComplexChildren,
    Element,
    ElementStrict,
    JavaScript,
    NoAttrs,
    NoChildren,
    PrimitiveChildren,
    Safe,
    TAttrs,
    TChildren,
    TChildrenArgs,
)
from .components import Blank, Component, ComponentStrict
from .styles import CSSProperties, GlobalStyles, Theme

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

__all__ = (
    "AnyChildren",
    "Attrs",
    "BaseElement",
    "ComplexChildren",
    "Component",
    "ComponentStrict",
    "CSSProperties",
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
    "Theme",
    "Blank",
)
