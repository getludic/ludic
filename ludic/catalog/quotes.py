from typing import override

from ludic.attrs import Attrs
from ludic.html import a, blockquote, div, footer, p, style
from ludic.types import BaseElement, ComponentStrict


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
                        f"{theme.borders.thick} solid {theme.colors.light.darken(0.05)}"
                    ),
                    "margin-bottom": theme.sizes.xxs,
                    "padding": f"{theme.sizes.l} {theme.sizes.m}",
                },
                "blockquote p": {
                    "font-size": theme.fonts.size,
                },
                "footer": {
                    "font-size": theme.fonts.size.scale(0.9),
                    "color": theme.colors.dark.lighten(0.5),
                },
                "footer a": {
                    "text-decoration": "none",
                    "color": theme.colors.dark.darken(0.5),
                },
                "footer a:hover": {
                    "text-decoration": "underline",
                },
            }
        }
    )

    @override
    def render(self) -> div:
        children: list[BaseElement] = [
            blockquote(*map(p, self.children[0].split("\n\n")))
        ]
        if source_url := self.attrs.get("source_url"):
            source_text = self.attrs.get("source_text", "Source: ")
            children.append(footer(source_text, a(source_url, href=source_url)))
        return div(*children)
