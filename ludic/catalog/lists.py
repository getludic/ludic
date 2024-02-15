from collections.abc import Iterable
from typing import override

from ludic.attrs import GlobalAttrs
from ludic.base import Component
from ludic.html import dd, dl, dt
from ludic.types import PrimitiveChild, PrimitiveChildren

from .utils import attr_to_camel


class Key(Component[*PrimitiveChildren, GlobalAttrs]):
    @override
    def render(self) -> dt:
        return dt(*self.children, **self.attrs)


class Value(Component[*PrimitiveChildren, GlobalAttrs]):
    @override
    def render(self) -> dd:
        return dd(*self.children, **self.attrs)


class PairsAttrs(GlobalAttrs, total=False):
    items: Iterable[tuple[str, PrimitiveChild]]


class Pairs(Component[*tuple[Key | Value, ...], PairsAttrs]):
    @override
    def render(self) -> dl:
        from_items: list[Key | Value] = []
        for key, value in self.attrs.get("items", ()):
            from_items.append(Key(attr_to_camel(key)))
            from_items.append(Value(value))
        return dl(*from_items, *self.children, **self.attrs_for(dl))
