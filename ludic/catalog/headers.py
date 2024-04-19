from typing import override

from ludic.attrs import Attrs
from ludic.html import a, div, h1, h2, h3, h4, style
from ludic.types import Component, ComponentStrict

from .utils import text_to_kebab


class AnchorAttrs(Attrs):
    target: str


class Anchor(Component[str, AnchorAttrs]):
    """Component representing a clickable anchor."""

    classes = ["anchor"]
    styles = style.use(
        lambda theme: {
            "a.anchor": {
                "font-family": theme.fonts.serif,
                "font-size": theme.fonts.size.scale(2.5),
                "color": theme.colors.dark.lighten(0.5),
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


class WitchAnchorAttrs(Attrs, total=False):
    anchor: Anchor


class WithAnchor(ComponentStrict[h1 | h2 | h3 | h4 | str, WitchAnchorAttrs]):
    """Component which renders its content (header) with a clickable anchor."""

    classes = ["with-anchor"]
    styles = style.use(
        lambda theme: {
            ".with-anchor": {
                "display": "flex",
                "flex-wrap": "wrap",
                "justify-content": "flex-start",
            },
            ".with-anchor > h2 + a": {
                "margin-inline-start": theme.sizes.s,
            },
        }
    )

    @override
    def render(self) -> div:
        element: h1 | h2 | h3 | h4
        if isinstance(self.children[0], str):
            element = h1(self.children[0], id=text_to_kebab(self.children[0]))
        else:
            element = self.children[0]

        id = element.attrs.get("id", text_to_kebab(element.text))

        return div(
            element,
            (self.attrs["anchor"] if "anchor" in self.attrs else Anchor(target=id)),
        )


class H1(ComponentStrict[str, WitchAnchorAttrs]):
    """Component rendering as h1 with an optional clickable anchor."""

    @override
    def render(self) -> h1 | WithAnchor:
        header = h1(self.children[0], style={"font-family": self.theme.fonts.serif})
        if anchor := self.attrs.get("anchor"):
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h1.anchor:
            return WithAnchor(header)
        else:
            return header


class H2(ComponentStrict[str, WitchAnchorAttrs]):
    """Component rendering as h2 with an optional clickable anchor."""

    @override
    def render(self) -> h2 | WithAnchor:
        header = h2(self.children[0], style={"font-family": self.theme.fonts.serif})
        if anchor := self.attrs.get("anchor"):
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h2.anchor:
            return WithAnchor(header)
        else:
            return header


class H3(ComponentStrict[str, WitchAnchorAttrs]):
    """Component rendering as h3 with an optional clickable anchor."""

    @override
    def render(self) -> h3 | WithAnchor:
        header = h3(self.children[0], style={"font-family": self.theme.fonts.serif})
        if anchor := self.attrs.get("anchor"):
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h3.anchor:
            return WithAnchor(header)
        else:
            return header


class H4(ComponentStrict[str, WitchAnchorAttrs]):
    """Component rendering as h4 with an optional clickable anchor."""

    @override
    def render(self) -> h4 | WithAnchor:
        header = h4(self.children[0], style={"font-family": self.theme.fonts.serif})
        if anchor := self.attrs.get("anchor"):
            return WithAnchor(header, anchor=anchor)
        elif self.theme.headers.h4.anchor:
            return WithAnchor(header)
        else:
            return header
