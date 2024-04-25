import json
from typing import override

from ludic.attrs import Attrs, NoAttrs
from ludic.html import body, head, html, link, meta, script, style, title
from ludic.types import AnyChildren, BaseElement, Component, ComponentStrict


class HtmlHeadAttrs(Attrs, total=False):
    title: str
    favicon: str
    load_styles: bool
    htmx_config: dict[str, str]


class HtmlBodyAttrs(Attrs, total=False):
    htmx_path: str
    htmx_enabled: bool
    htmx_version: str


class Head(Component[AnyChildren, HtmlHeadAttrs]):
    @override
    def render(self) -> head:
        elements: list[BaseElement] = [title(self.attrs.get("title", "Ludic App"))]

        if favicon := self.attrs.get("favicon"):
            elements.append(link(rel="icon", href=favicon, type="image/x-icon"))
        if config := self.attrs.get("htmx_config", {"defaultSwapStyle": "outerHTML"}):
            elements.append(meta(name="htmx-config", content=json.dumps(config)))
        if self.attrs.get("load_styles", True):
            elements.append(style.load(cache=True))

        return head(*elements, *self.children)


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
                "font-family": theme.fonts.serif,
            },
            "h2": {
                "font-size": theme.headers.h2.size,
                "font-family": theme.fonts.serif,
            },
            "h3": {
                "font-size": theme.headers.h3.size,
                "font-family": theme.fonts.serif,
            },
            "h4": {
                "font-size": theme.headers.h4.size,
                "font-family": theme.fonts.serif,
            },
            "h5": {
                "font-size": theme.headers.h5.size,
                "font-family": theme.fonts.serif,
            },
            "h6": {
                "font-size": theme.headers.h6.size,
                "font-family": theme.fonts.serif,
            },
            "a": {
                "color": theme.colors.primary.darken(2),
                "text-decoration": "none",
            },
            "a:hover": {
                "text-decoration": "underline",
            },
            "pre": {
                "overflow": "auto",
            },
            ("code", "pre", "pre *"): {
                "font-family": theme.fonts.mono,
                "font-size": theme.fonts.size * 0.95,
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
                "padding-inline-start": theme.sizes.xxl,
            },
            ("ul > li + li", "ol > li + li", "li > ul", "li > ol"): {
                "margin-block-start": theme.sizes.xxxxs,
            },
            ("img", "svg"): {
                "width": "100%",
            },
            "button": {
                "line-height": 1,
            },
            # utilities
            ".text-align-center": {
                "text-align": "center",
            },
            ".text-align-right": {
                "text-align": "right",
            },
            ".text-align-left": {
                "text-align": "left",
            },
            ".no-border": {
                "border": "none !important",
                "border-radius": "0 !important",
            },
            ".no-padding": {
                "padding": "0 !important",
            },
            ".no-inline-padding": {
                "padding-inline": "0 !important",
            },
            ".no-margin": {
                "margin": "0 !important",
            },
            ".no-inline-margin": {
                "margin-inline": "0 !important",
            },
        }
    )

    @override
    def render(self) -> html:
        return html(
            self.children[0].render(),
            self.children[1].render(),
        )
