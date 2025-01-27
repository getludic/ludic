from collections.abc import Callable, Iterator
from typing import Generic, Self, Unpack

from .attrs import (
    AreaAttrs,
    AudioAttrs,
    BaseAttrs,
    BlockquoteAttrs,
    ButtonAttrs,
    CanvasAttrs,
    CircleAttrs,
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
    LineAttrs,
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
    PathAttrs,
    PolylineAttrs,
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
from .base import BaseElement
from .elements import Element, ElementStrict
from .styles import (
    format_styles,
    from_components,
    from_loaded,
)
from .styles.types import TTheme
from .types import (
    AnyChildren,
    ComplexChildren,
    CSSProperties,
    GlobalStyles,
    NoChildren,
    PrimitiveChildren,
)


class div(Element[AnyChildren, GlobalAttrs]):
    html_name = "div"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class span(Element[AnyChildren, GlobalAttrs]):
    html_name = "span"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class main(Element[AnyChildren, GlobalAttrs]):
    html_name = "main"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class p(Element[AnyChildren, GlobalAttrs]):
    html_name = "p"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class a(Element[AnyChildren, HyperlinkAttrs]):
    html_name = "a"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[HyperlinkAttrs]) -> None:
        super().__init__(*children, **attrs)


class br(Element[NoChildren, GlobalAttrs]):
    void_element = True
    html_name = "br"

    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class button(Element[AnyChildren, ButtonAttrs]):
    html_name = "button"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ButtonAttrs]) -> None:
        super().__init__(*children, **attrs)


class label(Element[AnyChildren, LabelAttrs]):
    html_name = "label"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[LabelAttrs]) -> None:
        super().__init__(*children, **attrs)


class td(Element[AnyChildren, TdAttrs]):
    html_name = "td"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[TdAttrs]) -> None:
        super().__init__(*children, **attrs)


class th(Element[AnyChildren, ThAttrs]):
    html_name = "th"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ThAttrs]) -> None:
        super().__init__(*children, **attrs)


class tr(Element[ComplexChildren, GlobalAttrs]):
    html_name = "tr"

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class thead(Element[ComplexChildren, GlobalAttrs]):
    html_name = "thead"

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class tbody(Element[ComplexChildren, GlobalAttrs]):
    html_name = "tbody"

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class tfoot(Element[ComplexChildren, GlobalAttrs]):
    html_name = "tfoot"

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class table(Element[ComplexChildren, GlobalAttrs]):
    html_name = "table"

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class li(Element[AnyChildren, LiAttrs]):
    html_name = "li"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[LiAttrs]) -> None:
        super().__init__(*children, **attrs)


class ul(Element[ComplexChildren, GlobalAttrs]):
    html_name = "ul"

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class ol(Element[ComplexChildren, OlAttrs]):
    html_name = "ol"

    def __init__(self, *children: ComplexChildren, **attrs: Unpack[OlAttrs]) -> None:
        super().__init__(*children, **attrs)


class dt(Element[AnyChildren, GlobalAttrs]):
    html_name = "dt"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class dd(Element[AnyChildren, GlobalAttrs]):
    html_name = "dd"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class dl(Element[ComplexChildren, GlobalAttrs]):
    html_name = "dl"

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class section(Element[AnyChildren, GlobalAttrs]):
    html_name = "section"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class input(Element[NoChildren, InputAttrs]):
    void_element = True
    html_name = "input"

    def __init__(self, *children: NoChildren, **attrs: Unpack[InputAttrs]) -> None:
        super().__init__(*children, **attrs)


class output(Element[NoChildren, OutputAttrs]):
    html_name = "output"

    def __init__(self, *children: NoChildren, **attrs: Unpack[OutputAttrs]) -> None:
        super().__init__(*children, **attrs)


class legend(Element[PrimitiveChildren, GlobalAttrs]):
    html_name = "legend"

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class option(Element[PrimitiveChildren, OptionAttrs]):
    html_name = "option"

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[OptionAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class optgroup(Element[AnyChildren, OptgroupAttrs]):
    html_name = "optgroup"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[OptgroupAttrs]) -> None:
        super().__init__(*children, **attrs)


class select(Element[AnyChildren, SelectAttrs]):
    html_name = "select"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[SelectAttrs]) -> None:
        super().__init__(*children, **attrs)


class textarea(Element[PrimitiveChildren, TextAreaAttrs]):
    html_name = "textarea"

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[TextAreaAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class fieldset(Element[AnyChildren, FieldsetAttrs]):
    html_name = "fieldset"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[FieldsetAttrs]) -> None:
        super().__init__(*children, **attrs)


