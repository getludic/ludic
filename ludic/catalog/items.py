from collections.abc import Iterable
from typing import override

from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import dd, dl, dt
from ludic.types import PrimitiveChildren

from .utils import attr_to_camel


class Key(Component[PrimitiveChildren, GlobalAttrs]):
    """Simple component rendering as the HTML ``dt`` element."""

    @override
    def render(self) -> dt:
        return dt(*self.children, **self.attrs)


class Value(Component[PrimitiveChildren, GlobalAttrs]):
    """Simple component rendering as the HTML ``dd`` element."""

    @override
    def render(self) -> dd:
        return dd(*self.children, **self.attrs)


class PairsAttrs(GlobalAttrs, total=False):
    """Attributes of the component ``Pairs``."""

    items: Iterable[tuple[str, PrimitiveChildren]]


class Pairs(Component[Key | Value, PairsAttrs]):
    """Simple component rendering as the HTML ``dl`` element.

    Example usage:

        Pairs(
            Key("Name"),
            Value("John"),
            Key("Age"),
            Value(42),
        )

    The components accepts the ``items`` attribute, which allow the following usage:

        Pairs(
            items=[("name", "John"), ("age", 42)],
        )

    Or alternatively:

        Pairs(
            items={"name": "John", "age": 42}.items(),
        )
    """

    @override
    def render(self) -> dl:
        from_items: list[Key | Value] = []

        for key, value in self.attrs.get("items", ()):
            from_items.append(Key(attr_to_camel(key)))
            from_items.append(Value(value))

        return dl(*from_items, *self.children, **self.attrs_for(dl))
