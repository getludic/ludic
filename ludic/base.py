import html
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Iterator
from typing import (
    Any,
    TypedDict,
    Union,
    cast,
)

from .utils import (
    format_attrs,
    get_element_attrs_annotations,
    parse_element,
    validate_attributes,
    validate_elements,
)

_ELEMENT_REGISTRY: dict[str, type["AnyElement"]] = {}


def _parse_children(string: str) -> "AnyChildren":
    element: AnyElement = parse_element(f"<div>{string}</div>", _ELEMENT_REGISTRY)
    return element.children


def default_html_formatter(child: "AnyChild") -> str:
    """Default HTML formatter.

    Args:
        child (AnyChild): The HTML element or text to format.
    """
    if isinstance(child, str) and not isinstance(child, Safe):
        return html.escape(child)
    elif isinstance(child, Element):
        return child.to_html()
    else:
        return str(child)


class Alias(str):
    """Alias type for attributes."""


class Safe(str):
    """Marker for a safe string.

    The marker makes it possible to use e.g. f-string notation to render
    elements like here:

        >>> Paragraph(Safe(f"Hello, how {b('are you')}?")).to_html()
        >>> <p>Hello, how <b>are you</b>?</p>
    """

    @staticmethod
    def parse(string: str) -> Union["AnyChild", "AnyChildren"]:
        result = _parse_children(string)
        if len(result) == 1:
            return result[0]
        else:
            return result


class BaseAttrs(TypedDict, total=False):
    """Attributes of an element or component.

    Example usage::

        class PersonAttrs(Attributes):
            name: str
            age: NotRequired[int]

        class Person(Component[PersonAttrs]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(self.attrs["name"]),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )
    """


class Element[*Te, Ta: BaseAttrs]:
    """Base class for PyMX elements.

    Args:
        *children (*Te): The children of the element.
        **attributes (**Ta): The attributes of the element.
    """

    html_name: str
    always_pair: bool = False

    _children: tuple[*Te]
    _attrs: Ta

    def __init_subclass__(cls) -> None:
        _ELEMENT_REGISTRY[cls.__name__] = cast(type["AnyElement"], cls)

    def __init__(self, *children: *Te, **attributes: Any) -> None:
        validate_attributes(self, attributes)
        self._attrs = cast(Ta, attributes)

        if len(children) == 1 and isinstance(children[0], Safe):
            new_children = _parse_children(children[0])
            validate_elements(self, new_children)
            self._children = cast(tuple[*Te], new_children)

        else:
            validate_elements(self, children)
            self._children = children

    def __str__(self) -> str:
        return self.to_string()

    def __format__(self, _: str) -> str:
        return self.to_string(pretty=False)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.children)

    def __repr__(self) -> str:
        return self.to_string()

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, type(self))
            and self.children == other.children
            and self.attrs == other.attrs
        )

    def _format_attributes(self, html: bool = False) -> str:
        attrs: dict[str, Any]
        if html:
            attrs = format_attrs(type(self), dict(self.attrs), html=True)
        else:
            attrs = self.aliased_attrs
        return " ".join(f'{key}="{value}"' for key, value in attrs.items())

    def _format_children(
        self,
        formatter: Callable[[Any], str] = default_html_formatter,
    ) -> str:
        return "".join(formatter(child) for child in self.children)

    @property
    def children(self) -> tuple[*Te]:
        return cast(tuple[*Te], getattr(self, "_children", []))

    @property
    def text(self) -> str:
        return "".join(
            child.text if isinstance(child, Element) else str(child)
            for child in self.children
        )

    @property
    def attrs(self) -> Ta:
        return cast(Ta, getattr(self, "_attrs", {}))

    @property
    def aliased_attrs(self) -> dict[str, Any]:
        """Attributes as a dict with keys renamed to their aliases."""
        return format_attrs(type(self), dict(self.attrs))

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
        dom = self
        while not hasattr(dom, "html_name"):
            dom = dom.render()

        element_tag = f"<{dom.html_name}"

        if dom.has_attributes():
            attributes_str = dom._format_attributes(html=True)
            element_tag += f" {attributes_str}"

        if dom.children or dom.always_pair:
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
            if key in get_element_attrs_annotations(cls)
        }

    def render(self) -> "AnyElement":
        return cast(AnyElement, self)


class Component[*Te, Ta: BaseAttrs](Element[*Te, Ta], metaclass=ABCMeta):
    """Base class for components.

    A component subclasses an :class:`Element` and represents any element
    that can be rendered in PyMX.

    Example usage:

        class PersonAttrs(Attributes):
            age: NotRequired[int]

        class Person(Component[PersonAttrs]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(self.attrs["name"]),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )

    Now the component can be used in any other component or element:

        >>> div(Person(name="John Doe", age=30), id="person-detail")

    You can also make the component take children:

        class PersonAttrs(Attributes):
            age: NotRequired[int]

        class Person(Component[str, str, PersonAttrs]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(" ".join(self.children)),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )

    Valid usage would now look like this:

        >>> div(Person("John", "Doe", age=30), id="person-detail")
    """

    @abstractmethod
    def render(self) -> "AnyElement":
        """Render the component as an instance of :class:`Element`."""


PrimitiveChild = str | bool | int | float
AnyElement = Element[*tuple["AnyChild", ...], BaseAttrs]
AnyChild = PrimitiveChild | Safe | AnyElement

PrimitiveChildren = tuple[PrimitiveChild, ...]
AnyChildren = tuple[AnyChild, ...]
ComplexChildren = tuple[AnyElement, ...]