class form(Element[AnyChildren, FormAttrs]):
    html_name = "form"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[FormAttrs]) -> None:
        super().__init__(*children, **attrs)


class img(Element[NoChildren, ImgAttrs]):
    void_element = True
    html_name = "img"

    def __init__(self, *children: NoChildren, **attrs: Unpack[ImgAttrs]) -> None:
        super().__init__(*children, **attrs)


class svg(Element[AnyChildren, SvgAttrs]):
    html_name = "svg"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[SvgAttrs]) -> None:
        super().__init__(*children, **attrs)


class circle(Element[AnyChildren, CircleAttrs]):
    html_name = "circle"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[CircleAttrs]) -> None:
        super().__init__(*children, **attrs)


class line(Element[AnyChildren, LineAttrs]):
    html_name = "line"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[LineAttrs]) -> None:
        super().__init__(*children, **attrs)


class path(Element[AnyChildren, PathAttrs]):
    html_name = "path"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[PathAttrs]) -> None:
        super().__init__(*children, **attrs)


class polyline(Element[AnyChildren, PolylineAttrs]):
    html_name = "polyline"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[PolylineAttrs]) -> None:
        super().__init__(*children, **attrs)


class b(Element[AnyChildren, GlobalAttrs]):
    html_name = "b"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class i(Element[AnyChildren, GlobalAttrs]):
    html_name = "i"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class s(Element[AnyChildren, GlobalAttrs]):
    html_name = "s"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class u(Element[AnyChildren, GlobalAttrs]):
    html_name = "u"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class strong(Element[AnyChildren, GlobalAttrs]):
    html_name = "strong"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class em(Element[AnyChildren, GlobalAttrs]):
    html_name = "em"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class mark(Element[AnyChildren, GlobalAttrs]):
    html_name = "mark"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class del_(Element[AnyChildren, DelAttrs]):
    html_name = "del"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DelAttrs]) -> None:
        super().__init__(*children, **attrs)


class ins(Element[AnyChildren, InsAttrs]):
    html_name = "ins"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[InsAttrs]) -> None:
        super().__init__(*children, **attrs)


