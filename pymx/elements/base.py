from collections.abc import Callable, Iterator
from typing import (
    Any,
    TypeAlias,
    TypedDict,
    cast,
)

from .utils import (
    default_html_formatter,
    format_attribute,
    format_html_attribute,
    get_element_attributes,
    parse_elements,
    validate_attributes,
    validate_elements,
)

_ELEMENT_REGISTRY: dict[str, type[Any]] = {}


class Safe(str):
    """Marker for a safe string.

    The marker makes it possible to use e.g. f-string notation to render
    elements like here:

        >>> Paragraph(Safe(f"Hello, how {b('are you')}?")).to_html()
        >>> <p>Hello, how <b>are you</b>?</p>
    """

    @staticmethod
    def parse(string: str) -> "AnyChildren":
        parsed_children = parse_elements(string)
        new_children: list[AnyChild] = []
        for child in parsed_children:
            if isinstance(child, str):
                new_children.append(child)
            elif child["tag"] not in _ELEMENT_REGISTRY:
                raise TypeError(
                    f"Element or component {child["tag"]!r} not found, "
                    "maybe you forgot to import it?"
                )
            else:
                element_type = _ELEMENT_REGISTRY[child["tag"]]
                element = element_type(*child["children"], **child["attributes"])
                new_children.append(element)
        return tuple(new_children)


class Attributes(TypedDict, total=False):
    """Attributes of an element or component.

    Example usage::

        class PersonAttributes(Attributes):
            name: str
            age: NotRequired[int]

        class Person(Component[PersonAttributes]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(self.attrs["name"]),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )
    """

    id: str


class Element[*Te, Ta: Attributes]:
    """Base class for PyMX elements.

    Args:
        *children (*Te): The children of the element.
        **attributes (**Ta): The attributes of the element.
    """

    html_name: str

    _children: tuple[*Te]
    _attrs: Ta

    def __init_subclass__(cls) -> None:
        _ELEMENT_REGISTRY[cls.__name__] = cls

    def __init__(self, *children: *Te, **attributes: Any) -> None:
        validate_attributes(self, attributes)
        self._attrs = cast(Ta, attributes)

        if len(children) == 1 and isinstance(children[0], Safe):
            new_children = Safe.parse(children[0])
            validate_elements(self, new_children)
            self._children = cast(tuple[*Te], new_children)

        else:
            validate_elements(self, children)
            self._children = children

    def __str__(self) -> str:
        return self.to_html()

    def __format__(self, _: str) -> str:
        for child in self.children:
            if not isinstance(child, PrimitiveChild):
                raise TypeError(
                    "Only elements with textual children can be used "
                    f"within an f-string, {self!r} contains {child!r}."
                )
        return self.to_string(pretty=False)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.children)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} />"

    def _format_attributes(
        self, formatter: Callable[[str, Any], str] = format_attribute
    ) -> str:
        return " ".join(formatter(key, value) for key, value in self.attrs.items())

    def _format_children(
        self,
        formatter: Callable[[Any], str] = default_html_formatter,
    ) -> str:
        return "".join(formatter(child) for child in self.children)

    @property
    def children(self) -> tuple[*Te]:
        return cast(tuple[*Te], getattr(self, "_children", []))

    @property
    def attrs(self) -> Ta:
        return cast(Ta, getattr(self, "_attrs", {}))

    def is_simple(self) -> bool:
        """Check if the element is simple (i.e. contains only primitive types)."""
        return len(self) == 1 and isinstance(self.children[0], PrimitiveChild)

    def has_attributes(self) -> bool:
        """Check if the element has any attributes."""
        return bool(self.attrs)

    def to_string(self, pretty: bool = True, _level: int = 0) -> str:
        """Convert the element tree to a string representation.

        Args:
            pretty (bool, optional): Whether to indent the string. Defaults to True.

        Returns:
            str: The string representation of the element tree.
        """
        indent = "  " * _level if pretty else ""
        name = self.__class__.__name__
        element = f"{indent}<{name}"

        if _level > 0 and pretty:
            element = f"\n{element}"

        if self.has_attributes():
            element += f" {self._format_attributes()}"

        if self.children:
            children_str = self._format_children(
                lambda child: str(child)
                if isinstance(child, PrimitiveChild)
                else child.to_string(pretty=pretty, _level=_level + 1),
            )

            if pretty:
                if self.is_simple():
                    if self.has_attributes():
                        element += f">\n{indent}  {children_str}\n{indent}</{name}>"
                    else:
                        element += f">{children_str}</{name}>"
                else:
                    element += f">{indent}  {children_str}\n{indent}</{name}>"
            else:
                element += f">{children_str}</{name}>"
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
            children_str = dom._format_children()
            element_tag += f">{children_str}</{dom.html_name}>"
        else:
            element_tag += " />"

        return element_tag

    def attrs_for(self, cls: type["AnyElement"]) -> dict[str, Any]:
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

    def render(self) -> "AnyElement":
        return cast(AnyElement, self)


PrimitiveChild: TypeAlias = Safe | str | bool | int | float
AnyChild: TypeAlias = PrimitiveChild | Element[*tuple["AnyChild", ...], Attributes]

PrimitiveChildren: TypeAlias = tuple[PrimitiveChild, ...]
AnyChildren: TypeAlias = tuple[AnyChild, ...]
AnyElement: TypeAlias = Element[*AnyChildren, Attributes]
