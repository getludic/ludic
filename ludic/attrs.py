from typing import Annotated, Literal, Protocol, TypedDict

from .styles.types import CSSProperties


class URLType(Protocol):
    """Protocol for URL-like types."""

    def __str__(self) -> str: ...


class Alias(str):
    """Alias type for attributes."""


class Attrs(TypedDict, total=False):
    """Attributes of an element or component.

    Example usage::

        class PersonAttrs(Attributes):
            name: str
            age: NotRequired[int]

        class Person(Component[PersonAttrs]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(self.attrs["name"]),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )
    """


class NoAttrs(TypedDict):
    """Placeholder for element with no attributes."""


class HtmlAttrs(Attrs, total=False):
    """Common attributes for HTML elements."""

    id: str
    accesskey: str
    class_: Annotated[str, Alias("class")]
    classes: Annotated[list[str], Alias("class")]  # merged with class_
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

    hx_get: Annotated[URLType, Alias("hx-get")]
    hx_post: Annotated[URLType, Alias("hx-post")]
    hx_put: Annotated[URLType, Alias("hx-put")]
    hx_delete: Annotated[URLType, Alias("hx-delete")]
    hx_patch: Annotated[URLType, Alias("hx-patch")]

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
    hx_disabled_elt: Annotated[str, Alias("hx-disabled-elt")]
    hx_disinherit: Annotated[str, Alias("hx-disinherit")]
    hx_encoding: Annotated[str, Alias("hx-encoding")]
    hx_headers: Annotated[str, Alias("hx-headers")]
    hx_params: Annotated[str, Alias("hx-params")]
    hx_preserve: Annotated[bool, Alias("hx-preserve")]
    hx_prompt: Annotated[str, Alias("hx-prompt")]
    hx_replace_url: Annotated[URLType, Alias("hx-replace-url")]
    hx_request: Annotated[str, Alias("hx-request")]
    hx_validate: Annotated[bool, Alias("hx-validate")]
    hx_ws: Annotated[str, Alias("hx-ws")]
    hx_sse: Annotated[str, Alias("hx-sse")]

    # Extensions
    ws_connect: Annotated[str, Alias("ws-connect")]
    ws_send: Annotated[str, Alias("ws-send")]
    sse_connect: Annotated[str, Alias("sse-connect")]
    sse_send: Annotated[str, Alias("sse-send")]
    sse_swap: Annotated[str, Alias("sse-swap")]


class WindowEventAttrs(Attrs, total=False):
    """Event Attributes for HTML elements."""

    on_afterprint: Annotated[str, Alias("onafterprint")]
    on_beforeprint: Annotated[str, Alias("onbeforeprint")]
    on_beforeunload: Annotated[str, Alias("onbeforeunload")]
    on_error: Annotated[str, Alias("onerror")]
    on_hashchange: Annotated[str, Alias("onhashchange")]
    on_load: Annotated[str, Alias("onload")]
    on_message: Annotated[str, Alias("onmessage")]
    on_offline: Annotated[str, Alias("onoffline")]
    on_online: Annotated[str, Alias("ononline")]
    on_pagehide: Annotated[str, Alias("onpagehide")]
    on_pageshow: Annotated[str, Alias("onpageshow")]
    on_popstate: Annotated[str, Alias("onpopstate")]
    on_resize: Annotated[str, Alias("onresize")]
    on_storage: Annotated[str, Alias("onstorage")]
    on_unhandledrejection: Annotated[str, Alias("onunhandledrejection")]
    on_unload: Annotated[str, Alias("onunload")]


class FormEventAttrs(Attrs, total=False):
    """Event Attributes for HTML Form elements."""

    on_blur: Annotated[str, Alias("onblur")]
    on_change: Annotated[str, Alias("onchange")]
    on_contextmenu: Annotated[str, Alias("oncontextmenu")]
    on_focus: Annotated[str, Alias("onfocus")]
    on_input: Annotated[str, Alias("oninput")]
    on_invalid: Annotated[str, Alias("oninvalid")]
    on_reset: Annotated[str, Alias("onreset")]
    on_search: Annotated[str, Alias("onsearch")]
    on_select: Annotated[str, Alias("onselect")]
    on_submit: Annotated[str, Alias("onsubmit")]


class KeyboardEventAttrs(Attrs, total=False):
    """Event Attributes for Keyboard events."""

    on_keydown: Annotated[str, Alias("onkeydown")]
    on_keypress: Annotated[str, Alias("onkeypress")]
    on_keyup: Annotated[str, Alias("onkeyup")]


class MouseEventAttrs(Attrs, total=False):
    """Event Attributes for Mouse events."""

    on_click: Annotated[str, Alias("onclick")]
    on_dblclick: Annotated[str, Alias("ondblclick")]
    on_mousedown: Annotated[str, Alias("onmousedown")]
    on_mousemove: Annotated[str, Alias("onmousemove")]
    on_mouseout: Annotated[str, Alias("onmouseout")]
    on_mouseover: Annotated[str, Alias("onmouseover")]
    on_mouseup: Annotated[str, Alias("onmouseup")]
    on_wheel: Annotated[str, Alias("onwheel")]


class DragEventAttrs(Attrs, total=False):
    """Event Attributes for Drag events."""

    on_drag: Annotated[str, Alias("ondrag")]
    on_dragend: Annotated[str, Alias("ondragend")]
    on_dragenter: Annotated[str, Alias("ondragenter")]
    on_dragleave: Annotated[str, Alias("ondragleave")]
    on_dragover: Annotated[str, Alias("ondragover")]
    on_dragstart: Annotated[str, Alias("ondragstart")]
    on_drop: Annotated[str, Alias("ondrop")]


class ClipboardEventAttrs(Attrs, total=False):
    """Event Attributes for Clipboard events."""

    on_copy: Annotated[str, Alias("oncopy")]
    on_cut: Annotated[str, Alias("oncut")]
    on_paste: Annotated[str, Alias("onpaste")]


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
    property: str


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
    type: str
    rel: Literal[
        "canonical", "alternate", "stylesheet", "icon", "apple-touch-icon", "preconnect"
    ]
    crossorigin: Literal["anonymous", "use-credentials", True]
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
    view_box: Annotated[str, Alias("viewBox")]
    clip_path: Annotated[str, Alias("clip-path")]
    clip_rule: Annotated[str, Alias("clip-rule")]
    fill: str
    fill_rule: Annotated[str, Alias("fill-rule")]
    stroke: str
    stroke_dasharray: Annotated[str, Alias("stroke-dasharray")]
    stroke_dashoffset: Annotated[str, Alias("stroke-dashoffset")]
    stroke_linecap: Annotated[str, Alias("stroke-linecap")]
    stroke_linejoin: Annotated[str, Alias("stroke-linejoin")]
    stroke_miterlimit: Annotated[str, Alias("stroke-miterlimit")]
    stroke_opacity: Annotated[str, Alias("stroke-opacity")]
    stroke_width: Annotated[str, Alias("stroke-width")]
    transform: str


class CircleAttrs(SvgAttrs, total=False):
    cx: str
    cy: str
    r: str


class LineAttrs(SvgAttrs, total=False):
    x1: str
    x2: str
    y1: str
    y2: str


class PathAttrs(SvgAttrs, total=False):
    d: str


class PolylineAttrs(SvgAttrs, total=False):
    points: str


class IframeAttrs(GlobalAttrs, total=False):
    allow: str
    allowfullscreen: bool
    allowpaymentrequest: bool
    height: int
    frameborder: str
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
    scrolling: str
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
