from typing import Literal, TypedDict

from .base import Attributes

HTMLStyles = TypedDict(
    "HTMLStyles",
    {
        "color": str,
        "direction": Literal["row", "column"],
        "height": str,
        "justify-content": Literal["start", "end", "center", "equally-spaced"],
        "width": str,
    },
    total=False,
)


class NoAttributes(Attributes):
    """Placeholder for element with no attributes."""


class HtmlAttributes(Attributes, total=False):
    """Common attributes for HTML elements."""

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
    style: HTMLStyles
    tabindex: int
    title: str
    translate: Literal["yes", "no"]


class HtmxAttributes(Attributes, total=False):
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


class EventAttributes(Attributes, total=False):
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


class HtmlAndEventAttributes(HtmlAttributes, EventAttributes, total=False):
    """Common HTML and event attributes."""


class GlobalAttributes(HtmxAttributes, HtmlAndEventAttributes, total=False):
    """Global attributes for HTML elements."""


class HtmlTagAttributes(Attributes, total=False):
    xmlns: str


class MetaAttributes(HtmlAttributes):
    name: str
    content: str


class StyleAttributes(HtmlAndEventAttributes, total=False):
    media: str
    type: Literal["text/css"]


class ScriptAttributes(HtmlAttributes, total=False):
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


class HeadLinkAttributes(HtmlAttributes, total=False):
    rel: Literal["canonical", "alternate"]
    hreflang: str
    href: str


class InputAttributes(HtmxAttributes, total=False):
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


class OutputAttributes(GlobalAttributes, total=False):
    for_: str
    form: str
    name: str


class OptionAttributes(GlobalAttributes, total=False):
    disabled: bool
    label: str
    selected: bool
    value: str


class OptgroupAttributes(GlobalAttributes, total=False):
    disabled: bool
    label: str


class SelectAttributes(GlobalAttributes, total=False):
    autofocus: bool
    disabled: bool
    form: str
    multiple: bool
    name: str
    required: bool
    size: int


class TextareaAttributes(GlobalAttributes, total=False):
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


class FieldsetAttributes(GlobalAttributes, total=False):
    disabled: bool
    form: str
    name: str


class FormAttributes(GlobalAttributes, total=False):
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


class LinkAttributes(GlobalAttributes, total=False):
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


class ButtonAttributes(GlobalAttributes, total=False):
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


class LabelAttributes(GlobalAttributes, total=False):
    for_: str
    name: str


class TdAttributes(GlobalAttributes, total=False):
    colspan: int
    headers: str
    rowspan: int


class ThAttributes(GlobalAttributes, total=False):
    abbr: str
    colspan: int
    headers: str
    rowspan: int
    scope: Literal["col", "colgroup", "row", "rowgroup"]


class LiAttributes(GlobalAttributes, total=False):
    value: int


class ImgAttributes(GlobalAttributes, total=False):
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


class SvgAttributes(GlobalAttributes, total=False):
    height: int
    width: int


class IframeAttributes(GlobalAttributes, total=False):
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
