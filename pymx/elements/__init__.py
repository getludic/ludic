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
from .base import AnyChildren, Element, PrimitiveChildren


class div(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "div"


class span(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "span"


class main(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "main"


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


class tr(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "tr"


class thead(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "thead"


class tbody(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "tbody"


class tfoot(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "tfoot"


class table(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "table"


class li(Element[*AnyChildren, LiAttributes]):
    html_name: str = "li"


class ul(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "ul"


class ol(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "ol"


class dt(Element[*PrimitiveChildren, GlobalAttributes]):
    html_name: str = "dt"


class dd(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "dd"


class dl(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "dl"


class section(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "section"


class input(Element[InputAttributes]):
    html_name: str = "input"


class output(Element[OutputAttributes]):
    html_name: str = "output"


class legend(Element[*PrimitiveChildren, GlobalAttributes]):
    html_name: str = "legend"


class option(Element[*PrimitiveChildren, OptionAttributes]):
    html_name: str = "option"


class optgroup(Element[*AnyChildren, OptgroupAttributes]):
    html_name: str = "optgroup"


class select(Element[*AnyChildren, SelectAttributes]):
    html_name: str = "select"


class textarea(Element[*PrimitiveChildren, TextareaAttributes]):
    html_name: str = "textarea"


class fieldset(Element[*AnyChildren, FieldsetAttributes]):
    html_name: str = "fieldset"


class form(Element[*AnyChildren, FormAttributes]):
    html_name: str = "form"


class img(Element[ImgAttributes]):
    html_name: str = "img"


class svg(Element[*AnyChildren, SvgAttributes]):
    html_name: str = "svg"


class b(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "b"


class i(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "i"


class s(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "s"


class u(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "u"


class header(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "header"


class small(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "small"


class h1(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "h1"


class h2(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "h2"


class h3(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "h3"


class h4(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "h4"


class h5(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "h5"


class h6(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "h6"


class title(Element[*PrimitiveChildren, NoAttributes]):
    html_name: str = "title"


class link(Element[*PrimitiveChildren, HeadLinkAttributes]):
    html_name: str = "link"


class style(Element[*PrimitiveChildren, StyleAttributes]):
    html_name: str = "style"


class script(Element[*PrimitiveChildren, ScriptAttributes]):
    html_name: str = "script"
    always_pair: bool = True


class noscript(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "noscript"
    always_pair: bool = True


class meta(Element[*PrimitiveChildren, MetaAttributes]):
    html_name: str = "meta"


class head(Element[*AnyChildren, NoAttributes]):
    html_name: str = "head"


class body(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "body"


class footer(Element[*AnyChildren, GlobalAttributes]):
    html_name: str = "footer"


class html(Element[head, body, HtmlTagAttributes]):
    html_name: str = "html"


class iframe(Element[IframeAttributes]):
    html_name: str = "iframe"
