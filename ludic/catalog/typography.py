from typing import override

from ludic.attrs import GlobalAttrs
from ludic.html import a, p, style
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

    classes = ["link"]
    styles = style.use(
        lambda theme: {
            "a.link": {
                "font-size": theme.fonts.sizes.medium,
                "color": theme.colors.primary.darken(0.3),
                "text-decoration": "none",
            },
            "a.link:hover": {
                "text-decoration": "underline",
            },
        }
    )

    @override
    def render(self) -> a:
        return a(self.children[0], href=self.attrs["to"])


class Paragraph(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating a paragraph.

    There is basically just an alias for the :class:`p` element.

    Example usage:

        Paragraph(f"Hello, {b("World")}!")
    """

    classes = ["paragraph"]
    styles = style.use(
        lambda theme: {"p.paragraph": {"font-size": theme.fonts.sizes.medium}}
    )

    @override
    def render(self) -> p:
        return p(*self.children, **self.attrs)
