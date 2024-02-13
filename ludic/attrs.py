from typing import Literal, TypedDict

from .base import BaseAttrs
from .css import CSSProperties


class NoAttrs(BaseAttrs):
    """Placeholder for element with no attributes."""


_HtmlAttrsAlt = TypedDict(
    "_HtmlAttrsAlt",
    {
        "class": str,
    },
    total=False,
)

_LabelAttrsAlt = TypedDict(
    "_LabelAttrsAlt",
    {
        "for": str,
    },
    total=False,
)


class HtmlAttrs(BaseAttrs, _HtmlAttrsAlt, total=False):
    """Common attributes for HTML elements."""

    id: str
    accesskey: str
    class_: str
    contenteditable: Literal["true", "false"]
    dir: Literal["ltr", "rtl"]
    draggable: Literal["true", "false"]
    enterkeyhint: Literal["enter", "done", "go", "next", "previous", "search", "send"]
    hidden: Literal["true", "false"]
    id: str
    inert: bool
    inputmode: Literal[
        "none", "text", "search", "tel", "url", "email", "numeric", "decimal"
    ]
    lang: str
    popover: bool
    spellcheck: Literal["true", "false"]
    style: CSSProperties
    tabindex: int
    title: str
    translate: Literal["yes", "no"]


_HtmxAttrsAlt = TypedDict(
    "_HtmxAttrsAlt",
    {
        "hx-get": str,
        "hx-post": str,
        "hx-put": str,
        "hx-delete": str,
        "hx-patch": str,
        "hx-trigger": str,
        "hx-target": str,
        "hx-swap": Literal[
            "innerHTML",
            "outerHTML",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ],
    },
    total=False,
)


class HtmxAttrs(BaseAttrs, _HtmxAttrsAlt, total=False):
    """HTMX attributes for HTML elements.

    See: https://htmx.org/
    """

    hx_get: str
    hx_post: str
    hx_put: str
    hx_delete: str
    hx_patch: str

    hx_trigger: str
    hx_target: str
    hx_swap: Literal[
        "innerHTML",
        "outerHTML",
        "beforebegin",
        "afterbegin",
        "beforeend",
        "afterend",
        "delete",
        "none",
    ]


class EventAttrs(BaseAttrs, total=False):
    """Event Attributes for HTML elements."""

    onafterprint: str
    onbeforeprint: str
    onbeforeunload: str
    onerror: str
    onhashchange: str
    onload: str
    onmessage: str
    onoffline: str
    ononline: str
    onpagehide: str
    onpageshow: str
    onpopstate: str
    onresize: str
    onstorage: str
    onunhandledrejection: str
    onunload: str


class HtmlAndEventAttrs(HtmlAttrs, EventAttrs, total=False):
    """Common HTML and event attributes."""


class GlobalAttrs(HtmxAttrs, HtmlAndEventAttrs, total=False):
    """Global attributes for HTML elements."""


class HtmlTagAttrs(BaseAttrs, total=False):
    xmlns: str


class MetaAttrs(HtmlAttrs, total=False):
    name: str
    content: str
    charset: str


class StyleAttrs(HtmlAndEventAttrs, total=False):
    media: str
    type: Literal["text/css"]


class ScriptAttrs(HtmlAttrs, total=False):
    async_: bool
    crossorigin: Literal["anonymous", "use-credentials"]
    defer: bool
    integrity: str
    nomodule: bool
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    src: str
    type: str


class HeadLinkAttrs(HtmlAttrs, total=False):
    rel: Literal["canonical", "alternate", "stylesheet"]
    crossorigin: Literal["anonymous", "use-credentials"]
    hreflang: str
    href: str
    integrity: str


class InputAttrs(GlobalAttrs, total=False):
    accept: str
    alt: str
    autcomplete: Literal["on", "off"]
    autofocus: bool
    dirname: str
    disabled: bool
    form: str
    formaction: str
    formenctype: Literal[
        "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
    ]
    formmethod: Literal["get", "post"]
    formnovalidate: bool
    formtarget: str
    height: int
    list: str
    max: int
    maxlength: int
    min: int
    minlength: int
    multiple: bool
    name: str
    pattern: str
    placeholder: str
    popovertarget: str
    popovertargetaction: Literal["show", "hide", "toggle"]
    readonly: bool
    required: bool
    size: int
    src: str
    step: int
    type: Literal[
        "checkbox",
        "button",
        "color",
        "date",
        "datetime-local",
        "email",
        "file",
        "hidden",
        "image",
        "month",
        "number",
        "password",
        "radio",
        "range",
        "reset",
        "search",
        "submit",
        "tel",
        "text",
        "time",
        "url",
        "week",
    ]
    value: str
    width: int


