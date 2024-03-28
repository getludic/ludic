from typing import override

from ludic.attrs import Attrs
from ludic.html import a, blockquote, div, footer, p, style
from ludic.types import BaseElement, ComponentStrict


class QuoteAttrs(Attrs, total=False):
    source_url: str


class Quote(ComponentStrict[str, QuoteAttrs]):
    """Simple component rendering as the HTML ``blockquote`` element."""

    classes = ["quote"]
    styles = style.use(
        lambda theme: {
            ".quote": {
                "margin-bottom": "40px",  # type: ignore
                "blockquote": {
                    "background-color": theme.colors.light,
                    "border-left": f"8px solid {theme.colors.light.darken(0.1)}",
                    "margin": "0",
                    "margin-bottom": "20px",
                    "padding": "15px",
                },
                "blockquote p": {
                    "font-size": "1.1em",
                    "margin-bottom": "10px",
                },
                "footer": {
                    "font-size": "1.25em",
                    "margin-top": "10px",
                    "color": theme.colors.dark.lighten(1),
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
            children.append(footer("Source: ", a(source_url, href=source_url)))
        return div(*children)
