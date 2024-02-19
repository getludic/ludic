from .attrs import (
    AreaAttrs,
    BlockquoteAttrs,
    ButtonAttrs,
    ColAttrs,
    DelAttrs,
    FieldsetAttrs,
    FormAttrs,
    GlobalAttrs,
    HeadLinkAttrs,
    HtmlTagAttrs,
    HyperlinkAttrs,
    IframeAttrs,
    ImgAttrs,
    InputAttrs,
    InsAttrs,
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
    TextAreaAttrs,
    ThAttrs,
)
from .types import (
    AnyChild,
    ComplexChild,
    Element,
    ElementStrict,
    NoChild,
    PrimitiveChild,
)


class div(Element[AnyChild, GlobalAttrs]):
    html_name: str = "div"


class span(Element[AnyChild, GlobalAttrs]):
    html_name: str = "span"


class main(Element[AnyChild, GlobalAttrs]):
    html_name: str = "main"


class p(Element[AnyChild, GlobalAttrs]):
    html_name: str = "p"


class a(Element[AnyChild, HyperlinkAttrs]):
    html_name: str = "a"


class br(Element[NoChild, GlobalAttrs]):
    html_name: str = "br"


class button(Element[AnyChild, ButtonAttrs]):
    html_name: str = "button"


class label(Element[AnyChild, LabelAttrs]):
    html_name: str = "label"


class td(Element[AnyChild, TdAttrs]):
    html_name: str = "td"


class th(Element[AnyChild, ThAttrs]):
    html_name: str = "th"


class tr(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "tr"


class thead(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "thead"


class tbody(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "tbody"


class tfoot(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "tfoot"


class table(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "table"


class li(Element[AnyChild, LiAttrs]):
    html_name: str = "li"


class ul(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "ul"


class ol(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "ol"


class dt(Element[AnyChild, GlobalAttrs]):
    html_name: str = "dt"


class dd(Element[AnyChild, GlobalAttrs]):
    html_name: str = "dd"


class dl(Element[ComplexChild, GlobalAttrs]):
    html_name: str = "dl"


class section(Element[AnyChild, GlobalAttrs]):
    html_name: str = "section"


class input(Element[NoChild, InputAttrs]):
    html_name: str = "input"


class output(Element[NoChild, OutputAttrs]):
    html_name: str = "output"


class legend(Element[PrimitiveChild, GlobalAttrs]):
    html_name: str = "legend"


class option(Element[PrimitiveChild, OptionAttrs]):
    html_name: str = "option"


class optgroup(Element[AnyChild, OptgroupAttrs]):
    html_name: str = "optgroup"


class select(Element[AnyChild, SelectAttrs]):
    html_name: str = "select"


class textarea(Element[PrimitiveChild, TextAreaAttrs]):
    html_name: str = "textarea"


class fieldset(Element[AnyChild, FieldsetAttrs]):
    html_name: str = "fieldset"


class form(Element[AnyChild, FormAttrs]):
    html_name: str = "form"


class img(Element[NoChild, ImgAttrs]):
    html_name: str = "img"


class svg(Element[AnyChild, SvgAttrs]):
    html_name: str = "svg"


class b(Element[AnyChild, GlobalAttrs]):
    html_name: str = "b"


class i(Element[AnyChild, GlobalAttrs]):
    html_name: str = "i"


class s(Element[AnyChild, GlobalAttrs]):
    html_name: str = "s"


class u(Element[AnyChild, GlobalAttrs]):
    html_name: str = "u"


class strong(Element[AnyChild, GlobalAttrs]):
    html_name: str = "strong"


class em(Element[AnyChild, GlobalAttrs]):
    html_name: str = "em"


class mark(Element[AnyChild, GlobalAttrs]):
    html_name: str = "mark"


class del_(Element[AnyChild, DelAttrs]):
    html_name: str = "del"


class ins(Element[AnyChild, InsAttrs]):
    html_name: str = "ins"


class header(Element[AnyChild, GlobalAttrs]):
    html_name: str = "header"


class big(Element[AnyChild, GlobalAttrs]):
    html_name: str = "big"


class small(Element[AnyChild, GlobalAttrs]):
    html_name: str = "small"


class code(Element[AnyChild, GlobalAttrs]):
    html_name: str = "code"


class pre(Element[AnyChild, GlobalAttrs]):
    html_name: str = "pre"


class cite(Element[AnyChild, GlobalAttrs]):
    html_name: str = "cite"


class blockquote(Element[AnyChild, BlockquoteAttrs]):
    html_name: str = "blockquote"


class abbr(Element[AnyChild, GlobalAttrs]):
    html_name: str = "abbr"


class h1(Element[AnyChild, GlobalAttrs]):
    html_name: str = "h1"


class h2(Element[AnyChild, GlobalAttrs]):
    html_name: str = "h2"


class h3(Element[AnyChild, GlobalAttrs]):
    html_name: str = "h3"


class h4(Element[AnyChild, GlobalAttrs]):
    html_name: str = "h4"


class h5(Element[AnyChild, GlobalAttrs]):
    html_name: str = "h5"


class h6(Element[AnyChild, GlobalAttrs]):
    html_name: str = "h6"


class title(Element[PrimitiveChild, NoAttrs]):
    html_name: str = "title"


class link(Element[PrimitiveChild, HeadLinkAttrs]):
    html_name: str = "link"


class style(Element[PrimitiveChild, StyleAttrs]):
    html_name: str = "style"


class script(Element[PrimitiveChild, ScriptAttrs]):
    html_name: str = "script"
    always_pair: bool = True


class noscript(Element[AnyChild, GlobalAttrs]):
    html_name: str = "noscript"
    always_pair: bool = True


class meta(Element[PrimitiveChild, MetaAttrs]):
    html_name: str = "meta"


class head(Element[AnyChild, NoAttrs]):
    html_name: str = "head"


class body(Element[AnyChild, GlobalAttrs]):
    html_name: str = "body"


class footer(Element[AnyChild, GlobalAttrs]):
    html_name: str = "footer"


class html(ElementStrict[head, body, HtmlTagAttrs]):
    html_name: str = "html"


class iframe(Element[NoChild, IframeAttrs]):
    html_name: str = "iframe"


class article(Element[AnyChild, GlobalAttrs]):
    html_name: str = "article"


class address(Element[AnyChild, GlobalAttrs]):
    html_name: str = "address"


class caption(Element[AnyChild, GlobalAttrs]):
    html_name: str = "caption"


class col(Element[NoChild, ColAttrs]):
    html_name: str = "col"


class colgroup(Element[AnyChild, GlobalAttrs]):
    html_name: str = "colgroup"


class area(Element[NoChild, AreaAttrs]):
    html_name: str = "area"
