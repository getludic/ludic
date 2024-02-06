from collections.abc import Callable
from typing import (
    Any,
    Generic,
    Never,
    Self,
    TypeAlias,
    TypedDict,
    Union,
    Unpack,
    cast,
)

from typing_extensions import TypeVar, TypeVarTuple

from .utils import (
    format_attribute,
    format_html_attribute,
    get_element_attributes,
    validate_attributes,
    validate_elements,
)

NoChild: TypeAlias = Never
SimpleChild: TypeAlias = str | bool | int | float
AnyChild: TypeAlias = Union["Element[*TElements, TAttributes]", SimpleChild]

NoChildren: TypeAlias = tuple[NoChild, ...]
SimpleChildren: TypeAlias = tuple[SimpleChild, ...]
AnyChildren: TypeAlias = tuple[AnyChild, ...]
AnyElement: TypeAlias = "Element[*tuple[Any, ...], Any]"

TElement = TypeVar("TElement", bound=AnyChild, default=AnyChild)
TElements = TypeVarTuple("TElements", default=Unpack[SimpleChildren])
TAttributes = TypeVar(
    "TAttributes", bound="Attributes", default="Attributes", covariant=True
)


class Attributes(TypedDict):
    """Attributes of an element."""


class Element(Generic[*TElements, TAttributes]):
    """Base class for PyMX elements.

    Args:
        *children (*TElements): The children of the element.
        **attributes (**TAttributes): The attributes of the element.
    """

    html_name: str

    _children: tuple[*TElements]
    _attrs: TAttributes

    def __init__(
        self,
        *children: *TElements,
        # **attributes should be typed as Unpack[TAttributes]
        # see https://github.com/python/typing/issues/1399
        **attributes: Any,
    ) -> None:
        validate_attributes(self, attributes)
        validate_elements(self, children)

        self._children = children
        self._attrs = cast(TAttributes, attributes)

    def __call__(self, *children: *TElements) -> Self:
        self._children = children
        return self

    def __getitem__(self, index: int):
        return self.children[index]

    def __str__(self) -> str:
        return self.to_html()

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __repr__(self) -> str:
        name = self.__class__.__name__
        attrs = f" {self._format_attributes()}" if self.has_attributes() else ""

        if self.children:
            if len(self) == 1:
                return f"<{name}{attrs}>.. 1 child ..</{name}>"
            else:
                return f"<{name}{attrs}>.. {len(self)} children ..</{name}>"
        else:
            return f"<{name}{attrs} />"

    def _format_attributes(
        self, formatter: Callable[[str, Any], str] = format_attribute
    ) -> str:
        return " ".join(formatter(key, value) for key, value in self.attrs.items())

    def _format_children(self, formatter: Callable[[TElement], str] = str) -> str:
        return "".join(formatter(child) for child in self if child is not None)

    @property
    def children(self) -> tuple[*TElements]:
        return cast(tuple[*TElements], getattr(self, "_children", []))

    @property
    def attrs(self) -> TAttributes:
        return cast(TAttributes, getattr(self, "_attrs", {}))

    def is_simple(self) -> bool:
        """Check if the element is simple (i.e. contains only primitive types)."""
        return len(self) == 1 and isinstance(self[0], str | bool | int | float)

    def has_attributes(self) -> bool:
        """Check if the element has any attributes."""
        return bool(self.attrs)

    def to_string(self, _level: int = 0) -> str:
        """Convert the element tree to a string representation."""
        dom = self.render()
        indent = "  " * _level
        name = self.__class__.__name__
        element = f"{indent}<{name}"

        if _level > 0:
            element = f"\n{element}"

        if dom.has_attributes():
            element += f" {dom._format_attributes()}"

        if dom.children:
            children_str = dom._format_children(
                lambda child: child.to_string(_level + 1)
                if hasattr(child, "to_string")
                else str(child),
            )

            if dom.is_simple():
                if dom.has_attributes():
                    element += f">\n{indent}  {children_str}\n{indent}</{name}>"
                else:
                    element += f">{children_str}</{name}>"
            else:
                element += f">{indent}  {children_str}\n{indent}</{name}>"
        else:
            element += " />"

        return element

    def to_html(self) -> str:
        """Convert the element tree to an HTML string."""
        dom = self.render()
        element_tag = f"<{dom.html_name}"

        if dom.has_attributes():
            attributes_str = dom._format_attributes(format_html_attribute)
            element_tag += f" {attributes_str}"

        if dom.children:
            children_str = dom._format_children(
                lambda child: (
                    child.to_html() if hasattr(child, "to_html") else str(child)
                ),
            )
            element_tag += f">{children_str}</{dom.html_name}>"
        else:
            element_tag += " />"

        return element_tag

    def attrs_for(self, cls: type[AnyElement]) -> dict[str, Any]:
        """Get the attributes of this component that are defined in the given element.

        This is useful so that you can pass common attributes to an element
        without having to pass them from a parent one by one.

        Args:
            cls (type): The element to get the attributes of.
        """
        return {
            key: value
            for key, value in self.attrs.items()
            if key in get_element_attributes(cls)
        }

    def render(self) -> AnyElement:
        return self
