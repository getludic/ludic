from collections.abc import Callable, Iterator
from typing import Self, Unpack, override
from ludicrous import (
    div,
    span,
    main,
    p,
    a,
    br,
    button,
    label,
    td,
    th,
    tr,
    thead,
    tbody,
    tfoot,
    table,
    li,
    ul,
    ol,
    dt,
    dd,
    dl,
    section,
    input,
    output,
    legend,
    option,
    optgroup,
    select,
    textarea,
    fieldset,
    form,
    img,
    svg,
    circle,
    line,
    path,
    polyline,
    b,
    i,
    s,
    u,
    strong,
    em,
    mark,
    del_,
    ins,
    header,
    big,
    small,
    code,
    pre,
    cite,
    blockquote,
    abbr,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    title,
    link,
    script,
    noscript,
    meta,
    head,
    body,
    footer,
    html,
    iframe,
    article,
    address,
    caption,
    col,
    colgroup,
    area,
    aside,
    source,
    audio,
    base,
    bdi,
    bdo,
    canvas,
    data,
    datalist,
    details,
    dfn,
    dialog,
    embed,
    figcaption,
    figure,
    hrgroup,
    hr,
    kbd,
    map,
    menu,
    meter,
    nav,
    object,
    param,
    picture,
    progress,
    q,
    rp,
    rt,
    ruby,
    samp,
    search,
    sub,
    summary,
    sup,
    template,
    time,
    track,
    var,
    video,
    wbr,
)

from .attrs import StyleAttrs
from .base import BaseElement
from .styles import (
    Theme,
    get_default_theme,
    format_styles,
    from_components,
    from_loaded,
)
from .styles.types import CSSProperties, GlobalStyles
from .format import format_attrs


class style(BaseElement, GlobalStyles):
    html_name = "style"

    children: tuple[GlobalStyles | Callable[[Theme], GlobalStyles] | str]
    attrs: StyleAttrs

    def __init__(
        self,
        styles: GlobalStyles | Callable[[Theme], GlobalStyles] | str,
        theme: Theme | None = None,
        **attrs: Unpack[StyleAttrs],
    ) -> None:
        super().__init__(styles, **attrs)

        if theme:
            self.context["theme"] = theme

    @classmethod
    def use(cls, styles: GlobalStyles | Callable[[Theme], GlobalStyles]) -> Self:
        return cls(styles)

    @classmethod
    def from_components(
        cls, *components: type[BaseElement], theme: Theme | None = None
    ) -> Self:
        return cls(from_components(*components, theme=theme), type="text/css")

    @classmethod
    def load(cls, cache: bool = False, theme: Theme | None = None) -> Self:
        return cls(from_loaded(cache=cache, theme=theme), type="text/css")

    def __getitem__(self, key: str | tuple[str, ...]) -> CSSProperties | GlobalStyles:
        return self.styles[key]

    def __iter__(self) -> Iterator[str | tuple[str, ...]]:
        return iter(self.styles.keys())

    def __len__(self) -> int:
        return len(self.styles)

    @property
    def theme(self) -> Theme:
        return self.context.get("theme", get_default_theme())

    @property
    def styles(self) -> GlobalStyles:
        if isinstance(self.children[0], str):
            return {}
        elif callable(self.children[0]):
            return self.children[0](self.theme)
        else:
            return self.children[0]

    @styles.setter
    def styles(self, value: GlobalStyles) -> None:
        self.children = (value,)

    def to_html(self) -> str:
        attributes = ""
        if formatted_attrs := format_attrs(type(self), self.attrs):
            attributes = f" {formatted_attrs}"

        if isinstance(self.children[0], str):
            css_styles = self.children[0]
        else:
            css_styles = format_styles(self.styles)

        return (
            f"<style{attributes}>\n"
            f"{css_styles}\n"
            f"</style>"
        )  # fmt: off


__all__ = (
    "div",
    "span",
    "main",
    "p",
    "a",
    "br",
    "button",
    "label",
    "td",
    "th",
    "tr",
    "thead",
    "tbody",
    "tfoot",
    "table",
    "li",
    "ul",
    "ol",
    "dt",
    "dd",
    "dl",
    "section",
    "input",
    "output",
    "legend",
    "option",
    "optgroup",
    "select",
    "textarea",
    "fieldset",
    "form",
    "img",
    "svg",
    "circle",
    "line",
    "path",
    "polyline",
    "b",
    "i",
    "s",
    "u",
    "strong",
    "em",
    "mark",
    "del_",
    "ins",
    "header",
    "big",
    "small",
    "code",
    "pre",
    "cite",
    "blockquote",
    "abbr",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "title",
    "link",
    "script",
    "noscript",
    "meta",
    "head",
    "body",
    "footer",
    "html",
    "iframe",
    "article",
    "address",
    "caption",
    "col",
    "colgroup",
    "area",
    "aside",
    "source",
    "audio",
    "base",
    "bdi",
    "bdo",
    "canvas",
    "data",
    "datalist",
    "details",
    "dfn",
    "dialog",
    "embed",
    "figcaption",
    "figure",
    "hrgroup",
    "hr",
    "kbd",
    "map",
    "menu",
    "meter",
    "nav",
    "object",
    "param",
    "picture",
    "progress",
    "q",
    "rp",
    "rt",
    "ruby",
    "samp",
    "search",
    "style",
    "sub",
    "summary",
    "sup",
    "template",
    "time",
    "track",
    "var",
    "video",
    "wbr",
)
