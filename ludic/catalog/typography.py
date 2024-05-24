from typing import NotRequired, override

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name

    pygments_loaded = True
except ImportError:
    pygments_loaded = False

from ludic.attrs import GlobalAttrs, HyperlinkAttrs
from ludic.html import a, code, p, pre, style
from ludic.types import (
    AnyChildren,
    Attrs,
    Component,
    ComponentStrict,
    PrimitiveChildren,
    Safe,
)

from .utils import remove_whitespaces


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
                "padding": f"{theme.sizes.xxxxs * 0.3} {theme.sizes.xxxs}",
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
                "background-color": theme.code.background_color,
                "padding-block": theme.sizes.l,
                "padding-inline": theme.sizes.xxl,
                "font-size": theme.fonts.size * 0.9,
            },
        }
    )

    @override
    def render(self) -> pre:
        content = "".join(self.children)

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
            block = Safe(highlight(content, lexer, formatter))
            return pre(block, **self.attrs_for(pre))
        else:
            return pre(content, **self.attrs_for(pre))
