from collections.abc import Callable
from typing import (
    Any,
    Generic,
    Literal,
    Self,
    TypedDict,
    TypeVar,
    Union,
)

from .styles import Styles
from .utils import format_attribute, format_html_attribute

Primitives = str | bool | int | float
Elements = Union["Element", Primitives]

TElement = TypeVar("TElement", bound=Elements)
TElements = list[TElement]


class Attributes(TypedDict, total=False):
    ...


class HTMLAttributes(Attributes, total=False):
    id: str
    class_: str
    href: str
    name: str
    style: Styles
    value: str


class HTMXAttributes(HTMLAttributes, total=False):
    hx_get: str
    hx_post: str
    hx_put: str
    hx_delete: str
    hx_patch: str

    hx_trigger: str
    hx_target: Literal["this", "next", "previous"] | str
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


TAttributes = TypeVar("TAttributes", bound=Attributes)


class Element(Generic[TElement, TAttributes]):
    @property
    def html_name(self) -> str:
        return self.__class__.__name__.lower()

    def __init__(
        self,
        *children: TElement,
        **attributes: Any,
    ) -> None:
        self._children = list(children)
        self._attributes = attributes

    def __call__(self, *children: TElement) -> Self:
        self._children += children
        return self

    def __getitem__(self, index: int) -> TElement:
        return self._children[index]

    def __getattr__(self, name: str) -> Any:
        if name in self._attributes:
            return self._attributes.__getitem__(name)
        else:
            return super().__getattribute__(name)

    def __str__(self) -> str:
        return self.to_string()

    def _format_attributes(
        self, formatter: Callable[[str, Any], str] = format_attribute
    ) -> str:
        return " ".join(
            formatter(key, value) for key, value in self._attributes.items()
        )

    def _format_children(self, formatter: Callable[[TElement], str] = str) -> str:
        return "".join(formatter(child) for child in self._children)

    def is_simple(self) -> bool:
        return len(self._children) == 1 and isinstance(self._children[0], str)

    def has_attributes(self) -> bool:
        return bool(self._attributes)

    def append(self, element: TElement) -> None:
        self._children.append(element)

    def to_string(self, level: int = 0) -> str:
        dom = self.render()
        indent = "  " * level
        element = f"{indent}<{self.html_name}"

        if level > 0:
            element = f"\n{element}"

        if dom._attributes:
            element += f" {dom._format_attributes()}"

        if dom._children:
            children_str = dom._format_children(
                lambda child: child.to_string(level + 1)
                if isinstance(child, Element)
                else str(child),
            )

            if dom.is_simple():
                if dom.has_attributes():
                    element += (
                        f">\n{indent}  {children_str}\n{indent}</{self.html_name}>"
                    )
                else:
                    element += f">{children_str}</{self.html_name}>"
            else:
                element += f">{indent}  {children_str}\n{indent}</{self.html_name}>"
        else:
            element += " />"

        return element

    def to_html(self) -> str:
        dom = self.render()
        element_tag = f"<{dom.html_name}"

        if dom._attributes:
            attributes_str = dom._format_attributes(format_html_attribute)
            element_tag += f" {attributes_str}"

        if dom._children:
            children_str = dom._format_children(
                lambda child: (
                    child.to_html() if isinstance(child, Element) else str(child)
                ),
            )
            element_tag += f">{children_str}</{dom.html_name}>"
        else:
            element_tag += " />"

        return element_tag

    def render(self) -> "Element":
        return self