class header(Element[AnyChildren, GlobalAttrs]):
    html_name = "header"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class big(Element[AnyChildren, GlobalAttrs]):
    html_name = "big"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class small(Element[AnyChildren, GlobalAttrs]):
    html_name = "small"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class code(Element[AnyChildren, GlobalAttrs]):
    html_name = "code"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class pre(Element[AnyChildren, GlobalAttrs]):
    html_name = "pre"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class cite(Element[AnyChildren, GlobalAttrs]):
    html_name = "cite"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class blockquote(Element[AnyChildren, BlockquoteAttrs]):
    html_name = "blockquote"

    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[BlockquoteAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class abbr(Element[AnyChildren, GlobalAttrs]):
    html_name = "abbr"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class h1(Element[AnyChildren, GlobalAttrs]):
    html_name = "h1"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class h2(Element[AnyChildren, GlobalAttrs]):
    html_name = "h2"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class h3(Element[AnyChildren, GlobalAttrs]):
    html_name = "h3"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class h4(Element[AnyChildren, GlobalAttrs]):
    html_name = "h4"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class h5(Element[AnyChildren, GlobalAttrs]):
    html_name = "h5"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class h6(Element[AnyChildren, GlobalAttrs]):
    html_name = "h6"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class title(Element[PrimitiveChildren, NoAttrs]):
    html_name = "title"

    def __init__(self, *children: PrimitiveChildren, **attrs: Unpack[NoAttrs]) -> None:
        super().__init__(*children, **attrs)


class link(Element[NoChildren, HeadLinkAttrs]):
    void_element = True
    html_name = "link"

    def __init__(self, *children: NoChildren, **attrs: Unpack[HeadLinkAttrs]) -> None:
        super().__init__(*children, **attrs)


class style(Generic[TTheme], BaseElement, GlobalStyles):
    html_name = "style"

    children: tuple[GlobalStyles | Callable[[TTheme], GlobalStyles] | str]
    attrs: StyleAttrs

    def __init__(
        self,
        styles: GlobalStyles | Callable[[TTheme], GlobalStyles] | str,
        theme: TTheme | None = None,
        **attrs: Unpack[StyleAttrs],
    ) -> None:
        super().__init__(styles, **attrs)

        if theme:
            self.context["theme"] = theme

    @classmethod
    def use(cls, styles: GlobalStyles | Callable[[TTheme], GlobalStyles]) -> Self:
        return cls(styles)

    @classmethod
    def from_components(
        cls, *components: type[BaseElement], theme: TTheme | None = None
    ) -> Self:
        return cls(from_components(*components, theme=theme), type="text/css")

    @classmethod
    def load(cls, cache: bool = False, theme: TTheme | None = None) -> Self:
        return cls(from_loaded(cache=cache, theme=theme), type="text/css")

    def __getitem__(self, key: str | tuple[str, ...]) -> CSSProperties | GlobalStyles:
        return self.styles[key]

    def __iter__(self) -> Iterator[str | tuple[str, ...]]:
        return iter(self.styles.keys())

    def __len__(self) -> int:
        return len(self.styles)

    @property
    def styles(self) -> GlobalStyles:
        if isinstance(self.children[0], str):
            return {}
        elif callable(self.children[0]):
            return self.children[0](self.context["theme"])
        else:
            return self.children[0]

    @styles.setter
    def styles(self, value: GlobalStyles) -> None:
        self.children = (value,)

    def to_html(self) -> str:
        attributes = ""
        if formatted_attrs := self._format_attributes():
            attributes = f" {formatted_attrs}"

        if isinstance(self.children[0], str):
            css_styles = self.children[0]
        else:
            css_styles = format_styles(self.styles)

        return (
            f"<{self.html_name}{attributes}>\n"
            f"{css_styles}\n"
            f"</{self.html_name}>"
        )  # fmt: off


class script(Element[PrimitiveChildren, ScriptAttrs]):
    html_name = "script"

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[ScriptAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class noscript(Element[AnyChildren, GlobalAttrs]):
    html_name = "noscript"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class meta(Element[NoChildren, MetaAttrs]):
    void_element = True
    html_name = "meta"

    def __init__(self, *children: NoChildren, **attrs: Unpack[MetaAttrs]) -> None:
        super().__init__(*children, **attrs)


class head(Element[AnyChildren, NoAttrs]):
    html_name = "head"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[NoAttrs]) -> None:
        super().__init__(*children, **attrs)


class body(Element[AnyChildren, GlobalAttrs]):
    html_name = "body"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class footer(Element[AnyChildren, GlobalAttrs]):
    html_name = "footer"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class html(ElementStrict[head, body, HtmlTagAttrs]):
    html_header = "<!doctype html>"
    html_name = "html"

    def __init__(
        self, *children: *tuple[head, body], **attrs: Unpack[HtmlTagAttrs]
    ) -> None:
        super().__init__(*children, **attrs)


class iframe(Element[NoChildren, IframeAttrs]):
    html_name = "iframe"

    def __init__(self, *children: NoChildren, **attrs: Unpack[IframeAttrs]) -> None:
        super().__init__(*children, **attrs)


class article(Element[AnyChildren, GlobalAttrs]):
    html_name = "article"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class address(Element[AnyChildren, GlobalAttrs]):
    html_name = "address"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class caption(Element[AnyChildren, GlobalAttrs]):
    html_name = "caption"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class col(Element[NoChildren, ColAttrs]):
    void_element = True
    html_name = "col"

    def __init__(self, *children: NoChildren, **attrs: Unpack[ColAttrs]) -> None:
        super().__init__(*children, **attrs)


class colgroup(Element[AnyChildren, GlobalAttrs]):
    html_name = "colgroup"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class area(Element[NoChildren, AreaAttrs]):
    void_element = True
    html_name = "area"

    def __init__(self, *children: NoChildren, **attrs: Unpack[AreaAttrs]) -> None:
        super().__init__(*children, **attrs)


class aside(Element[AnyChildren, GlobalAttrs]):
    html_name = "aside"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class source(Element[NoChildren, SourceAttrs]):
    void_element = True
    html_name = "source"

    def __init__(self, *children: NoChildren, **attrs: Unpack[SourceAttrs]) -> None:
        super().__init__(*children, **attrs)


class audio(Element[AnyChildren, AudioAttrs]):
    html_name = "audio"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[AudioAttrs]) -> None:
        super().__init__(*children, **attrs)


class base(Element[NoChildren, BaseAttrs]):
    void_element = True
    html_name = "base"

    def __init__(self, *children: NoChildren, **attrs: Unpack[BaseAttrs]) -> None:
        super().__init__(*children, **attrs)


class bdi(Element[AnyChildren, GlobalAttrs]):
    html_name = "bdi"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class bdo(Element[AnyChildren, GlobalAttrs]):
    html_name = "bdo"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class canvas(Element[AnyChildren, CanvasAttrs]):
    html_name = "canvas"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[CanvasAttrs]) -> None:
        super().__init__(*children, **attrs)


