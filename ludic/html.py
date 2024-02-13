from .attrs import (
    ButtonAttrs,
    FieldsetAttrs,
    FormAttrs,
    GlobalAttrs,
    HeadLinkAttrs,
    HtmlTagAttrs,
    HyperlinkAttrs,
    IframeAttrs,
    ImgAttrs,
    InputAttrs,
    LabelAttrs,
    LiAttrs,
    MetaAttrs,
    NoAttrs,
    OptgroupAttrs,
    OptionAttrs,
    OutputAttrs,
    ScriptAttrs,
    SelectAttrs,
    StyleAttrs,
    SvgAttrs,
    TdAttrs,
    TextareaAttrs,
    ThAttrs,
)
from .base import AnyChildren, ComplexChildren, Element, PrimitiveChildren


class div(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "div"


class span(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "span"


class main(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "main"


class p(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "p"


class a(Element[*AnyChildren, HyperlinkAttrs]):
    html_name: str = "a"


class br(Element[GlobalAttrs]):
    html_name: str = "br"


class button(Element[*AnyChildren, ButtonAttrs]):
    html_name: str = "button"


class label(Element[*AnyChildren, LabelAttrs]):
    html_name: str = "label"


class td(Element[*AnyChildren, TdAttrs]):
    html_name: str = "td"


class th(Element[*AnyChildren, ThAttrs]):
    html_name: str = "th"


class tr(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "tr"


class thead(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "thead"


class tbody(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "tbody"


class tfoot(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "tfoot"


class table(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "table"


class li(Element[*AnyChildren, LiAttrs]):
    html_name: str = "li"


class ul(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "ul"


class ol(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "ol"


class dt(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "dt"


class dd(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "dd"


class dl(Element[*ComplexChildren, GlobalAttrs]):
    html_name: str = "dl"


class section(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "section"


class input(Element[InputAttrs]):
    html_name: str = "input"


class output(Element[OutputAttrs]):
    html_name: str = "output"


class legend(Element[*PrimitiveChildren, GlobalAttrs]):
    html_name: str = "legend"


class option(Element[*PrimitiveChildren, OptionAttrs]):
    html_name: str = "option"


class optgroup(Element[*AnyChildren, OptgroupAttrs]):
    html_name: str = "optgroup"


class select(Element[*AnyChildren, SelectAttrs]):
    html_name: str = "select"


class textarea(Element[*PrimitiveChildren, TextareaAttrs]):
    html_name: str = "textarea"


class fieldset(Element[*AnyChildren, FieldsetAttrs]):
    html_name: str = "fieldset"


class form(Element[*AnyChildren, FormAttrs]):
    html_name: str = "form"


class img(Element[ImgAttrs]):
    html_name: str = "img"


class svg(Element[*AnyChildren, SvgAttrs]):
    html_name: str = "svg"


class b(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "b"


class i(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "i"


class s(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "s"


class u(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "u"


class header(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "header"


class small(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "small"


class h1(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "h1"


class h2(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "h2"


class h3(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "h3"


class h4(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "h4"


class h5(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "h5"


class h6(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "h6"


class title(Element[*PrimitiveChildren, NoAttrs]):
    html_name: str = "title"


class link(Element[*PrimitiveChildren, HeadLinkAttrs]):
    html_name: str = "link"


class style(Element[*PrimitiveChildren, StyleAttrs]):
    html_name: str = "style"


class script(Element[*PrimitiveChildren, ScriptAttrs]):
    html_name: str = "script"
    always_pair: bool = True


class noscript(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "noscript"
    always_pair: bool = True


class meta(Element[*PrimitiveChildren, MetaAttrs]):
    html_name: str = "meta"


class head(Element[*AnyChildren, NoAttrs]):
    html_name: str = "head"


class body(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "body"


class footer(Element[*AnyChildren, GlobalAttrs]):
    html_name: str = "footer"


class html(Element[head, body, HtmlTagAttrs]):
    html_name: str = "html"


class iframe(Element[IframeAttrs]):
    html_name: str = "iframe"
