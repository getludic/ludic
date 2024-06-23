from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping
from typing import Any, Generic

from .base import BaseElement
from .styles import Theme, get_default_theme
from .utils import get_element_attrs_annotations
from .format import format_attrs
from .types import NoAttrs, TAttrs, TChildren, TChildrenArgs

COMPONENT_REGISTRY: MutableMapping[str, list[type["BaseElement"]]] = {}


class BaseComponent(BaseElement, metaclass=ABCMeta):
    def __init_subclass__(cls) -> None:
        COMPONENT_REGISTRY.setdefault(cls.__name__, [])
        COMPONENT_REGISTRY[cls.__name__].append(cls)

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_string(pretty=False)

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


class Blank(Component[TChildren, NoAttrs]):
    """Element representing no element at all, just children.

    The purpose of this element is to be able to return only children
    when rendering a component.
    """
