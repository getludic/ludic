from abc import ABCMeta
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

from .format import FormatContext, format_attrs, format_element
from .styles import GlobalStyles, Theme, get_default_theme
from .utils import get_element_attrs_annotations

ELEMENT_REGISTRY: MutableMapping[str, list[type["BaseElement"]]] = {}


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
    formatter: ClassVar[FormatContext] = FormatContext("element_formatter")

    classes: ClassVar[Sequence[str]] = []
    styles: ClassVar["GlobalStyles"] = {}

    children: Sequence[Any]
    attrs: Mapping[str, Any]

    context: dict[str, Any]

    def __init_subclass__(cls) -> None:
        ELEMENT_REGISTRY.setdefault(cls.__name__, [])
        ELEMENT_REGISTRY[cls.__name__].append(cls)

    def __init__(self, *children: Any, **attrs: Any) -> None:
        self.context = {}
        self.children = children
        self.attrs = attrs

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

    def _format_attributes(
        self, classes: list[str] | None = None, is_html: bool = False
    ) -> str:
        attrs: dict[str, Any]
        if is_html:
            attrs = format_attrs(type(self), dict(self.attrs), is_html=True)
        else:
            attrs = self.aliased_attrs

        if classes:
            if "class" in attrs:
                attrs["class"] += " " + " ".join(classes)
            else:
                attrs["class"] = " ".join(classes)

        return " ".join(
            f'{key}="{value}"' if '"' not in value else f"{key}='{value}'"
            for key, value in attrs.items()
        )

    def _format_children(
        self,
        format_fun: Callable[[Any], str] = format_element,
    ) -> str:
        formatted = []
        for child in self.children:
            if isinstance(child, BaseElement):
                child.context.update(self.context)
            formatted.append(format_fun(child))
        return "".join(formatted)

    @property
    def aliased_attrs(self) -> dict[str, Any]:
        """Attributes as a dict with keys renamed to their aliases."""
        return format_attrs(type(self), dict(self.attrs))

    @property
    def text(self) -> str:
        """Get the text content of the element."""
        return "".join(
            child.text if isinstance(child, BaseElement) else str(child)
            for child in self.children
        )

    @property
    def theme(self) -> Theme:
        """Get the theme of the element."""
        if context_theme := self.context.get("theme"):
            if isinstance(context_theme, Theme):
                return context_theme
        return get_default_theme()

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
        classes = list(dom.classes)

        while dom != (rendered_dom := dom.render()):
            rendered_dom.context.update(dom.context)
            dom = rendered_dom
            classes += dom.classes

        element_tag = f"{dom.html_header}\n" if dom.html_header else ""
        children_str = dom._format_children() if dom.children else ""

        if dom.html_name == "__hidden__":
            element_tag += children_str
            return element_tag
        
        element_tag += f"<{dom.html_name}"
        if (dom.has_attributes() or classes):
            attributes_str = dom._format_attributes(classes, is_html=True)
            element_tag += f" {attributes_str}"
        
        if dom.children or dom.always_pair:
            element_tag += f">{children_str}</{dom.html_name}>"
        else:
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

TAttrs = TypeVar("TAttrs", bound=Attrs | NoAttrs, default=Attrs, covariant=True)
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
        super().__init__()
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
        super().__init__()
        self.attrs = cast(TAttrs, attrs)
        self.children = tuple(self.formatter.extract(*children))
