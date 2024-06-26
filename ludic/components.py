from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping, Sequence
from typing import Any, ClassVar, override

from .attrs import GlobalAttrs
from .base import BaseElement
from .elements import Blank as Blank
from .elements import Element, ElementStrict
from .html import div, span
from .styles import Theme, get_default_theme
from .styles.types import GlobalStyles
from .types import AnyChildren, TAttrs, TChildren, TChildrenArgs
from .utils import get_element_attrs_annotations

COMPONENT_REGISTRY: MutableMapping[str, list[type["BaseComponent"]]] = {}


class BaseComponent(BaseElement, metaclass=ABCMeta):
    classes: ClassVar[Sequence[str]] = []
    styles: ClassVar[GlobalStyles] = {}

    @property
    def theme(self) -> Theme:
        """Get the theme of the element."""
        if context_theme := self.context.get("theme"):
            if isinstance(context_theme, Theme):
                return context_theme
        return get_default_theme()

    def __init_subclass__(cls) -> None:
        COMPONENT_REGISTRY.setdefault(cls.__name__, [])
        COMPONENT_REGISTRY[cls.__name__].append(cls)

    def _add_classes(self, classes: list[str], element: BaseElement) -> None:
        if classes:
            element.attrs.setdefault("classes", [])  # type: ignore
            element.attrs["classes"].extend(classes)

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

    def to_html(self) -> str:
        dom: BaseElement | BaseComponent = self
        classes: list[str] = []

        while isinstance(dom, BaseComponent):
            classes += dom.classes
            context = dom.context
            dom = dom.render()
            dom.context.update(context)

        self._add_classes(classes, dom)
        return dom.to_html()

    @abstractmethod
    def render(self) -> BaseElement:
        """Render the component as an instance of :class:`BaseElement`."""


class Component(Element[TChildren, TAttrs], BaseComponent):
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


class ComponentStrict(ElementStrict[*TChildrenArgs, TAttrs], BaseComponent):
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


class Block(Component[AnyChildren, GlobalAttrs]):
    """Component rendering as a div."""

    @override
    def render(self) -> div:
        return div(*self.children, **self.attrs)


class Inline(Component[AnyChildren, GlobalAttrs]):
    """Component rendering as a span."""

    @override
    def render(self) -> span:
        return span(*self.children, **self.attrs)
