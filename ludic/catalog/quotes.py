from typing import override

from ludic.attrs import Attrs
from ludic.base import BaseElement
from ludic.components import ComponentStrict
from ludic.html import a, blockquote, div, footer, p, style
from ludic.types import AnyChildren


class QuoteAttrs(Attrs, total=False):
    source_url: str
    source_text: str


class Quote(ComponentStrict[str, QuoteAttrs]):
    """Simple component rendering as the HTML ``blockquote`` element."""

    classes = ["quote"]
    styles = style.use(
        lambda theme: {
            ".quote": {
                "blockquote": {
                    "background-color": theme.colors.light,
                    "border-left": (
                        f"{theme.borders.thick} solid {theme.colors.light.darken(1)}"
                    ),
                    "margin-bottom": theme.sizes.xxs,
                    "padding": f"{theme.sizes.l} {theme.sizes.m}",
                },
                "blockquote p": {
                    "font-size": theme.fonts.size,
                },
                "blockquote code": {
                    "background-color": theme.colors.white,
                },
                "footer": {
                    "font-size": theme.fonts.size * 0.9,
                    "color": theme.colors.dark.lighten(1),
                },
                "footer a": {
                    "text-decoration": "none",
                    "color": theme.colors.dark.darken(1),
                },
                "footer a:hover": {
                    "text-decoration": "underline",
                },
            }
        }
    )

    @override
    def render(self) -> div:
        p_children: list[BaseElement] = []
        current_children: list[AnyChildren] = []

        for child in self.children:
            if isinstance(child, str) and "\n\n" in child:
                p_children.append(p(*current_children))
                current_children = []
            else:
                current_children.append(child)

        children: list[BaseElement] = [blockquote(*p_children, p(*current_children))]
        if source_url := self.attrs.get("source_url"):
            source_text = self.attrs.get("source_text", "Source: ")
            children.append(footer(source_text, a(source_url, href=source_url)))
        return div(*children)
