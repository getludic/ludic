from .attrs import (
    ButtonAttributes,
    FieldsetAttributes,
    FormAttributes,
    GlobalAttributes,
    HeadLinkAttributes,
    HtmlTagAttributes,
    HyperlinkAttributes,
    IframeAttributes,
    ImgAttributes,
    InputAttributes,
    LabelAttributes,
    LiAttributes,
    MetaAttributes,
    NoAttributes,
    OptgroupAttributes,
    OptionAttributes,
    OutputAttributes,
    ScriptAttributes,
    SelectAttributes,
    StyleAttributes,
    SvgAttributes,
    TdAttributes,
    TextareaAttributes,
    ThAttributes,
)
from .base import AnyChildren, Element, TextChildren


class div(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "div"


class span(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "span"


class p(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "p"


class a(Element[*AnyChildren, HyperlinkAttributes]):
    html_name: str = "a"


class br(Element[GlobalAttributes]):
    html_name: str = "br"


class button(Element[*AnyChildren, ButtonAttributes]):
    html_name: str = "button"


class label(Element[*AnyChildren, LabelAttributes]):
    html_name: str = "label"


class td(Element[*AnyChildren, TdAttributes]):
    html_name: str = "td"


class th(Element[*AnyChildren, ThAttributes]):
    html_name: str = "th"


class tr(Element[*tuple[th | td, ...], GlobalAttributes]):
    html_name: str = "tr"


class thead(Element[*tuple[tr, ...], GlobalAttributes]):
    html_name: str = "thead"


class tbody(Element[*tuple[tr, ...], GlobalAttributes]):
    html_name: str = "tbody"


class tfoot(Element[*tuple[tr, ...], GlobalAttributes]):
    html_name: str = "tfoot"


class table(Element[*tuple[thead | tbody | tfoot, ...], GlobalAttributes]):
    html_name: str = "table"


class li(Element[*AnyChildren, LiAttributes]):
    html_name: str = "li"


class ul(Element[*tuple[li, ...], GlobalAttributes]):
    html_name: str = "ul"


class ol(Element[*tuple[li, ...], GlobalAttributes]):
    html_name: str = "ol"


class dt(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "dt"


class dd(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "dd"


class dl(Element[*tuple[dt | dd, ...], GlobalAttributes]):
    html_name: str = "dl"


class section(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "section"


class input(Element[InputAttributes]):
    html_name: str = "input"


class output(Element[OutputAttributes]):
    html_name: str = "output"


class legend(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "legend"


class option(Element[*TextChildren, OptionAttributes]):
    html_name: str = "option"


class optgroup(Element[*tuple[option, ...], OptgroupAttributes]):
    html_name: str = "optgroup"


class select(Element[*tuple[option | optgroup, ...], SelectAttributes]):
    html_name: str = "select"


class textarea(Element[*TextChildren, TextareaAttributes]):
    html_name: str = "textarea"


class fieldset(Element[*tuple[legend | label | input, ...], FieldsetAttributes]):
    html_name: str = "fieldset"


class form(
    Element[
        *tuple[
            input
            | textarea
            | select
            | option
            | button
            | label
            | output
            | fieldset
            | optgroup
            | span
            | div,
            ...,
        ],
        FormAttributes,
    ]
):
    html_name: str = "form"


class img(Element[ImgAttributes]):
    html_name: str = "img"


class svg(Element[*AnyChildren, SvgAttributes]):
    html_name: str = "svg"


class b(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "b"


class i(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "i"


class s(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "s"


class u(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "u"


class header(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "header"


class small(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "small"


class h1(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "h1"


class h2(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "h2"


class h3(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "h3"


class h4(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "h4"


class h5(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "h5"


class h6(Element[*TextChildren, GlobalAttributes]):
    html_name: str = "h6"


class title(Element[*TextChildren, NoAttributes]):
    html_name: str = "title"


class link(Element[*TextChildren, HeadLinkAttributes]):
    html_name: str = "link"


class style(Element[*TextChildren, StyleAttributes]):
    html_name: str = "style"


class script(Element[*TextChildren, ScriptAttributes]):
    html_name: str = "script"


class meta(Element[*TextChildren, MetaAttributes]):
    html_name: str = "meta"


class head(Element[*tuple[title | link | style | meta, ...], NoAttributes]):
    html_name: str = "head"


class body(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "body"


class footer(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "footer"


class html(Element[head, body, HtmlTagAttributes]):
    html_name: str = "html"


class iframe(Element[IframeAttributes]):
    html_name: str = "iframe"
