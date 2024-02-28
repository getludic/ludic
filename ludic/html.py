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
    AllowAny,
    Element,
    ElementStrict,
    NotAllowed,
    OnlyComplex,
    OnlyPrimitive,
)


class div(Element[AllowAny, GlobalAttrs]):
    html_name = "div"


class span(Element[AllowAny, GlobalAttrs]):
    html_name = "span"


class main(Element[AllowAny, GlobalAttrs]):
    html_name = "main"


class p(Element[AllowAny, GlobalAttrs]):
    html_name = "p"


class a(Element[AllowAny, HyperlinkAttrs]):
    html_name = "a"


class br(Element[NotAllowed, GlobalAttrs]):
    html_name = "br"


class button(Element[AllowAny, ButtonAttrs]):
    html_name = "button"


class label(Element[AllowAny, LabelAttrs]):
    html_name = "label"


class td(Element[AllowAny, TdAttrs]):
    html_name = "td"


class th(Element[AllowAny, ThAttrs]):
    html_name = "th"


class tr(Element[OnlyComplex, GlobalAttrs]):
    html_name = "tr"


class thead(Element[OnlyComplex, GlobalAttrs]):
    html_name = "thead"


class tbody(Element[OnlyComplex, GlobalAttrs]):
    html_name = "tbody"


class tfoot(Element[OnlyComplex, GlobalAttrs]):
    html_name = "tfoot"


class table(Element[OnlyComplex, GlobalAttrs]):
    html_name = "table"


class li(Element[AllowAny, LiAttrs]):
    html_name = "li"


class ul(Element[OnlyComplex, GlobalAttrs]):
    html_name = "ul"


class ol(Element[OnlyComplex, GlobalAttrs]):
    html_name = "ol"


class dt(Element[AllowAny, GlobalAttrs]):
    html_name = "dt"


class dd(Element[AllowAny, GlobalAttrs]):
    html_name = "dd"


class dl(Element[OnlyComplex, GlobalAttrs]):
    html_name = "dl"


class section(Element[AllowAny, GlobalAttrs]):
    html_name = "section"


class input(Element[NotAllowed, InputAttrs]):
    html_name = "input"


class output(Element[NotAllowed, OutputAttrs]):
    html_name = "output"


class legend(Element[OnlyPrimitive, GlobalAttrs]):
    html_name = "legend"


class option(Element[OnlyPrimitive, OptionAttrs]):
    html_name = "option"


class optgroup(Element[AllowAny, OptgroupAttrs]):
    html_name = "optgroup"


class select(Element[AllowAny, SelectAttrs]):
    html_name = "select"


class textarea(Element[OnlyPrimitive, TextAreaAttrs]):
    html_name = "textarea"


class fieldset(Element[AllowAny, FieldsetAttrs]):
    html_name = "fieldset"


class form(Element[AllowAny, FormAttrs]):
    html_name = "form"


class img(Element[NotAllowed, ImgAttrs]):
    html_name = "img"


class svg(Element[AllowAny, SvgAttrs]):
    html_name = "svg"


class b(Element[AllowAny, GlobalAttrs]):
    html_name = "b"


class i(Element[AllowAny, GlobalAttrs]):
    html_name = "i"


class s(Element[AllowAny, GlobalAttrs]):
    html_name = "s"


class u(Element[AllowAny, GlobalAttrs]):
    html_name = "u"


class strong(Element[AllowAny, GlobalAttrs]):
    html_name = "strong"


class em(Element[AllowAny, GlobalAttrs]):
    html_name = "em"


class mark(Element[AllowAny, GlobalAttrs]):
    html_name = "mark"


class del_(Element[AllowAny, DelAttrs]):
    html_name = "del"


class ins(Element[AllowAny, InsAttrs]):
    html_name = "ins"


class header(Element[AllowAny, GlobalAttrs]):
    html_name = "header"


class big(Element[AllowAny, GlobalAttrs]):
    html_name = "big"


class small(Element[AllowAny, GlobalAttrs]):
    html_name = "small"


class code(Element[AllowAny, GlobalAttrs]):
    html_name = "code"


class pre(Element[AllowAny, GlobalAttrs]):
    html_name = "pre"


class cite(Element[AllowAny, GlobalAttrs]):
    html_name = "cite"


class blockquote(Element[AllowAny, BlockquoteAttrs]):
    html_name = "blockquote"


class abbr(Element[AllowAny, GlobalAttrs]):
    html_name = "abbr"


class h1(Element[AllowAny, GlobalAttrs]):
    html_name = "h1"


class h2(Element[AllowAny, GlobalAttrs]):
    html_name = "h2"


class h3(Element[AllowAny, GlobalAttrs]):
    html_name = "h3"


class h4(Element[AllowAny, GlobalAttrs]):
    html_name = "h4"


class h5(Element[AllowAny, GlobalAttrs]):
    html_name = "h5"


class h6(Element[AllowAny, GlobalAttrs]):
    html_name = "h6"


class title(Element[OnlyPrimitive, NoAttrs]):
    html_name = "title"


class link(Element[OnlyPrimitive, HeadLinkAttrs]):
    html_name = "link"


class style(Element[OnlyPrimitive, StyleAttrs]):
    html_name = "style"


class script(Element[OnlyPrimitive, ScriptAttrs]):
    html_name = "script"
    always_pair = True


class noscript(Element[AllowAny, GlobalAttrs]):
    html_name = "noscript"
    always_pair = True


class meta(Element[OnlyPrimitive, MetaAttrs]):
    html_name = "meta"


class head(Element[AllowAny, NoAttrs]):
    html_name = "head"


class body(Element[AllowAny, GlobalAttrs]):
    html_name = "body"


class footer(Element[AllowAny, GlobalAttrs]):
    html_name = "footer"


class html(ElementStrict[head, body, HtmlTagAttrs]):
    html_name = "html"


class iframe(Element[NotAllowed, IframeAttrs]):
    html_name = "iframe"


class article(Element[AllowAny, GlobalAttrs]):
    html_name = "article"


class address(Element[AllowAny, GlobalAttrs]):
    html_name = "address"


class caption(Element[AllowAny, GlobalAttrs]):
    html_name = "caption"


class col(Element[NotAllowed, ColAttrs]):
    html_name = "col"


class colgroup(Element[AllowAny, GlobalAttrs]):
    html_name = "colgroup"


class area(Element[NotAllowed, AreaAttrs]):
    html_name = "area"
