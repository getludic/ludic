from typing import Annotated, Literal

from .base import BaseAttrs
from .css import CSSProperties


class NoAttrs(BaseAttrs):
    """Placeholder for element with no attributes."""


class HtmlAttrs(BaseAttrs, total=False):
    """Common attributes for HTML elements."""

    id: str
    accesskey: str
    class_: Annotated[str, "class"]
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


class HtmxAttrs(BaseAttrs, total=False):
    """HTMX attributes for HTML elements.

    See: https://htmx.org/
    """

    hx_get: Annotated[str, "hx-get"]
    hx_post: Annotated[str, "hx-post"]
    hx_put: Annotated[str, "hx-put"]
    hx_delete: Annotated[str, "hx-delete"]
    hx_patch: Annotated[str, "hx-patch"]

    hx_trigger: Annotated[str, "hx-trigger"]
    hx_target: Annotated[str, "hx-target"]
    hx_swap: Annotated[
        Literal[
            "innerHTML",
            "outerHTML",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ],
        "hx-swap",
    ]


class WindowEventAttrs(BaseAttrs, total=False):
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


class FormEventAttrs(BaseAttrs, total=False):
    """Event Attributes for HTML Form elements."""

    onblur: str
    onchange: str
    oncontextmenu: str
    onfocus: str
    oninput: str
    oninvalid: str
    onreset: str
    onsearch: str
    onselect: str
    onsubmit: str


class KeyboardEventAttrs(BaseAttrs, total=False):
    """Event Attributes for Keyboard events."""

    onkeydown: str
    onkeypress: str
    onkeyup: str


class MouseEventAttrs(BaseAttrs, total=False):
    """Event Attributes for Mouse events."""

    onclick: str
    ondblclick: str
    onmousedown: str
    onmousemove: str
    onmouseout: str
    onmouseover: str
    onmouseup: str
    onmousewheel: str  # Deprecated, use onwheel instead
    onwheel: str


class DragEventAttrs(BaseAttrs, total=False):
    """Event Attributes for Drag events."""

    ondrag: str
    ondragend: str
    ondragenter: str
    ondragleave: str
    ondragover: str
    ondragstart: str
    ondrop: str


class ClipboardEventAttrs(BaseAttrs, total=False):
    """Event Attributes for Clipboard events."""

    oncopy: str
    oncut: str
    onpaste: str


class EventAttrs(
    WindowEventAttrs,
    FormEventAttrs,
    KeyboardEventAttrs,
    MouseEventAttrs,
    DragEventAttrs,
    ClipboardEventAttrs,
    total=False,
):
    """Event Attributes for HTML elements."""


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


class OutputAttrs(GlobalAttrs, total=False):
    for_: Annotated[str, "for"]
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


class BlockquoteAttrs(GlobalAttrs, total=False):
    cite: str


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


class LabelAttrs(GlobalAttrs, total=False):
    for_: Annotated[str, "for"]
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
