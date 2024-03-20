from typing import Annotated, Literal

from .base import Attrs as Attrs
from .base import NoAttrs as NoAttrs
from .css import CSSProperties


class Alias(str):
    """Alias type for attributes."""


class HtmlAttrs(Attrs, total=False):
    """Common attributes for HTML elements."""

    id: str
    accesskey: str
    class_: Annotated[str, Alias("class")]
    contenteditable: Literal["true", "false"]
    dir: Literal["ltr", "rtl", "auto"]
    draggable: Literal["true", "false"]
    enterkeyhint: Literal["enter", "done", "go", "next", "previous", "search", "send"]
    hidden: Literal["true", "false"]
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


class HtmxAttrs(Attrs, total=False):
    """HTMX attributes for HTML elements.

    See: https://htmx.org/
    """

    hx_get: Annotated[str, Alias("hx-get")]
    hx_post: Annotated[str, Alias("hx-post")]
    hx_put: Annotated[str, Alias("hx-put")]
    hx_delete: Annotated[str, Alias("hx-delete")]
    hx_patch: Annotated[str, Alias("hx-patch")]

    hx_on: Annotated[str, Alias("hx-on")]
    hx_include: Annotated[str, Alias("hx-include")]
    hx_confirm: Annotated[str, Alias("hx-confirm")]
    hx_trigger: Annotated[str, Alias("hx-trigger")]
    hx_target: Annotated[Literal["this", "next", "previous"] | str, Alias("hx-target")]
    hx_select: Annotated[str, Alias("hx-select")]
    hx_select_oob: Annotated[str, Alias("hx-select-oob")]
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
        ]
        | str,
        Alias("hx-swap"),
    ]
    hx_swap_oob: Annotated[str, Alias("hx-swap-oob")]
    hx_vals: Annotated[str, Alias("hx-vals")]
    hx_sync: Annotated[str, Alias("hx-sync")]
    hx_boost: Annotated[bool, Alias("hx-boost")]
    hx_indicator: Annotated[str, Alias("hx-indicator")]
    hx_push_url: Annotated[bool, Alias("hx-push-url")]
    hx_history: Annotated[bool, Alias("hx-history")]
    hx_history_elt: Annotated[str, Alias("hx-history-elt")]
    hx_ext: Annotated[str, Alias("hx-ext")]
    hx_disable: Annotated[bool, Alias("hx-disable")]
    hx_disabled_ext: Annotated[str, Alias("hx-disabled-ext")]
    hx_disinherit: Annotated[str, Alias("hx-disinherit")]
    hx_encoding: Annotated[str, Alias("hx-encoding")]
    hx_headers: Annotated[str, Alias("hx-headers")]
    hx_params: Annotated[str, Alias("hx-params")]
    hx_preserve: Annotated[bool, Alias("hx-preserve")]
    hx_prompt: Annotated[str, Alias("hx-prompt")]
    hx_replace_url: Annotated[str, Alias("hx-replace-url")]
    hx_request: Annotated[str, Alias("hx-request")]
    hx_validate: Annotated[bool, Alias("hx-validate")]
    hx_ws: Annotated[str, Alias("hx-ws")]
    hx_sse: Annotated[str, Alias("hx-sse")]


class WindowEventAttrs(Attrs, total=False):
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


class FormEventAttrs(Attrs, total=False):
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


class KeyboardEventAttrs(Attrs, total=False):
    """Event Attributes for Keyboard events."""

    onkeydown: str
    onkeypress: str
    onkeyup: str


class MouseEventAttrs(Attrs, total=False):
    """Event Attributes for Mouse events."""

    onclick: str
    ondblclick: str
    onmousedown: str
    onmousemove: str
    onmouseout: str
    onmouseover: str
    onmouseup: str
    onwheel: str


class DragEventAttrs(Attrs, total=False):
    """Event Attributes for Drag events."""

    ondrag: str
    ondragend: str
    ondragenter: str
    ondragleave: str
    ondragover: str
    ondragstart: str
    ondrop: str


class ClipboardEventAttrs(Attrs, total=False):
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


class HtmlTagAttrs(Attrs, total=False):
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
    checked: bool
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


class TextAreaAttrs(GlobalAttrs, total=False):
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
    version: str
    xmlns: str
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


class ColAttrs(GlobalAttrs, total=False):
    span: int


class DelAttrs(GlobalAttrs, total=False):
    cite: str
    datetime: str


class InsAttrs(GlobalAttrs, total=False):
    cite: str
    datetime: str


class AreaAttrs(GlobalAttrs, total=False):
    alt: str
    coords: str
    download: str
    href: str
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
    rel: str
    shape: Literal["rect", "circle", "poly", "default"]
    target: str


class SourceAttrs(GlobalAttrs, total=False):
    media: str
    sizes: str
    src: str
    srcset: str
    type: str


class AudioAttrs(GlobalAttrs, total=False):
    src: str
    preload: Literal["auto", "metadata", "none"]
    autoplay: bool
    controls: bool
    loop: bool
    muted: bool
    mediagroup: str


class BaseAttrs(GlobalAttrs, total=False):
    href: str
    target: str


class CanvasAttrs(GlobalAttrs, total=False):
    width: int
    height: int


class DataAttrs(GlobalAttrs, total=False):
    value: str


class DetailsAttrs(GlobalAttrs, total=False):
    open: bool


class DialogAttrs(GlobalAttrs, total=False):
    open: bool


class EmbedAttrs(GlobalAttrs, total=False):
    height: int
    src: str
    type: str
    width: int


class MapAttrs(GlobalAttrs, total=False):
    name: str


class MeterAttrs(GlobalAttrs, total=False):
    form: str
    high: int
    low: int
    max: int
    min: int
    optimum: int
    value: int


class ObjectAttrs(GlobalAttrs, total=False):
    data: str
    form: str
    height: int
    name: str
    type: str
    typemustmatch: bool
    usemap: str
    width: int


class OlAttrs(GlobalAttrs, total=False):
    reversed: bool
    start: int
    type: Literal["1", "a", "A", "i", "I"]


class ParamAttrs(GlobalAttrs, total=False):
    name: str
    value: str


class ProgressAttrs(GlobalAttrs, total=False):
    max: int
    value: int


class QAttrs(HtmlAttrs, total=False):
    cite: str


class TimeAttrs(GlobalAttrs, total=False):
    datetime: str


class TrackAttrs(GlobalAttrs, total=False):
    default: bool
    kind: Literal["subtitles", "captions", "descriptions", "chapters", "metadata"]
    label: str
    src: str
    srclang: str


class VideoAttrs(GlobalAttrs, total=False):
    autoplay: bool
    controls: bool
    height: int
    loop: bool
    muted: bool
    poster: str
    preload: Literal["auto", "metadata", "none"]
    src: str
    width: int
