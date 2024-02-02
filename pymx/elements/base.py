from collections.abc import Callable
from typing import (
    Any,
    Generic,
    Literal,
    NotRequired,
    Self,
    TypedDict,
    TypeVar,
    Union,
    Unpack,
)

from .styles import Styles
from .utils import format_attribute, format_html_attribute

Child = TypeVar("Child", bound=Union["Element", str])
Children = tuple[Child, ...]


class Attributes(TypedDict):
    class_: NotRequired[str]
    href: NotRequired[str]
    id: NotRequired[str]
    name: NotRequired[str]
    style: NotRequired[Styles]
    value: NotRequired[str]

    hx_get: NotRequired[str]
    hx_post: NotRequired[str]
    hx_put: NotRequired[str]
    hx_delete: NotRequired[str]
    hx_patch: NotRequired[str]

    hx_trigger: NotRequired[str]
    hx_target: NotRequired[Literal["this", "next", "previous"] | str]
    hx_swap: NotRequired[
        Literal[
            "innerHTML",
            "outerHTML",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ]
    ]


def format_attributes(
    attributes: Attributes, formatter: Callable[[str, Any], str] = format_attribute
) -> str:
    return " ".join(formatter(key, value) for key, value in attributes.items())


def format_children(children: Children, formatter: Callable[[Child], str] = str) -> str:
    return "".join(formatter(child) for child in children)


class Element(Generic[Child]):
    html_name: str

    _children: Children
    _attributes: Attributes

    def __init__(
        self,
        *children: Child,
        **attributes: Unpack[Attributes],
    ) -> None:
        self._children = children
        self._attributes = attributes

    def __call__(self, *children: Child) -> Self:
        self._children += children
        return self

    def __getitem__(self, index: int) -> Child:
        return self._children[index]

    def __getattr__(self, name: str) -> Any:
        if name in self._attributes:
            return self._attributes.__getitem__(name)
        else:
            return super().__getattribute__(name)

    def __str__(self) -> str:
        return self.as_string()

    def is_simple(self) -> bool:
        return len(self._children) == 1 and isinstance(self._children[0], str)

    def has_attributes(self) -> bool:
        return bool(self._attributes)

    def as_string(self, level: int = 0) -> str:
        element_name = self.__class__.__name__
        indent = "  " * level
        element = f"{indent}<{element_name}"

        if level > 0:
            element = f"\n{element}"

        if self._attributes:
            element += f" {format_attributes(self._attributes)}"

        if self._children:
            children_str = format_children(
                self._children,
                lambda child: child.as_string(level + 1)
                if isinstance(child, Element)
                else str(child),
            )

            if self.is_simple():
                if self.has_attributes():
                    element += f">\n{indent}  {children_str}\n{indent}</{element_name}>"
                else:
                    element += f">{children_str}</{element_name}>"
            else:
                element += f">{indent}  {children_str}\n{indent}</{element_name}>"
        else:
            element += " />"

        return element

    def as_html(self) -> str:
        element_tag = f"<{self.html_name}"

        if self._attributes:
            attributes_str = format_attributes(self._attributes, format_html_attribute)
            element_tag += f" {attributes_str}"

        if self._children:
            children_str = format_children(
                self._children,
                lambda child: (
                    child.as_html() if isinstance(child, Element) else str(child)
                ),
            )
            element_tag += f">{children_str}</{self.html_name}>"
        else:
            element_tag += " />"

        return element_tag
