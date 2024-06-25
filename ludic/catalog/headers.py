from typing import override

from ludic.attrs import Attrs, GlobalAttrs
from ludic.components import Component, ComponentStrict
from ludic.html import a, div, h1, h2, h3, h4, style

from .utils import text_to_kebab


class AnchorAttrs(Attrs):
    target: str


class Anchor(Component[str, AnchorAttrs]):
    """Component representing a clickable anchor."""

    classes = ["anchor"]
    styles = style.use(
        lambda theme: {
            "a.anchor": {
                "font-family": theme.fonts.secondary,
                "color": theme.colors.light.darken(1),
                "text-decoration": "none",
            },
            "a.anchor:hover": {
                "color": theme.colors.dark,
                "text-decoration": "none",
            },
        }
    )

    @override
    def render(self) -> a:
        return a(
            self.children[0] if self.children else "#", href=f"#{self.attrs["target"]}"
        )


class WithAnchorAttrs(GlobalAttrs, total=False):
    anchor: Anchor | bool


class WithAnchor(ComponentStrict[h1 | h2 | h3 | h4 | str, WithAnchorAttrs]):
    """Component which renders its content (header) with a clickable anchor."""

    classes = ["with-anchor"]
    styles = style.use(
        lambda theme: {
            ".with-anchor": {
                "display": "flex",
                "flex-wrap": "wrap",
                "justify-content": "flex-start",
            },
            ".with-anchor > h1 + a": {
                "margin-inline-start": theme.sizes.m,
                "font-size": theme.headers.h1.size,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            ".with-anchor > h2 + a": {
                "margin-inline-start": theme.sizes.s,
                "font-size": theme.headers.h2.size,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            ".with-anchor > h3 + a": {
                "margin-inline-start": theme.sizes.xs,
                "font-size": theme.headers.h3.size,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            ".with-anchor > h4 + a": {
                "margin-inline-start": theme.sizes.xxs,
                "font-size": theme.headers.h4.size,
                "line-height": round(theme.line_height * 0.9, 2),
            },
        }
    )

    @override
    def render(self) -> div:
        element: h1 | h2 | h3 | h4
        if isinstance(self.children[0], h1 | h2 | h3 | h4):
            element = self.children[0]
        else:
            element = h1(*self.children)

        element.attrs.setdefault("id", text_to_kebab(element.text))
        id = element.attrs["id"]

        return div(
            element,
            (
                self.attrs["anchor"]
                if isinstance(self.attrs.get("anchor"), Anchor)
                else Anchor(target=id)
            ),
        )


class H1(ComponentStrict[str, WithAnchorAttrs]):
    """Component rendering as h1 with an optional clickable anchor."""

    @override
    def render(self) -> h1 | WithAnchor:
        header = h1(*self.children, **self.attrs_for(h1))
        anchor = self.attrs.get("anchor")
        if anchor:
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h1.anchor and anchor is not False:
            return WithAnchor(header)
        else:
            return header


class H2(ComponentStrict[str, WithAnchorAttrs]):
    """Component rendering as h2 with an optional clickable anchor."""

    @override
    def render(self) -> h2 | WithAnchor:
        header = h2(*self.children, **self.attrs_for(h2))
        anchor = self.attrs.get("anchor")
        if anchor:
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h2.anchor and anchor is not False:
            return WithAnchor(header)
        else:
            return header


class H3(ComponentStrict[str, WithAnchorAttrs]):
    """Component rendering as h3 with an optional clickable anchor."""

    @override
    def render(self) -> h3 | WithAnchor:
        header = h3(*self.children, **self.attrs_for(h3))
        anchor = self.attrs.get("anchor")
        if anchor:
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h3.anchor and anchor is not False:
            return WithAnchor(header)
        else:
            return header


class H4(ComponentStrict[str, WithAnchorAttrs]):
    """Component rendering as h4 with an optional clickable anchor."""

    @override
    def render(self) -> h4 | WithAnchor:
        header = h4(*self.children, **self.attrs_for(h4))
        anchor = self.attrs.get("anchor")
        if anchor:
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h4.anchor and anchor is not False:
            return WithAnchor(header)
        else:
            return header
