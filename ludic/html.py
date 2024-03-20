from typing import Self, Unpack, override

from .attrs import (
    AreaAttrs,
    AudioAttrs,
    BaseAttrs,
    BlockquoteAttrs,
    ButtonAttrs,
    CanvasAttrs,
    ColAttrs,
    DataAttrs,
    DelAttrs,
    DetailsAttrs,
    DialogAttrs,
    EmbedAttrs,
    FieldsetAttrs,
    FormAttrs,
    GlobalAttrs,
    HeadLinkAttrs,
    HtmlAttrs,
    HtmlTagAttrs,
    HyperlinkAttrs,
    IframeAttrs,
    ImgAttrs,
    InputAttrs,
    InsAttrs,
    LabelAttrs,
    LiAttrs,
    MapAttrs,
    MetaAttrs,
    MeterAttrs,
    NoAttrs,
    ObjectAttrs,
    OlAttrs,
    OptgroupAttrs,
    OptionAttrs,
    OutputAttrs,
    ParamAttrs,
    ProgressAttrs,
    QAttrs,
    ScriptAttrs,
    SelectAttrs,
    SourceAttrs,
    StyleAttrs,
    SvgAttrs,
    TdAttrs,
    TextAreaAttrs,
    ThAttrs,
    TimeAttrs,
    TrackAttrs,
    VideoAttrs,
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


class ol(Element[ComplexChildren, OlAttrs]):
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

    children: tuple[GlobalStyles | str]
    attrs: StyleAttrs

    def __init__(self, styles: GlobalStyles | str, **attrs: Unpack[StyleAttrs]) -> None:
        self.children = (styles,)
        self.attrs = attrs

    @classmethod
    def from_components(cls, *components: type[BaseElement]) -> Self:
        return cls(collect_from_components(*components))

    @classmethod
    def load(cls, cache: bool = False) -> Self:
        return cls(collect_from_loaded(cache=cache))

    def to_html(self) -> str:
        dom: BaseElement = self
        while dom != (rendered_dom := dom.render()):
            dom = rendered_dom

        attributes = ""
        if formatted_attrs := dom._format_attributes():
            attributes = f" {formatted_attrs}"

        css_styles = self.children[0]
        if not isinstance(css_styles, str):
            css_styles = format_styles(dom.children[0])

        return (
            f"<{dom.html_name}{attributes}>\n" f"{css_styles}\n" f"</{dom.html_name}>"
        )

    @override
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
    html_header = "<!doctype html>"
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


class aside(Element[AnyChildren, GlobalAttrs]):
    html_name = "aside"


class source(Element[NoChildren, SourceAttrs]):
    html_name = "source"


class audio(Element[AnyChildren, AudioAttrs]):
    html_name = "audio"


class base(Element[NoChildren, BaseAttrs]):
    html_name = "base"


class bdi(Element[AnyChildren, GlobalAttrs]):
    html_name = "bdi"


class bdo(Element[AnyChildren, GlobalAttrs]):
    html_name = "bdo"


class canvas(Element[AnyChildren, CanvasAttrs]):
    html_name = "canvas"


class data(Element[AnyChildren, DataAttrs]):
    html_name = "data"


class datalist(Element[AnyChildren, GlobalAttrs]):
    html_name = "datalist"


class details(Element[AnyChildren, DetailsAttrs]):
    html_name = "details"


class dfn(Element[AnyChildren, GlobalAttrs]):
    html_name = "dfn"


class dialog(Element[AnyChildren, DialogAttrs]):
    html_name = "dialog"


class embed(Element[NoChildren, EmbedAttrs]):
    html_name = "embed"


class figcaption(Element[AnyChildren, GlobalAttrs]):
    html_name = "figcaption"


class figure(Element[AnyChildren, GlobalAttrs]):
    html_name = "figure"


class hrgroup(Element[AnyChildren, GlobalAttrs]):
    html_name = "hrgroup"


class hr(Element[NoChildren, GlobalAttrs]):
    html_name = "hr"


class kbd(Element[AnyChildren, GlobalAttrs]):
    html_name = "kbd"


class map(Element[AnyChildren, MapAttrs]):
    html_name = "map"


class menu(Element[AnyChildren, GlobalAttrs]):
    html_name = "menu"


class meter(Element[AnyChildren, MeterAttrs]):
    html_name = "meter"


class nav(Element[AnyChildren, GlobalAttrs]):
    html_name = "nav"


class object(Element[AnyChildren, ObjectAttrs]):
    html_name = "object"


class param(Element[NoChildren, ParamAttrs]):
    html_name = "param"


class picture(Element[AnyChildren, GlobalAttrs]):
    html_name = "picture"


class progress(Element[AnyChildren, ProgressAttrs]):
    html_name = "progress"


class q(Element[AnyChildren, QAttrs]):
    html_name = "q"


class rp(Element[AnyChildren, GlobalAttrs]):
    html_name = "rp"


class rt(Element[AnyChildren, GlobalAttrs]):
    html_name = "rt"


class ruby(Element[AnyChildren, GlobalAttrs]):
    html_name = "ruby"


class samp(Element[AnyChildren, GlobalAttrs]):
    html_name = "samp"


class search(Element[AnyChildren, GlobalAttrs]):
    html_name = "search"


class sub(Element[AnyChildren, GlobalAttrs]):
    html_name = "sub"


class summary(Element[AnyChildren, GlobalAttrs]):
    html_name = "summary"


class sup(Element[AnyChildren, GlobalAttrs]):
    html_name = "sup"


class template(Element[AnyChildren, HtmlAttrs]):
    html_name = "template"


class time(Element[AnyChildren, TimeAttrs]):
    html_name = "time"


class track(Element[NoChildren, TrackAttrs]):
    html_name = "track"


class var(Element[AnyChildren, GlobalAttrs]):
    html_name = "var"


class video(Element[AnyChildren, VideoAttrs]):
    html_name = "video"


class wbr(Element[NoChildren, GlobalAttrs]):
    html_name = "wbr"
