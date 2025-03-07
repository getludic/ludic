from typing import NotRequired, override

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name

    pygments_loaded = True
except ImportError:
    pygments_loaded = False

from ludic.attrs import Attrs, GlobalAttrs, HyperlinkAttrs
from ludic.components import Component, ComponentStrict
from ludic.html import a, code, p, pre, span, style
from ludic.types import (
    AnyChildren,
    PrimitiveChildren,
    Safe,
)

from .utils import add_line_numbers, remove_whitespaces


class LinkAttrs(Attrs):
    to: str
    external: NotRequired[bool]
    classes: NotRequired[list[str]]


class Link(ComponentStrict[PrimitiveChildren, LinkAttrs]):
    """Simple component simulating a link.

    The main difference between :class:`Link` and :class:`a` is that this component
    automatically adds the ``target="_blank"`` attribute to the link if the link
    points to an external resource. This can be overridden by setting the
    ``external`` attribute to ``False``.

    Another difference between :class:`Link` and :class:`a` is that this component
    expects only one primitive child, so it cannot contain any nested elements.

    Example usage:

        Link("Hello, World!", to="https://example.com")
    """

    @override
    def render(self) -> a:
        attrs: HyperlinkAttrs = {"href": self.attrs.get("to", "#")}
        if "classes" in self.attrs:
            attrs["classes"] = self.attrs["classes"]

        match self.attrs.get("external", "auto"):
            case True:
                attrs["target"] = "_blank"
            case False:
                pass
            case "auto":
                if str(attrs["href"]).startswith("http"):
                    attrs["target"] = "_blank"

        return a(self.children[0], **attrs)


class Paragraph(Component[AnyChildren, GlobalAttrs]):
    """Simple component simulating a paragraph.

    There is basically just an alias for the :class:`p` element.

    Example usage:

        Paragraph(f"Hello, {b("World")}!")
    """

    @override
    def render(self) -> p:
        return p(*self.children, **self.attrs)


class Code(Component[str, GlobalAttrs]):
    """Simple component simulating a code block.

    Example usage:

        Code("print('Hello, World!')")
    """

    classes = ["code"]
    styles = style.use(
        lambda theme: {
            ".code": {
                "background-color": theme.colors.light,
                "color": theme.colors.primary.darken(1),
                "padding": f"{theme.sizes.xxxxs * 0.3} {theme.sizes.xxxxs}",
                "border-radius": theme.rounding.less,
                "font-size": theme.fonts.size * 0.9,
            }
        }
    )

    @override
    def render(self) -> code:
        return code(*self.children, **self.attrs)


class CodeBlockAttrs(GlobalAttrs, total=False):
    language: str
    line_numbers: bool
    remove_whitespaces: bool


class CodeBlock(Component[str, CodeBlockAttrs]):
    """Simple component simulating a code block.

    Example usage:

        CodeBlock("print('Hello, World!')")
    """

    classes = ["code-block"]
    styles = style.use(
        lambda theme: {
            ".code-block": {
                "color": theme.code.color,
                "border": (
                    f"{theme.borders.thin} solid "
                    f"{theme.code.background_color.darken(1)}"
                ),
                "border-radius": theme.rounding.normal,
                "background-color": theme.code.background_color,
                "padding-block": theme.sizes.m,
                "padding-inline": theme.sizes.l,
                "font-size": theme.code.font_size,
            },
        }
    )

    def _get_line_number_span(self, line: str) -> str:
        return str(
            span(
                line,
                style={
                    "color": self.theme.code.line_number_color,
                    "user-select": "none",
                },
            )
        )

    @override
    def render(self) -> pre:
        content = "".join(self.children)
        append_line_numbers = self.attrs.get(
            "line_numbers", self.theme.code.line_numbers
        )

        if self.attrs.get("remove_whitespaces", True):
            content = remove_whitespaces(content)

        if pygments_loaded and (language := self.attrs.get("language")):
            lexer = get_lexer_by_name(language)
            formatter = HtmlFormatter(
                noclasses=True,
                nobackground=True,
                nowrap=True,
                style=self.theme.code.style,
            )
            highlighted_content = highlight(content, lexer, formatter)

            if append_line_numbers:
                highlighted_content = add_line_numbers(
                    highlighted_content, apply_fun=self._get_line_number_span
                )

            return pre(Safe(highlighted_content), **self.attrs_for(pre))
        else:
            return pre(content, **self.attrs_for(pre))
