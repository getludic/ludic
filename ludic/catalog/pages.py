import json
from typing import override

from ludic.attrs import Attrs, NoAttrs
from ludic.base import BaseElement
from ludic.components import Component, ComponentStrict
from ludic.html import body, head, html, link, meta, script, style, title
from ludic.types import AnyChildren


class HtmlHeadAttrs(Attrs, total=False):
    title: str
    favicon: str
    charset: str
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
        if charset := self.attrs.get("charset", "utf-8"):
            elements.append(meta(charset=charset))
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
                "font-family": theme.fonts.primary,
                "font-size": theme.fonts.size,
                "color": theme.colors.dark,
                "overflow-wrap": "break-word",
                "margin": "0",
                "padding": "0",
                "line-height": theme.line_height,
            },
            "body": {
                "background-color": theme.colors.white,
            },
            ("html", "body", "div", "header", "nav", "main", "footer"): {
                "max-inline-size": "none",
            },
            # elements styling
            "h1": {
                "font-size": theme.headers.h1.size,
                "font-family": theme.fonts.secondary,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            "h2": {
                "font-size": theme.headers.h2.size,
                "font-family": theme.fonts.secondary,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            "h3": {
                "font-size": theme.headers.h3.size,
                "font-family": theme.fonts.secondary,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            "h4": {
                "font-size": theme.headers.h4.size,
                "font-family": theme.fonts.secondary,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            "h5": {
                "font-size": theme.headers.h5.size,
                "font-family": theme.fonts.secondary,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            "h6": {
                "font-size": theme.headers.h6.size,
                "font-family": theme.fonts.secondary,
                "line-height": round(theme.line_height * 0.9, 2),
            },
            "a": {
                "color": theme.colors.primary,
                "text-decoration": "none",
            },
            "a:hover": {
                "text-decoration": "underline",
            },
            "pre": {
                "overflow": "auto",
            },
            ("code", "pre", "pre *"): {
                "font-family": theme.fonts.monospace,
            },
            "dl": {
                "margin-block": "0",
            },
            "dl dd + dt": {
                "margin-block-start": theme.sizes.xs,
            },
            "dl dt + dd": {
                "margin-block-start": theme.sizes.xxxxs,
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
            ("ul > li + li", "ol > li + li", "li > * + *"): {
                "margin-block-start": theme.sizes.xxs,
            },
            "ul > li::marker": {
                "font-size": theme.fonts.size * 1.2,
            },
            ("img", "svg"): {
                "width": "100%",
            },
            # utilities
            ".text-align-center": {
                "text-align": "center !important",  # type: ignore[typeddict-item]
            },
            ".text-align-right": {
                "text-align": "right !important",  # type: ignore[typeddict-item]
            },
            ".text-align-left": {
                "text-align": "left !important",  # type: ignore[typeddict-item]
            },
            ".justify-space-between": {
                "justify-content": "space-between !important",  # type: ignore[typeddict-item]
            },
            ".justify-space-around": {
                "justify-content": "space-around !important",  # type: ignore[typeddict-item]
            },
            ".justify-space-evenly": {
                "justify-content": "space-evenly !important",  # type: ignore[typeddict-item]
            },
            ".justify-center": {
                "justify-content": "center !important",  # type: ignore[typeddict-item]
            },
            ".justify-end": {
                "justify-content": "end !important",  # type: ignore[typeddict-item]
            },
            ".justify-start": {
                "justify-content": "start !important",  # type: ignore[typeddict-item]
            },
            ".align-center": {
                "align-items": "center !important",  # type: ignore[typeddict-item]
            },
            ".align-end": {
                "align-items": "end !important",  # type: ignore[typeddict-item]
            },
            ".align-start": {
                "align-items": "start !important",  # type: ignore[typeddict-item]
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
            ".no-block-margin": {
                "margin-block": "0 !important",
            },
            ".no-block-padding": {
                "padding-block": "0 !important",
            },
            ".no-border": {
                "border": "none !important",
                "border-radius": "0 !important",
            },
            ".no-border-radius": {
                "border-radius": "0 !important",
            },
        }
    )

    @override
    def render(self) -> html:
        return html(
            self.children[0].render(),
            self.children[1].render(),
        )
