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
        # A blank line ("\n\n") in a text child starts a new paragraph.
        paragraphs: list[list[AnyChildren]] = [[]]
        for child in self.children:
            if isinstance(child, str) and "\n\n" in child:
                for index, text in enumerate(child.split("\n\n")):
                    if index > 0:
                        paragraphs.append([])
                    if text:
                        # Keep the type of the text, e.g. Safe stays Safe.
                        paragraphs[-1].append(type(child)(text))
            else:
                paragraphs[-1].append(child)

        children: list[BaseElement] = [
            blockquote(*(p(*paragraph) for paragraph in paragraphs if paragraph))
        ]
        if source_url := self.attrs.get("source_url"):
            source_text = self.attrs.get("source_text", "Source: ")
            children.append(footer(source_text, a(source_url, href=source_url)))
        return div(*children)
