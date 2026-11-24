import json
from typing import override

from ludic.attrs import Attrs, GlobalAttrs, NoAttrs
from ludic.base import BaseElement
from ludic.components import Component, ComponentStrict
from ludic.html import body, button, head, html, link, meta, script, span, style, title
from ludic.styles.themes import Theme
from ludic.types import AnyChildren, JavaScript, Safe

DARK_STYLES_ID = "ludic-dark-styles"
"""The id of the style element with the dark theme, see :class:`Head`."""

COLOR_SCHEME_KEY = "ludic-color-scheme"
"""The localStorage key that remembers the color scheme picked by the visitor."""

_RESTORE_COLOR_SCHEME = JavaScript(
    "(() => {"
    f"const styles = document.getElementById({json.dumps(DARK_STYLES_ID)});"
    "let scheme = null;"
    f"try {{ scheme = localStorage.getItem({json.dumps(COLOR_SCHEME_KEY)}); }}"
    " catch {}"
    'if (styles && scheme) styles.media = scheme === "dark" ? "all" : "not all";'
    "})();"
)

_TOGGLE_COLOR_SCHEME = (
    f"const styles = document.getElementById({json.dumps(DARK_STYLES_ID)});"
    "if (!styles) return;"
    'const dark = styles.media === "all" || (styles.media !== "not all"'
    ' && matchMedia("(prefers-color-scheme: dark)").matches);'
    'styles.media = dark ? "not all" : "all";'
    f"try {{ localStorage.setItem({json.dumps(COLOR_SCHEME_KEY)},"
    ' dark ? "light" : "dark"); } catch {}'
)

_MOON_ICON = Safe(
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true">'
    '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>'
)

_SUN_ICON = Safe(
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true">'
    '<circle cx="12" cy="12" r="4"/>'
    '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2'
    'M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
)


class HtmlHeadAttrs(Attrs, total=False):
    title: str
    favicon: str
    charset: str
    load_styles: bool
    htmx_config: dict[str, str]
    theme: Theme
    dark_theme: Theme


class HtmlBodyAttrs(Attrs, total=False):
    htmx_path: str
    htmx_enabled: bool
    htmx_version: str


class Head(Component[AnyChildren, HtmlHeadAttrs]):
    """The head of an HTML page with the styles of all loaded components.

    The styles are rendered with ``theme``, or with the default theme. With
    ``dark_theme``, the head also renders the styles with the dark theme, which
    apply when the visitor's system is in dark mode. A
    :class:`ColorSchemeToggle` lets the visitor switch the scheme by hand,
    and the choice is remembered in the browser.

    The two themes must have different names, because the styles are cached
    per theme name. Inline styles computed from ``self.theme`` in a component
    use the default theme in both schemes.

    Example usage:

        Head(title="My App", theme=LightTheme(), dark_theme=DarkTheme())
    """

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
            elements.append(style.load(cache=True, theme=self.attrs.get("theme")))
            if dark_theme := self.attrs.get("dark_theme"):
                elements.append(
                    style.load(
                        cache=True,
                        theme=dark_theme,
                        media="(prefers-color-scheme: dark)",
                        id=DARK_STYLES_ID,
                    )
                )
                elements.append(script(_RESTORE_COLOR_SCHEME))

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
            "html": {
                "color-scheme": theme.color_scheme,
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
                "text-align": "center !important",  # type: ignore[dict-item]
            },
            ".text-align-right": {
                "text-align": "right !important",  # type: ignore[dict-item]
            },
            ".text-align-left": {
                "text-align": "left !important",  # type: ignore[dict-item]
            },
            ".justify-space-between": {
                "justify-content": "space-between !important",  # type: ignore[dict-item]
            },
            ".justify-space-around": {
                "justify-content": "space-around !important",  # type: ignore[dict-item]
            },
            ".justify-space-evenly": {
                "justify-content": "space-evenly !important",  # type: ignore[dict-item]
            },
            ".justify-center": {
                "justify-content": "center !important",  # type: ignore[dict-item]
            },
            ".justify-end": {
                "justify-content": "end !important",  # type: ignore[dict-item]
            },
            ".justify-start": {
                "justify-content": "start !important",  # type: ignore[dict-item]
            },
            ".align-center": {
                "align-items": "center !important",  # type: ignore[dict-item]
            },
            ".align-end": {
                "align-items": "end !important",  # type: ignore[dict-item]
            },
            ".align-start": {
                "align-items": "start !important",  # type: ignore[dict-item]
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


class ColorSchemeToggle(Component[AnyChildren, GlobalAttrs]):
    """A button switching between the light and the dark theme of the page.

    It works with a :class:`Head` that has a ``dark_theme``. Without children,
    the button shows a moon in the light theme and a sun in the dark one.

    Example usage:

        ColorSchemeToggle(aria_label="Switch between light and dark theme")
    """

    classes = ["color-scheme-toggle"]
    styles = style.use(
        lambda theme: {
            ".color-scheme-toggle": {
                "display": "inline-flex",
                "align-items": "center",
                "justify-content": "center",
                "padding": theme.sizes.xxxs,
                "border": "none",
                "border-radius": theme.rounding.normal,
                "background": "none",
                "color": theme.colors.dark,
                "cursor": "pointer",
            },
            ".color-scheme-toggle:hover": {
                "background-color": theme.colors.light,
            },
            ".color-scheme-toggle svg": {
                "width": "1.25em",
                "height": "1.25em",
            },
            ".color-scheme-toggle .when-light": {
                "display": "inline-flex" if theme.color_scheme == "light" else "none",
            },
            ".color-scheme-toggle .when-dark": {
                "display": "inline-flex" if theme.color_scheme == "dark" else "none",
            },
        }
    )

    @override
    def render(self) -> button:
        self.attrs.setdefault("aria_label", "Switch between light and dark theme")
        self.attrs.setdefault("title", self.attrs["aria_label"])
        content = self.children or (
            span(_MOON_ICON, classes=["when-light"]),
            span(_SUN_ICON, classes=["when-dark"]),
        )
        return button(
            *content,
            type="button",
            on_click=_TOGGLE_COLOR_SCHEME,
            **self.attrs,
        )
