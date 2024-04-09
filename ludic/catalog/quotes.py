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
                "margin-bottom": "20px",  # type: ignore
                "blockquote": {
                    "background-color": theme.colors.light,
                    "border-left": f"8px solid {theme.colors.light.darken(0.1)}",
                    "margin": "0",
                    "margin-bottom": "10px",
                    "padding": "15px",
                },
                "blockquote p": {
                    "font-size": theme.fonts.sizes.large,
                    "margin-bottom": "10px",
                },
                "footer": {
                    "font-size": theme.fonts.sizes.medium,
                    "margin-top": "10px",
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
            blockquote(*map(p, self.children[0].split("\n")))
        ]
        if source_url := self.attrs.get("source_url"):
            source_text = self.attrs.get("source_text", "Source: ")
            children.append(footer(source_text, a(source_url, href=source_url)))
        return div(*children)
