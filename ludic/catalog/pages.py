from typing import override

from ludic.attrs import Attrs, NoAttrs
from ludic.html import body, head, html, script, style, title
from ludic.types import AnyChildren, Component, ComponentStrict


class HtmlHeadAttrs(Attrs, total=False):
    title: str


class HtmlBodyAttrs(Attrs, total=False):
    htmx_path: str
    htmx_enabled: bool
    htmx_version: str


class Head(Component[AnyChildren, HtmlHeadAttrs]):
    @override
    def render(self) -> head:
        return head(
            title(self.attrs.get("title", "Ludic App")),
            style.load(cache=True),
            *self.children,
        )


class Body(Component[AnyChildren, HtmlBodyAttrs]):
    @override
    def render(self) -> body:
        scripts = []
        if htmx_path := self.attrs.get("htmx_path"):
            scripts.append(script(src=htmx_path))
        elif self.attrs.get("htmx_enabled", "htmx_version" in self.attrs):
            htmx_version = self.attrs.get("htmx_version", "latest")
            scripts.append(script(src=f"https://unpkg.com/htmx.org@{htmx_version}"))
        return body(*self.children, *scripts)


class HtmlPage(ComponentStrict[Head, Body, NoAttrs]):
    styles = style.use(
        lambda theme: {
            # global styling
            "*": {
                "box-sizing": "border-box",
                "max-inline-size": theme.measure,
                "font-family": theme.fonts.plain,
                "font-size": theme.fonts.size,
                "color": theme.colors.dark,
                "overflow-wrap": "break-word",
                "margin": "0",
                "padding": "0",
                "line-height": theme.line_height,
            },
            ("html", "body", "div", "header", "nav", "main", "footer"): {
                "max-inline-size": "none",
            },
            # elements styling
            "h1": {
                "font-size": theme.headers.h1.size,
            },
            "h2": {
                "font-size": theme.headers.h2.size,
            },
            "h3": {
                "font-size": theme.headers.h3.size,
            },
            "h4": {
                "font-size": theme.headers.h4.size,
            },
            "h5": {
                "font-size": theme.headers.h5.size,
            },
            "h6": {
                "font-size": theme.headers.h6.size,
            },
            "a": {
                "color": theme.colors.primary.darken(0.3),
                "text-decoration": "none",
            },
            "a:hover": {
                "text-decoration": "underline",
            },
            "dl": {
                "margin-block": "0",
            },
            "dl dt": {
                "margin-block-start": theme.sizes.xxs,
            },
            "dl dd": {
                "margin-block-start": theme.sizes.xxxs,
            },
            "dt": {
                "font-weight": "bold",
            },
            "dd": {
                "margin-left": "0",
            },
            ("ul", "ol"): {
                "padding-inline-start": theme.sizes.xl,
            },
            ("img", "svg"): {
                "width": "100%",
            },
            "button": {
                "line-height": theme.line_height - 0.2,
            },
            # utilities
            ".text-align-center": {
                "text-align": "center",
            },
        }
    )

    @override
    def render(self) -> html:
        return html(
            self.children[0].render(),
            self.children[1].render(),
        )
