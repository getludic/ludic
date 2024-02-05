from .base import AnyChildren, Element, NoChildren, SimpleChildren
from .html import (
    ButtonAttributes,
    FieldsetAttributes,
    FormAttributes,
    GlobalAttributes,
    HeadLinkAttributes,
    HtmlTagAttributes,
    IframeAttributes,
    ImgAttributes,
    InputAttributes,
    LabelAttributes,
    LiAttributes,
    LinkAttributes,
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


class div(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "div"


class span(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "span"


class p(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "p"


class a(Element[*AnyChildren, LinkAttributes]):
    html_name: str = "a"


class br(Element[*NoChildren, GlobalAttributes]):
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


class table(Element[thead | None, tbody | None, tfoot | None, GlobalAttributes]):
    html_name: str = "table"


class li(Element[*AnyChildren, LiAttributes]):
    html_name: str = "li"


class ul(Element[*tuple[li, ...], GlobalAttributes]):
    html_name: str = "ul"


class ol(Element[*tuple[li, ...], GlobalAttributes]):
    html_name: str = "ol"


class dt(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "dt"


class dd(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "dd"


class dl(Element[*tuple[dt | dd, ...], GlobalAttributes]):
    html_name: str = "dl"


class section(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "section"


class input(Element[*NoChildren, InputAttributes]):
    html_name: str = "input"


class output(Element[*NoChildren, OutputAttributes]):
    html_name: str = "output"


class legend(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "legend"


class option(Element[*SimpleChildren, OptionAttributes]):
    html_name: str = "option"


class optgroup(Element[*tuple[option, ...], OptgroupAttributes]):
    html_name: str = "optgroup"


class select(Element[*tuple[option | optgroup, ...], SelectAttributes]):
    html_name: str = "select"


class textarea(Element[*SimpleChildren, TextareaAttributes]):
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


class img(Element[*NoChildren, ImgAttributes]):
    html_name: str = "img"


class svg(Element[*AnyChildren, SvgAttributes]):
    html_name: str = "svg"


class b(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "b"


class i(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "i"


class s(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "s"


class u(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "u"


class header(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "header"


class small(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "small"


class h1(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "h1"


class h2(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "h2"


class h3(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "h3"


class h4(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "h4"


class h5(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "h5"


class h6(Element[*SimpleChildren, GlobalAttributes]):
    html_name: str = "h6"


class title(Element[*SimpleChildren, NoAttributes]):
    html_name: str = "title"


class link(Element[*SimpleChildren, HeadLinkAttributes]):
    html_name: str = "link"


class style(Element[*SimpleChildren, StyleAttributes]):
    html_name: str = "style"


class script(Element[*SimpleChildren, ScriptAttributes]):
    html_name: str = "script"


class meta(Element[*SimpleChildren, MetaAttributes]):
    html_name: str = "meta"


class head(Element[*tuple[title | link | style | meta, ...], NoAttributes]):
    html_name: str = "head"


class body(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "body"


class footer(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "footer"


class html(Element[head, body, HtmlTagAttributes]):
    html_name: str = "html"


class iframe(Element[*NoChildren, IframeAttributes]):
    html_name: str = "iframe"