class OutputAttrs(GlobalAttrs, _LabelAttrsAlt, total=False):
    for_: str
    form: str
    name: str


class OptionAttrs(GlobalAttrs, total=False):
    disabled: bool
    label: str
    selected: bool
    value: str


class OptgroupAttrs(GlobalAttrs, total=False):
    disabled: bool
    label: str


class SelectAttrs(GlobalAttrs, total=False):
    autofocus: bool
    disabled: bool
    form: str
    multiple: bool
    name: str
    required: bool
    size: int


class TextareaAttrs(GlobalAttrs, total=False):
    autofocus: bool
    cols: int
    dirname: str
    disabled: bool
    form: str
    maxlength: int
    name: str
    placeholder: str
    readonly: bool
    required: bool
    rows: int
    wrap: Literal["hard", "soft"]


class FieldsetAttrs(GlobalAttrs, total=False):
    disabled: bool
    form: str
    name: str


class FormAttrs(GlobalAttrs, total=False):
    accept_charset: str
    action: str
    autocomplete: Literal["on", "off"]
    enctype: Literal[
        "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
    ]
    method: Literal["get", "post"]
    name: str
    novalidate: bool
    rel: Literal[
        "external",
        "help",
        "license",
        "next",
        "nofollow",
        "noopener",
        "noreferrer",
        "opener",
        "prev",
        "search",
    ]
    target: str


class HyperlinkAttrs(GlobalAttrs, total=False):
    download: str
    href: str
    hreflang: str
    media: str
    ping: str
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    rel: Literal[
        "alternate",
        "author",
        "bookmark",
        "external",
        "help",
        "license",
        "next",
        "nofollow",
        "noreferrer",
        "noopener",
        "prev",
        "search",
        "tag",
    ]
    target: str
    type: str


class ButtonAttrs(GlobalAttrs, total=False):
    autofocus: bool
    disabled: bool
    form: str
    formaction: str
    formenctype: Literal[
        "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
    ]
    formmethod: Literal["get", "post"]
    formnovalidate: bool
    formtarget: str
    popovertarget: str
    popovertargetaction: Literal["show", "hide", "toggle"]
    name: str
    type: Literal["submit", "reset", "button"]
    value: str


class LabelAttrs(GlobalAttrs, _LabelAttrsAlt, total=False):
    for_: str
    name: str


class TdAttrs(GlobalAttrs, total=False):
    colspan: int
    headers: str
    rowspan: int


class ThAttrs(GlobalAttrs, total=False):
    abbr: str
    colspan: int
    headers: str
    rowspan: int
    scope: Literal["col", "colgroup", "row", "rowgroup"]


class LiAttrs(GlobalAttrs, total=False):
    value: int


class ImgAttrs(GlobalAttrs, total=False):
    alt: str
    crossorigin: Literal["anonymous", "use-credentials"]
    height: int
    ismap: bool
    loading: Literal["eager", "lazy"]
    longdesc: str
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "unsafe-url",
    ]
    sizes: str
    src: str
    srcset: str
    usemap: str
    width: int


class SvgAttrs(GlobalAttrs, total=False):
    height: int
    width: int


class IframeAttrs(GlobalAttrs, total=False):
    allow: str
    allowfullscreen: bool
    allowpaymentrequest: bool
    height: int
    loading: Literal["eager", "lazy"]
    name: str
    referrerpolicy: Literal[
        "no-referrer",
        "no-referrer-when-downgrade",
        "origin",
        "origin-when-cross-origin",
        "same-origin",
        "strict-origin-when-cross-origin",
        "unsafe-url",
    ]
    sandbox: Literal[
        "allow-forms",
        "allow-pointer-lock",
        "allow-popups",
        "allow-same-origin",
        "allow-scripts",
        "allow-top-navigation",
    ]
    src: str
    srcdoc: str
    width: int
