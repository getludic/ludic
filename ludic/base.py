from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Iterator, Mapping, MutableMapping, Sequence
from typing import (
    Any,
    ClassVar,
    Generic,
    Never,
    TypeAlias,
    TypedDict,
    Unpack,
    cast,
)

from typing_extensions import TypeVar, TypeVarTuple

from .css import CSSProperties
from .format import FormatContext, format_attrs, format_element
from .utils import get_element_attrs_annotations

ELEMENT_REGISTRY: MutableMapping[str, list[type["BaseElement"]]] = {}

# FIXME: Currently, it is impossible to properly type nested CSS properties
# defined similar as in SCSS, it will be possible when the following PEP is
# implemented and supported by type checkers: https://peps.python.org/pep-0728/
GlobalStyles = Mapping[str, "CSSProperties | GlobalStyles"]
"""CSS styles for elements or components which are defined by setting the ``styles``
class property.

Example usage:

    class Page(Component[AnyChildren, NoAttrs]):
        styles = {
            "body": {
                "background-color": "red",
            },
        }
"""


class Safe(str):
    """Marker for a string that is safe to use as is without HTML escaping.

    That means the content of the string is not escaped when rendered.

    Usage:

        >>> div(Safe("Hello <b>World!</b>")).to_html()
        '<div>Hello <b>World!</b></div>'
    """

    escape = False


class JavaScript(Safe):
    """Marker for a JavaScript string.

    The content of this string is not escaped when rendered.

    Usage:

        js = JavaScript("alert('Hello World!')")
    """


class Attrs(TypedDict, total=False):
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


class NoAttrs(TypedDict):
    """Placeholder for element with no attributes."""


class BaseElement(metaclass=ABCMeta):
    html_header: ClassVar[str | None] = None
    html_name: ClassVar[str | None] = None

    always_pair: ClassVar[bool] = False
    styles: ClassVar[GlobalStyles] = {}

    formatter: ClassVar[FormatContext] = FormatContext("element_formatter")

    children: Sequence[Any]
    attrs: Mapping[str, Any]

    def __init_subclass__(cls) -> None:
        ELEMENT_REGISTRY.setdefault(cls.__name__, [])
        ELEMENT_REGISTRY[cls.__name__].append(cls)

    def __str__(self) -> str:
        return self.to_string()

    def __format__(self, _: str) -> str:
        return self.formatter.append(self)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.children)

    def __repr__(self) -> str:
        return self.to_string(pretty=False)

    def __eq__(self, other: Any) -> bool:
        return (
            type(self) is type(other)
            and self.children == other.children
            and self.attrs == other.attrs
        )

    def _format_attributes(self, is_html: bool = False) -> str:
        attrs: dict[str, Any]
        if is_html:
            attrs = format_attrs(type(self), dict(self.attrs), True)
        else:
            attrs = self.aliased_attrs
        return " ".join(f'{key}="{value}"' for key, value in attrs.items())

    def _format_children(
        self,
        format_fun: Callable[[Any], str] = format_element,
    ) -> str:
        return "".join(format_fun(child) for child in self.children)

    @property
    def aliased_attrs(self) -> dict[str, Any]:
        """Attributes as a dict with keys renamed to their aliases."""
        return format_attrs(type(self), dict(self.attrs))

    @property
    def text(self) -> str:
        return "".join(
            child.text if isinstance(child, BaseElement) else str(child)
            for child in self.children
        )

    def is_simple(self) -> bool:
        """Check if the element is simple (i.e. contains only one primitive type)."""
        return len(self) == 1 and isinstance(self.children[0], str | int | float | bool)

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
        element = f"<{name}"

        if self.has_attributes():
            element += f" {self._format_attributes()}"

        if self.children:
            prefix, sep, suffix = "", "", ""
            if pretty and (not self.is_simple() or self.has_attributes()):
                prefix, sep, suffix = f"\n{indent}  ", f"\n{indent}  ", f"\n{indent}"

            children_str = sep.join(
                child.to_string(pretty=pretty, _level=_level + 1)
                if isinstance(child, BaseElement)
                else str(child)
                for child in self.children
            )

            element += f">{prefix}{children_str}{suffix}</{name}>"
        else:
            element += " />"

        return element

    def to_html(self) -> str:
        """Convert an element tree to an HTML string."""
        dom = self
        while dom != (rendered_dom := dom.render()):
            dom = rendered_dom

        element_tag = f"{dom.html_header}\n" if dom.html_header else ""

        hidden = dom.html_name == "__hidden__"
        element_tag = "" if hidden else f"<{dom.html_name}"

        if dom.has_attributes():
            attributes_str = dom._format_attributes(is_html=True)
            element_tag += f" {attributes_str}"

        if dom.children or dom.always_pair:
            children_str = dom._format_children()
            element_tag += (
                children_str if hidden else f">{children_str}</{dom.html_name}>"
            )
        elif not hidden:
            element_tag += " />"

        return element_tag

    def attrs_for(self, cls: type["BaseElement"]) -> dict[str, Any]:
        """Get the attributes of this component that are defined in the given element.

        This is useful so that you can pass common attributes to an element
        without having to pass them from a parent one by one.

        Args:
            cls (type[BaseElement]): The element to get the attributes of.
        """
        return {
            key: value
            for key, value in self.attrs.items()
            if key in get_element_attrs_annotations(cls)
        }

    def render(self) -> "BaseElement":
        return self


