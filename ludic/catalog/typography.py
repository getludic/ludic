from typing import override

from ludic.attrs import GlobalAttrs
from ludic.html import a, p
from ludic.types import (
    AnyChildren,
    Attrs,
    Component,
    ComponentStrict,
    PrimitiveChildren,
)


class LinkAttrs(Attrs):
    to: str


class Link(ComponentStrict[PrimitiveChildren, LinkAttrs]):
    """Simple component simulating a link.

    The difference between :class:`Link` and :class:`a` is that this component
    expects only one primitive child, so it cannot contain any nested elements.

    Example usage:

        Link("Hello, World!", to="https://example.com")
    """

    @override
    def render(self) -> a:
        return a(self.children[0], href=self.attrs["to"], **self.attrs_for(a))


class Paragraph(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating a paragraph.

    There is basically just an alias for the :class:`p` element.

    Example usage:

        Paragraph(f"Hello, {b("World")}!")
    """

    @override
    def render(self) -> p:
        return p(*self.children, **self.attrs)
