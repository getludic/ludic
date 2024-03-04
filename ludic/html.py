from typing import Self, Unpack

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
from .styles import collect_from_components, collect_from_loaded, format_styles
from .types import (
    AnyChildren,
    BaseElement,
    ComplexChildren,
    Element,
    ElementStrict,
    GlobalStyles,
    NoChildren,
    PrimitiveChildren,
)


class div(Element[AnyChildren, GlobalAttrs]):
    html_name = "div"


class span(Element[AnyChildren, GlobalAttrs]):
    html_name = "span"


class main(Element[AnyChildren, GlobalAttrs]):
    html_name = "main"


class p(Element[AnyChildren, GlobalAttrs]):
    html_name = "p"


class a(Element[AnyChildren, HyperlinkAttrs]):
    html_name = "a"


class br(Element[NoChildren, GlobalAttrs]):
    html_name = "br"


class button(Element[AnyChildren, ButtonAttrs]):
    html_name = "button"


class label(Element[AnyChildren, LabelAttrs]):
    html_name = "label"


class td(Element[AnyChildren, TdAttrs]):
    html_name = "td"


class th(Element[AnyChildren, ThAttrs]):
    html_name = "th"


class tr(Element[ComplexChildren, GlobalAttrs]):
    html_name = "tr"


class thead(Element[ComplexChildren, GlobalAttrs]):
    html_name = "thead"


class tbody(Element[ComplexChildren, GlobalAttrs]):
    html_name = "tbody"


class tfoot(Element[ComplexChildren, GlobalAttrs]):
    html_name = "tfoot"


class table(Element[ComplexChildren, GlobalAttrs]):
    html_name = "table"


class li(Element[AnyChildren, LiAttrs]):
    html_name = "li"


class ul(Element[ComplexChildren, GlobalAttrs]):
    html_name = "ul"


class ol(Element[ComplexChildren, GlobalAttrs]):
    html_name = "ol"


class dt(Element[AnyChildren, GlobalAttrs]):
    html_name = "dt"


class dd(Element[AnyChildren, GlobalAttrs]):
    html_name = "dd"


class dl(Element[ComplexChildren, GlobalAttrs]):
    html_name = "dl"


class section(Element[AnyChildren, GlobalAttrs]):
    html_name = "section"


class input(Element[NoChildren, InputAttrs]):
    html_name = "input"


class output(Element[NoChildren, OutputAttrs]):
    html_name = "output"


class legend(Element[PrimitiveChildren, GlobalAttrs]):
    html_name = "legend"


class option(Element[PrimitiveChildren, OptionAttrs]):
    html_name = "option"


class optgroup(Element[AnyChildren, OptgroupAttrs]):
    html_name = "optgroup"


class select(Element[AnyChildren, SelectAttrs]):
    html_name = "select"


class textarea(Element[PrimitiveChildren, TextAreaAttrs]):
    html_name = "textarea"


class fieldset(Element[AnyChildren, FieldsetAttrs]):
    html_name = "fieldset"


class form(Element[AnyChildren, FormAttrs]):
    html_name = "form"


class img(Element[NoChildren, ImgAttrs]):
    html_name = "img"


class svg(Element[AnyChildren, SvgAttrs]):
    html_name = "svg"


class b(Element[AnyChildren, GlobalAttrs]):
    html_name = "b"


class i(Element[AnyChildren, GlobalAttrs]):
    html_name = "i"


class s(Element[AnyChildren, GlobalAttrs]):
    html_name = "s"


class u(Element[AnyChildren, GlobalAttrs]):
    html_name = "u"


class strong(Element[AnyChildren, GlobalAttrs]):
    html_name = "strong"


class em(Element[AnyChildren, GlobalAttrs]):
    html_name = "em"


class mark(Element[AnyChildren, GlobalAttrs]):
    html_name = "mark"


class del_(Element[AnyChildren, DelAttrs]):
    html_name = "del"


class ins(Element[AnyChildren, InsAttrs]):
    html_name = "ins"


class header(Element[AnyChildren, GlobalAttrs]):
    html_name = "header"


class big(Element[AnyChildren, GlobalAttrs]):
    html_name = "big"


class small(Element[AnyChildren, GlobalAttrs]):
    html_name = "small"


class code(Element[AnyChildren, GlobalAttrs]):
    html_name = "code"


class pre(Element[AnyChildren, GlobalAttrs]):
    html_name = "pre"


class cite(Element[AnyChildren, GlobalAttrs]):
    html_name = "cite"


class blockquote(Element[AnyChildren, BlockquoteAttrs]):
    html_name = "blockquote"


class abbr(Element[AnyChildren, GlobalAttrs]):
    html_name = "abbr"


class h1(Element[AnyChildren, GlobalAttrs]):
    html_name = "h1"


class h2(Element[AnyChildren, GlobalAttrs]):
    html_name = "h2"


class h3(Element[AnyChildren, GlobalAttrs]):
    html_name = "h3"


class h4(Element[AnyChildren, GlobalAttrs]):
    html_name = "h4"


class h5(Element[AnyChildren, GlobalAttrs]):
    html_name = "h5"


class h6(Element[AnyChildren, GlobalAttrs]):
    html_name = "h6"


class title(Element[PrimitiveChildren, NoAttrs]):
    html_name = "title"


class link(Element[PrimitiveChildren, HeadLinkAttrs]):
    html_name = "link"


class style(BaseElement):
    html_name = "style"

    children: tuple[GlobalStyles]
    attrs: StyleAttrs

    def __init__(self, styles: GlobalStyles, **attrs: Unpack[StyleAttrs]) -> None:
        self.children = (styles,)
        self.attrs = attrs

    @classmethod
    def from_components(cls, *components: type[BaseElement]) -> Self:
        return cls(collect_from_components(*components))

    @classmethod
    def load(cls) -> Self:
        return cls(collect_from_loaded())

    def to_html(self) -> str:
        dom: BaseElement = self
        while dom != (rendered_dom := dom.render()):
            dom = rendered_dom

        attributes = ""
        if formatted_attrs := dom._format_attributes():
            attributes = f" {formatted_attrs}"

        return (
            f"<{dom.html_name}{attributes}>\n"
            f"{format_styles(dom.children[0])}\n"
            f"</{dom.html_name}>"
        )

    def render(self) -> BaseElement:
        return self


class script(Element[PrimitiveChildren, ScriptAttrs]):
    html_name = "script"
    always_pair = True


class noscript(Element[AnyChildren, GlobalAttrs]):
    html_name = "noscript"
    always_pair = True


class meta(Element[PrimitiveChildren, MetaAttrs]):
    html_name = "meta"


class head(Element[AnyChildren, NoAttrs]):
    html_name = "head"


class body(Element[AnyChildren, GlobalAttrs]):
    html_name = "body"


class footer(Element[AnyChildren, GlobalAttrs]):
    html_name = "footer"


class html(ElementStrict[head, body, HtmlTagAttrs]):
    html_name = "html"


class iframe(Element[NoChildren, IframeAttrs]):
    html_name = "iframe"


class article(Element[AnyChildren, GlobalAttrs]):
    html_name = "article"


class address(Element[AnyChildren, GlobalAttrs]):
    html_name = "address"


class caption(Element[AnyChildren, GlobalAttrs]):
    html_name = "caption"


class col(Element[NoChildren, ColAttrs]):
    html_name = "col"


class colgroup(Element[AnyChildren, GlobalAttrs]):
    html_name = "colgroup"


class area(Element[NoChildren, AreaAttrs]):
    html_name = "area"