NoChildren: TypeAlias = Never
"""Type alias for elements that are not allowed to have children."""

PrimitiveChildren: TypeAlias = str | bool | int | float
"""Type alias for elements that are allowed to have only primitive children.

Primitive children are ``str``, ``bool``, ``int`` and ``float``.
"""

ComplexChildren: TypeAlias = BaseElement
"""Type alias for elements that are allowed to have only non-primitive children."""

AnyChildren: TypeAlias = PrimitiveChildren | ComplexChildren | Safe
"""Type alias for elements that are allowed to have any children."""

TChildren = TypeVar("TChildren", bound=AnyChildren, default=AnyChildren, covariant=True)
"""Type variable for elements representing type of children (the type of *args).

See also: :class:`ludic.types.Component`.
"""

TChildrenArgs = TypeVarTuple("TChildrenArgs", default=Unpack[tuple[AnyChildren, ...]])
"""Type variable for strict elements representing type of children (the type of *args).

See also: :class:`ludic.types.ComponentStrict`.
"""

TAttrs = TypeVar("TAttrs", bound=Attrs, default=Attrs, covariant=True)
"""Type variable for elements representing type of attributes (the type of **kwargs)."""


class Element(Generic[TChildren, TAttrs], BaseElement):
    """Base class for Ludic elements.

    Args:
        *children (TChild): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[TChildren, ...]
    attrs: TAttrs

    def __init__(
        self,
        *children: TChildren,
        # FIXME: https://github.com/python/typing/issues/1399
        **attributes: Unpack[TAttrs],  # type: ignore
    ) -> None:
        self.attrs = cast(TAttrs, attributes)
        self.children = tuple(self.formatter.extract(*children))


class ElementStrict(Generic[*TChildrenArgs, TAttrs], BaseElement):
    """Base class for strict elements (elements with concrete types of children).

    Args:
        *children (*TChildTuple): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[*TChildrenArgs]
    attrs: TAttrs

    def __init__(
        self,
        *children: *TChildrenArgs,
        # FIXME: https://github.com/python/typing/issues/1399
        **attrs: Unpack[TAttrs],  # type: ignore
    ) -> None:
        self.attrs = cast(TAttrs, attrs)
        self.children = tuple(self.formatter.extract(*children))


class Blank(Element[TChildren, NoAttrs]):
    """Element representing no element at all, just children.

    The purpose of this element is to be able to return only children
    when rendering a component.
    """

    html_name = "__hidden__"

    def __init__(self, *children: TChildren) -> None:
        super().__init__(*self.formatter.extract(*children))


class Component(Element[TChildren, TAttrs], metaclass=ABCMeta):
    """Base class for components.

    A component subclasses an :class:`Element` and represents any element
    that can be rendered in Ludic.

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

    """

    @abstractmethod
    def render(self) -> BaseElement:
        """Render the component as an instance of :class:`BaseElement`."""


class ComponentStrict(ElementStrict[*TChildrenArgs, TAttrs], metaclass=ABCMeta):
    """Base class for strict components.

    A component subclasses an :class:`ElementStrict` and represents any
    element that can be rendered in Ludic. The difference between
    :class:`Component` and :class:`ComponentStrict` is that the latter
    expects concrete types of children. It allows specification
    of each child's type.

    Example usage:

        class PersonAttrs(Attributes):
            age: NotRequired[int]

        class Person(ComponentStrict[str, str, PersonAttrs]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(" ".join(self.children),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )

    Valid usage would look like this:

        >>> div(Person("John", "Doe", age=30), id="person-detail")

    In this case, we specified that Person expects two string children.
    First child is the first name, and the second is the second name.
    We also specify age as an optional key-word argument.
    """

    @abstractmethod
    def render(self) -> BaseElement:
        """Render the component as an instance of :class:`BaseElement`."""
