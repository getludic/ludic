from typing import override

from ludic.attrs import GlobalAttrs
from ludic.html import li, ol, ul
from ludic.types import AnyChildren, Component


class List(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating a list.

    There is basically just an alias for the :class:`ul` element
    without the requirement to pass `li` as children.

    Example usage:

        List("Item 1", "Item 2")
    """

    @override
    def render(self) -> ul:
        return ul(
            *(child if isinstance(child, li) else li(child) for child in self.children),
            **self.attrs,
        )


class NumberedList(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating a numbered list.

    There is basically just an alias for the :class:`ol` element
    without the requirement to pass `li` as children.

    Example usage:

        NumberedList("Item 1", "Item 2")
    """

    @override
    def render(self) -> ol:
        return ol(
            *(child if isinstance(child, li) else li(child) for child in self.children),
            **self.attrs,
        )
