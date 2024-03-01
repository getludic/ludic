import html
from abc import ABCMeta, abstractmethod
from collections.abc import Callable, Iterator, Mapping, Sequence
from typing import (
    Any,
    ClassVar,
    Generic,
    Never,
    TypeAlias,
    TypedDict,
    Unpack,
    cast,
    override,
)

from typing_extensions import TypeVar, TypeVarTuple

from .css import CSSProperties
from .utils import (
    format_attrs,
    get_element_attrs_annotations,
    parse_element,
)

_ELEMENT_REGISTRY: dict[str, list[type["BaseElement"]]] = {}

GlobalStyles = dict[str, CSSProperties]
"""CSS styles for elements or components which are defined by setting the ``styles``
class property.

Example usage:

    class Page(Component[AllowAny, NoAttrs]):
        styles = {
            "body": {
                "background-color": "red",
            },
        }
"""


def _parse_children(string: str) -> tuple["TChild", ...]:
    element = parse_element(f"<div>{string}</div>", _ELEMENT_REGISTRY)
    return tuple(
        Safe(child) if isinstance(child, str) else child for child in element.children
    )


def default_html_formatter(child: "AllowAny") -> str:
    """Default HTML formatter.

    Args:
        child (AnyChild): The HTML element or text to format.
    """
    if isinstance(child, str) and not isinstance(child, Safe):
        return html.escape(child)
    elif isinstance(child, BaseElement):
        return child.to_html()
    else:
        return str(child)


class Safe(str):
    """Marker for a safe string.

    The marker makes it possible to use e.g. f-string notation to render
    elements like here:

        >>> Paragraph(Safe(f"Hello, how {b('are you')}?")).to_html()
        >>> <p>Hello, how <b>are you</b>?</p>
    """

    @staticmethod
    def parse(string: str) -> "AllowAny | tuple[AllowAny, ...]":
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


class NoAttrs(TypedDict):
    """Placeholder for element with no attributes."""


class BaseElement(metaclass=ABCMeta):
    html_name: ClassVar[str | None] = None
    always_pair: ClassVar[bool] = False
    styles: ClassVar[GlobalStyles] = {}

    children: Sequence[Any]
    attrs: Mapping[str, Any]

    def __init_subclass__(cls) -> None:
        _ELEMENT_REGISTRY.setdefault(cls.__name__, [])
        _ELEMENT_REGISTRY[cls.__name__].append(cls)

    def __str__(self) -> str:
        return self.to_string()

    def __format__(self, _: str) -> str:
        return self.to_string(pretty=False)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.children)

    def __repr__(self) -> str:
        return self.to_string(pretty=False)

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
        """Check if the element is simple (i.e. contains only primitive types)."""
        return len(self) == 1 and not isinstance(self.children[0], BaseElement)

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
                lambda child: child.to_string(pretty=pretty, _level=_level + 1)
                if isinstance(child, BaseElement)
                else str(child)
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
        while dom != (rendered_dom := dom.render()):
            dom = rendered_dom

        hidden = dom.html_name == "__hidden__"
        element_tag = "" if hidden else f"<{dom.html_name}"

        if dom.has_attributes():
            attributes_str = dom._format_attributes(html=True)
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
            cls (type): The element to get the attributes of.
        """
        return {
            key: value
            for key, value in self.attrs.items()
            if key in get_element_attrs_annotations(cls)
        }

    @abstractmethod
    def render(self) -> "BaseElement":
        raise NotImplementedError()


NotAllowed: TypeAlias = Never
"""Type alias for elements that are not allowed to have children."""

OnlyPrimitive: TypeAlias = str | bool | int | float
"""Type alias for elements that are allowed to have only primitive children.

Primitive children are ``str``, ``bool``, ``int`` and ``float``.
"""

OnlyComplex: TypeAlias = BaseElement
"""Type alias for elements that are allowed to have only non-primitive children."""

AllowAny: TypeAlias = OnlyPrimitive | OnlyComplex | Safe
"""Type alias for elements that are allowed to have any children."""

TChild = TypeVar("TChild", bound=AllowAny, default=AllowAny, covariant=True)
"""Type variable for elements representing type of children (the type of *args).

See also: :class:`ludic.types.Component`.
"""

TChildTuple = TypeVarTuple("TChildTuple", default=Unpack[tuple[AllowAny, ...]])
"""Type variable for strict elements representing type of children (the type of *args).

See also: :class:`ludic.types.ComponentStrict`.
"""

TAttrs = TypeVar("TAttrs", bound=BaseAttrs, default=BaseAttrs, covariant=True)
"""Type variable for elements representing type of attributes (the type of **kwargs)."""


class Element(Generic[TChild, TAttrs], BaseElement):
    """Base class for Ludic elements.

    Args:
        *children (TChild): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[TChild, ...]
    attrs: TAttrs

    def __init__(
        self,
        *children: TChild,
        # FIXME: https://github.com/python/typing/issues/1399
        **attributes: Unpack[TAttrs],  # type: ignore
    ) -> None:
        self.attrs = cast(TAttrs, attributes)

        parsed_children: list[TChild] = []
        for child in children:
            if isinstance(child, Safe):
                parsed_children.extend(_parse_children(child))
            else:
                parsed_children.append(child)

        self.children = tuple(parsed_children)

    @override
    def render(self) -> BaseElement:
        return self


class ElementStrict(Generic[*TChildTuple, TAttrs], BaseElement):
    """Base class for strict elements (elements with concrete types of children).

    Args:
        *children (*TChildTuple): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[*TChildTuple]
    attrs: TAttrs

    def __init__(
        self,
        *children: *TChildTuple,
        # FIXME: https://github.com/python/typing/issues/1399
        **attrs: Unpack[TAttrs],  # type: ignore
    ) -> None:
        self.attrs = cast(TAttrs, attrs)

        child_list: list[Any] = []
        for child in children:
            if isinstance(child, Safe):
                child_list.extend(_parse_children(child))
            else:
                child_list.append(child)

        self.children = cast(tuple[*TChildTuple], tuple(children))

    @override
    def render(self) -> BaseElement:
        return self


class Children(Element[TChild, NoAttrs]):
    """Element representing no element at all, just children.

    The purpose of this element is to be able to return only children
    when rendering a component.
    """

    html_name = "__hidden__"

    def __init__(self, *children: TChild) -> None:
        super().__init__(*children)

    @override
    def render(self) -> BaseElement:
        return self


class Component(Element[TChild, TAttrs], metaclass=ABCMeta):
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


class ComponentStrict(ElementStrict[*TChildTuple, TAttrs], metaclass=ABCMeta):
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


def locate_element(
    name: str, base_class: type[BaseElement] = BaseElement
) -> type[BaseElement]:
    """Get the element class by its name.

    Args:
        name (str): The name of the element.

    Returns:
        type[TChild]: The element class.
    """
    result = []
    if "." in name:
        module, element_name = name.rsplit(".", 1)
    else:
        module = ""
        element_name = name

    for element in _ELEMENT_REGISTRY[element_name]:
        if issubclass(element, base_class):
            if not module:
                result.append(element)
            submodules = element.__module__.split(".")
            if all(submodule in submodules for submodule in module.split(".")):
                result.append(element)

    if len(result) == 1:
        return result[0]
    elif len(result) > 1:
        raise ValueError(f"Multiple elements found for {name!r}: {result!r}.")
    else:
        raise ValueError(f"Could not locate element: {name!r}.")
