from typing import Literal, TypedDict

from .base import Attributes

HTMLStyles = TypedDict(
    "HTMLStyles",
    {
        "color": str,
        "direction": Literal["row", "column"],
        "height": str,
        "justify-content": Literal["start", "end", "center", "equally-spaced"],
        "width": str,
    },
    total=False,
)


class HTMLAttributes(Attributes, total=False):
    id: str
    class_: str
    href: str
    name: str
    style: HTMLStyles
    value: str


class HTMXAttributes(HTMLAttributes, total=False):
    hx_get: str
    hx_post: str
    hx_put: str
    hx_delete: str
    hx_patch: str

    hx_trigger: str
    hx_target: str
    hx_swap: Literal[
        "innerHTML",
        "outerHTML",
        "beforebegin",
        "afterbegin",
        "beforeend",
        "afterend",
        "delete",
        "none",
    ]


class MetaAttributes(Attributes):
    name: str
    content: str


class LinkAttributes(Attributes, total=False):
    rel: Literal["canonical", "alternate"]
    hreflang: str
    href: str
