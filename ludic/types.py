from collections.abc import Mapping
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

Headers = Mapping[str, str | Mapping[str, str]]
HXHeaders = TypedDict(
    "HXHeaders",
    {
        "HX-Location": str | Mapping[str, str],
        "HX-Push-Url": str,
        "HX-Redirect": str,
        "HX-Refresh": bool,
        "HX-Replace-Url": str,
        "HX-Reswap": str,
        "HX-Retarget": str,
        "HX-Reselect": str,
        "HX-Trigger": str | Mapping[str, str],
        "HX-Trigger-After-Settle": str | Mapping[str, str],
        "HX-Trigger-After-Swap": str | Mapping[str, str],
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
