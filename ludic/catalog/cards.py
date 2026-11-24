from typing import override

from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import a, div, style
from ludic.types import AnyChildren


class CardAttrs(GlobalAttrs, total=False):
    to: str


class Card(Component[AnyChildren, CardAttrs]):
    """A framed box for a short piece of content, such as a feature.

    The children are stacked with a small space between them. With ``to``,
    the whole card is a link. Put cards in a :class:`ludic.catalog.layouts.Grid`
    to lay them out in responsive columns.

    Example usage:

        Grid(
            Card(h3("Typed"), Paragraph("Mypy checks the markup.")),
            Card(h3("Fast"), Paragraph("Renders plain strings."), to="/docs"),
        )
    """

    classes = ["card"]
    styles = style.use(
        lambda theme: {
            ".card": {
                "display": "flex",
                "flex-direction": "column",
                "gap": theme.sizes.xs,
                "padding": theme.sizes.l,
                "border": f"{theme.borders.thin} solid {theme.colors.light.darken(1)}",
                "border-radius": theme.rounding.more,
                "background-color": theme.colors.white,
                "color": theme.colors.dark,
            },
            ".card > *": {
                "margin": "0",
            },
            "a.card": {
                "text-decoration": "none",
                "transition": "border-color 0.15s, transform 0.15s",
            },
            ("a.card:hover", "a.card:focus-visible"): {
                "border-color": theme.colors.primary,
                "text-decoration": "none",
                "transform": "translateY(-2px)",
            },
            "@media (prefers-reduced-motion: reduce)": {
                "a.card": {
                    "transition": "none",
                },
                "a.card:hover": {
                    "transform": "none",
                },
            },
        }
    )

    @override
    def render(self) -> div | a:
        if to := self.attrs.get("to"):
            return a(*self.children, href=to, **self.attrs_for(a))
        return div(*self.children, **self.attrs_for(div))