class data(Element[AnyChildren, DataAttrs]):
    html_name = "data"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DataAttrs]) -> None:
        super().__init__(*children, **attrs)


class datalist(Element[AnyChildren, GlobalAttrs]):
    html_name = "datalist"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class details(Element[AnyChildren, DetailsAttrs]):
    html_name = "details"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DetailsAttrs]) -> None:
        super().__init__(*children, **attrs)


class dfn(Element[AnyChildren, GlobalAttrs]):
    html_name = "dfn"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class dialog(Element[AnyChildren, DialogAttrs]):
    html_name = "dialog"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DialogAttrs]) -> None:
        super().__init__(*children, **attrs)


class embed(Element[NoChildren, EmbedAttrs]):
    void_element = True
    html_name = "embed"

    def __init__(self, *children: NoChildren, **attrs: Unpack[EmbedAttrs]) -> None:
        super().__init__(*children, **attrs)


class figcaption(Element[AnyChildren, GlobalAttrs]):
    html_name = "figcaption"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class figure(Element[AnyChildren, GlobalAttrs]):
    html_name = "figure"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class hrgroup(Element[AnyChildren, GlobalAttrs]):
    html_name = "hrgroup"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class hr(Element[NoChildren, GlobalAttrs]):
    void_element = True
    html_name = "hr"

    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class kbd(Element[AnyChildren, GlobalAttrs]):
    html_name = "kbd"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class map(Element[AnyChildren, MapAttrs]):
    html_name = "map"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[MapAttrs]) -> None:
        super().__init__(*children, **attrs)


class menu(Element[AnyChildren, GlobalAttrs]):
    html_name = "menu"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class meter(Element[AnyChildren, MeterAttrs]):
    html_name = "meter"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[MeterAttrs]) -> None:
        super().__init__(*children, **attrs)


class nav(Element[AnyChildren, GlobalAttrs]):
    html_name = "nav"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class object(Element[AnyChildren, ObjectAttrs]):
    html_name = "object"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ObjectAttrs]) -> None:
        super().__init__(*children, **attrs)


class param(Element[NoChildren, ParamAttrs]):
    void_element = True
    html_name = "param"

    def __init__(self, *children: NoChildren, **attrs: Unpack[ParamAttrs]) -> None:
        super().__init__(*children, **attrs)


class picture(Element[AnyChildren, GlobalAttrs]):
    html_name = "picture"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class progress(Element[AnyChildren, ProgressAttrs]):
    html_name = "progress"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ProgressAttrs]) -> None:
        super().__init__(*children, **attrs)


class q(Element[AnyChildren, QAttrs]):
    html_name = "q"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[QAttrs]) -> None:
        super().__init__(*children, **attrs)


class rp(Element[AnyChildren, GlobalAttrs]):
    html_name = "rp"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class rt(Element[AnyChildren, GlobalAttrs]):
    html_name = "rt"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class ruby(Element[AnyChildren, GlobalAttrs]):
    html_name = "ruby"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class samp(Element[AnyChildren, GlobalAttrs]):
    html_name = "samp"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class search(Element[AnyChildren, GlobalAttrs]):
    html_name = "search"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class sub(Element[AnyChildren, GlobalAttrs]):
    html_name = "sub"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class summary(Element[AnyChildren, GlobalAttrs]):
    html_name = "summary"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class sup(Element[AnyChildren, GlobalAttrs]):
    html_name = "sup"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class template(Element[AnyChildren, HtmlAttrs]):
    html_name = "template"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[HtmlAttrs]) -> None:
        super().__init__(*children, **attrs)


class time(Element[AnyChildren, TimeAttrs]):
    html_name = "time"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[TimeAttrs]) -> None:
        super().__init__(*children, **attrs)


class track(Element[NoChildren, TrackAttrs]):
    void_element = True
    html_name = "track"

    def __init__(self, *children: NoChildren, **attrs: Unpack[TrackAttrs]) -> None:
        super().__init__(*children, **attrs)


class var(Element[AnyChildren, GlobalAttrs]):
    html_name = "var"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)


class video(Element[AnyChildren, VideoAttrs]):
    html_name = "video"

    def __init__(self, *children: AnyChildren, **attrs: Unpack[VideoAttrs]) -> None:
        super().__init__(*children, **attrs)


class wbr(Element[NoChildren, GlobalAttrs]):
    void_element = True
    html_name = "wbr"

    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        super().__init__(*children, **attrs)
