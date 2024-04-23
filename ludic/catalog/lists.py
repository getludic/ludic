from typing import override

from ludic.attrs import GlobalAttrs
from ludic.html import li, ol, ul
from ludic.types import AnyChildren, Component


class ListAttrs(GlobalAttrs, total=False):
    items: list[AnyChildren]


class Item(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating an item in a list.

    Example usage:

        Item("Item 1")
    """

    @override
    def render(self) -> li:
        return li(*self.children, **self.attrs)


class List(Component[Item, ListAttrs]):
    """Simple component simulating a list.

    There is basically just an alias for the :class:`ul` element
    without the requirement to pass `li` as children.

    Example usage:

        List(Item("Item 1"), Item("Item 2"))
    """

    @override
    def render(self) -> ul:
        if items := self.attrs.get("items"):
            children = tuple(map(Item, items))
        else:
            children = self.children
        return ul(*children, **self.attrs)


class NumberedList(Component[Item, ListAttrs]):
    """Simple component simulating a numbered list.

    There is basically just an alias for the :class:`ol` element
    without the requirement to pass `li` as children.

    Example usage:

        NumberedList(Item("Item 1"), Item("Item 2"))
    """

    @override
    def render(self) -> ol:
        if items := self.attrs.get("items"):
            children = tuple(map(Item, items))
        else:
            children = self.children
        return ol(*children, **self.attrs)
