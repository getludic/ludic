from typing import override

from ludic.attrs import GlobalAttrs, OlAttrs
from ludic.components import Component
from ludic.html import li, ol, ul
from ludic.types import AnyChildren


class Item(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating an item in a list.

    Example usage:

        Item("Item 1")
    """

    @override
    def render(self) -> li:
        return li(*self.children, **self.attrs)


class List(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating a list.

    There is basically just an alias for the :class:`ul` element
    without the requirement to pass `li` as children.

    Example usage:

        List("Item 1", "Item 2")
        List(Item("Item 1"), Item("Item 2"))
    """

    formatter_fstring_wrap_in = Item

    @override
    def render(self) -> ul:
        children = (
            child if isinstance(child, Item) else Item(child) for child in self.children
        )
        return ul(*children, **self.attrs_for(ul))


class NumberedList(Component[AnyChildren, OlAttrs]):
    """Simple component simulating a numbered list.

    There is basically just an alias for the :class:`ol` element
    without the requirement to pass `li` as children.

    Example usage:

        NumberedList("Item 1", "Item 2")
        NumberedList(Item("Item 1"), Item("Item 2"))
    """

    formatter_fstring_wrap_in = Item

    @override
    def render(self) -> ol:
        children = (
            child if isinstance(child, Item) else Item(child) for child in self.children
        )
        return ol(*children, **self.attrs_for(ol))
