from abc import ABCMeta, abstractmethod
from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, ClassVar, Generic, Unpack, override

from .attrs import GlobalAttrs, NoAttrs
from .base import BaseElement
from .format import format_attrs
from .html import div, span
from .styles import Theme, get_default_theme, types
from .types import AnyChildren, TAttrs, TChildren, TChildrenArgs
from .utils import get_element_attrs_annotations

COMPONENT_REGISTRY: MutableMapping[str, list[type["BaseComponent"]]] = {}


class BaseComponent(metaclass=ABCMeta):
    classes: ClassVar[Sequence[str]] = []
    styles: ClassVar[types.GlobalStyles] = {}

    children: Sequence[Any]
    attrs: Mapping[str, Any]
    context: MutableMapping[str, Any]

    def __init__(self, *children: Any, **attrs: Any) -> None:
        self.children = children
        self.attrs = attrs

    def __init_subclass__(cls) -> None:
        COMPONENT_REGISTRY.setdefault(cls.__name__, [])
        COMPONENT_REGISTRY[cls.__name__].append(cls)

    def __len__(self) -> int:
        return len(self.children)

    def __str__(self) -> str:
        return self.to_html()

    def __repr__(self) -> str:
        return self.to_string()

    @property
    def text(self) -> str:
        """Get the text content of the element."""
        return "".join(getattr(child, "text", str(child)) for child in self.children)

    @property
    def theme(self) -> Theme:
        """Get the theme of the element."""
        if context_theme := self.context.get("theme"):
            if isinstance(context_theme, Theme):
                return context_theme
        return get_default_theme()

    def has_attributes(self) -> bool:
        return bool(self.attrs)

    def is_simple(self) -> bool:
        return len(self) == 1 and all(
            isinstance(child, str | int | bool | float) for child in self.children
        )

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
            element += f" {format_attrs(type(self), self.attrs)}"

        if self.children:
            prefix, sep, suffix = "", "", ""
            if pretty and (not self.is_simple() or self.has_attributes()):
                prefix, sep, suffix = f"\n{indent}  ", f"\n{indent}  ", f"\n{indent}"

            children_str = sep.join(repr(child) for child in self.children)

            element += f">{prefix}{children_str}{suffix}</{name}>"
        else:
            element += " />"

        return element

    def to_html(self) -> str:
        dom: BaseElement | BaseComponent = self
        classes: list[str] = []

        while isinstance(dom, BaseComponent):
            classes += dom.classes
            dom = dom.render()
            dom.context.update(dom.context)

        return dom.to_html()

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
            if key in get_element_attrs_annotations(cls)  # type: ignore
        }

    @abstractmethod
    def render(self) -> BaseElement:
        """Render the component as an instance of :class:`BaseElement`."""


class Component(Generic[TChildren, TAttrs], BaseComponent):
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

    children: tuple[TChildren, ...]
    attrs: TAttrs

    def __init__(
        self,
        *children: TChildren,
        # FIXME: https://github.com/python/typing/issues/1399
        **attrs: Unpack[TAttrs],  # type: ignore
    ) -> None:
        super().__init__(*children, **attrs)


class ComponentStrict(Generic[*TChildrenArgs, TAttrs], BaseComponent):
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

    children: tuple[*TChildrenArgs]
    attrs: TAttrs

    def __init__(
        self,
        *children: *TChildrenArgs,
        # FIXME: https://github.com/python/typing/issues/1399
        **attrs: Unpack[TAttrs],  # type: ignore
    ) -> None:
        super().__init__(*children, **attrs)


class Block(Component[AnyChildren, GlobalAttrs]):
    """Component rendering as a div"""

    @override
    def render(self) -> div:
        return div(*self.children, **self.attrs)


class Inline(Component[AnyChildren, GlobalAttrs]):
    """Component rendering as a span"""

    @override
    def render(self) -> span:
        return span(*self.children, **self.attrs)


class Blank(Component[TChildren, NoAttrs]):
    """Component representing no component at all, just children.

    The purpose of this component is to be able to render only children
    when rendering a component.
    """

    def to_html(self) -> str:
        return "".join(map(str, self.children))

    @override
    def render(self) -> div:
        return div()  # workaround, we need to return a base element
