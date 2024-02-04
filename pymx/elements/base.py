from collections.abc import Callable
from typing import (
    Any,
    Generic,
    Literal,
    Never,
    Self,
    Union,
)

from typing_extensions import TypeVar, TypeVarTuple

from .styles import Styles
from .utils import format_attribute, format_html_attribute

Text = str | bool | int | float
Complex = Union["Element", Text]

TElement = TypeVar("TElement", bound=Text, default=Never)
TElements = TypeVarTuple("TElements")


class Attributes:
    id: str

    def __init__(self, **kwargs: Any) -> None:
        members = {}
        for cls in type(self).__mro__:
            if cls is not Generic and issubclass(cls, Attributes):
                members.update(cls.__annotations__)

        for key, value in kwargs.items():
            if key not in members:
                raise TypeError(f"{key} is not a valid attribute")
            if members[key].__name__ == "Literal":
                if value not in members[key].__args__:
                    raise TypeError(f"{key} must be one of {members[key].__args__}")
            elif dict in getattr(members[key], "__mro__", []):
                if not isinstance(value, dict):
                    raise TypeError(f"{key} must be of type {members[key]}")
            elif not isinstance(value, members[key]):
                raise TypeError(f"{key} must be of type {members[key]}")
            setattr(self, key, value)


class HTMLAttributes(Attributes):
    class_: str
    href: str
    name: str
    style: Styles
    value: str


class HTMXAttributes(HTMLAttributes):
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


TAttributes = TypeVar("TAttributes", bound=Attributes, default=Attributes)


class Element(Generic[*TElements]):
    html_name: str

    _children: tuple[*TElements]
    _attributes: list[str]

    @property
    def attrs(self) -> dict[str, Any]:
        return {key: getattr(self, key) for key in self._attributes}

    def __init__(
        self,
        *children: *TElements,
        **attributes: Any,
    ) -> None:
        self._children = children
        self._attributes = list(attributes.keys())
        super().__init__(**attributes)

    def __call__(self, *children: *TElements) -> Self:
        self._children = children
        return self

    def __getitem__(self, index: int):
        return self._children[index]

    def __str__(self) -> str:
        return self.to_string()

    def __len__(self) -> int:
        return len(self._children)

    def __iter__(self):
        return iter(self._children)

    def _format_attributes(
        self, formatter: Callable[[str, Any], str] = format_attribute
    ) -> str:
        return " ".join(formatter(key, getattr(self, key)) for key in self._attributes)

    def _format_children(self, formatter: Callable[[TElement], str] = str) -> str:
        return "".join(formatter(child) for child in self)

    def is_simple(self) -> bool:
        return len(self) == 1 and isinstance(self[0], str)

    def has_attributes(self) -> bool:
        return bool(self._attributes)

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
                if hasattr(child, "to_string")
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
                    child.to_html() if hasattr(child, "to_html") else str(child)
                ),
            )
            element_tag += f">{children_str}</{dom.html_name}>"
        else:
            element_tag += " />"

        return element_tag

    def render(self) -> "Element":
        return self
