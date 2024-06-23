from collections.abc import Mapping, MutableMapping, Sequence
from typing import Any, Generic, Unpack

from ludic.attrs import (
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
    SvgAttrs,
    TdAttrs,
    TextAreaAttrs,
    ThAttrs,
    TimeAttrs,
    TrackAttrs,
    VideoAttrs,
)
from ludic.types import (
    AnyChildren,
    ComplexChildren,
    NoChildren,
    PrimitiveChildren,
    TAttrs,
    TChildren,
    TChildrenArgs,
)

class BaseElement:
    html_header: str | None
    html_name: str | None
    void_element: bool

    children: Sequence[Any]
    attrs: Mapping[str, Any]
    context: MutableMapping[str, Any]

    @property
    def text(self) -> str:
        """Get the text content of the element."""
    def __init__(self, *children: Any, **attrs: Any) -> None: ...
    def __str__(self) -> str: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def is_simple(self) -> bool: ...
    def has_attributes(self) -> bool: ...
    def to_html(self) -> str: ...

class Element(Generic[TChildren, TAttrs], BaseElement):
    """Base class for Ludic elements.

    Args:
        *children (TChild): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[TChildren, ...]
    attrs: TAttrs

class ElementStrict(Generic[*TChildrenArgs, TAttrs], BaseElement):
    """Base class for strict elements (elements with concrete types of children).

    Args:
        *children (*TChildTuple): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[*TChildrenArgs]
    attrs: TAttrs

class div(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class span(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class main(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class p(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class a(Element[AnyChildren, HyperlinkAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[HyperlinkAttrs]
    ) -> None: ...

class br(Element[NoChildren, GlobalAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None: ...

class button(Element[AnyChildren, ButtonAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[ButtonAttrs]
    ) -> None: ...

class label(Element[AnyChildren, LabelAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[LabelAttrs]) -> None: ...

class td(Element[AnyChildren, TdAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[TdAttrs]) -> None: ...

class th(Element[AnyChildren, ThAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[ThAttrs]) -> None: ...

class tr(Element[ComplexChildren, GlobalAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class thead(Element[ComplexChildren, GlobalAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class tbody(Element[ComplexChildren, GlobalAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class tfoot(Element[ComplexChildren, GlobalAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class table(Element[ComplexChildren, GlobalAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class li(Element[AnyChildren, LiAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[LiAttrs]) -> None: ...

class ul(Element[ComplexChildren, GlobalAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class ol(Element[ComplexChildren, OlAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[OlAttrs]
    ) -> None: ...

class dt(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class dd(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class dl(Element[ComplexChildren, GlobalAttrs]):
    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class section(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class input(Element[NoChildren, InputAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[InputAttrs]) -> None: ...

class output(Element[NoChildren, OutputAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[OutputAttrs]) -> None: ...

class legend(Element[PrimitiveChildren, GlobalAttrs]):
    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class option(Element[PrimitiveChildren, OptionAttrs]):
    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[OptionAttrs]
    ) -> None: ...

class optgroup(Element[AnyChildren, OptgroupAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[OptgroupAttrs]
    ) -> None: ...

class select(Element[AnyChildren, SelectAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[SelectAttrs]
    ) -> None: ...

class textarea(Element[PrimitiveChildren, TextAreaAttrs]):
    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[TextAreaAttrs]
    ) -> None: ...

class fieldset(Element[AnyChildren, FieldsetAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[FieldsetAttrs]
    ) -> None: ...

class form(Element[AnyChildren, FormAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[FormAttrs]) -> None: ...

class img(Element[NoChildren, ImgAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[ImgAttrs]) -> None: ...

class svg(Element[AnyChildren, SvgAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[SvgAttrs]) -> None: ...

class circle(Element[AnyChildren, CircleAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[CircleAttrs]
    ) -> None: ...

class line(Element[AnyChildren, LineAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[LineAttrs]) -> None: ...

class path(Element[AnyChildren, PathAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[PathAttrs]) -> None: ...

class polyline(Element[AnyChildren, PolylineAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[PolylineAttrs]
    ) -> None: ...

class b(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class i(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class s(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class u(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class strong(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class em(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class mark(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class del_(Element[AnyChildren, DelAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[DelAttrs]) -> None: ...

class ins(Element[AnyChildren, InsAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[InsAttrs]) -> None: ...

class header(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class big(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class small(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class code(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class pre(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class cite(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class blockquote(Element[AnyChildren, BlockquoteAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[BlockquoteAttrs]
    ) -> None: ...

class abbr(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class h1(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class h2(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class h3(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class h4(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class h5(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class h6(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class title(Element[PrimitiveChildren, NoAttrs]):
    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[NoAttrs]
    ) -> None: ...

class link(Element[NoChildren, HeadLinkAttrs]):
    def __init__(
        self, *children: NoChildren, **attrs: Unpack[HeadLinkAttrs]
    ) -> None: ...

class script(Element[PrimitiveChildren, ScriptAttrs]):
    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[ScriptAttrs]
    ) -> None: ...

class noscript(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class meta(Element[NoChildren, MetaAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[MetaAttrs]) -> None: ...

class head(Element[AnyChildren, NoAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[NoAttrs]) -> None: ...

class body(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class footer(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class html(ElementStrict[head, body, HtmlTagAttrs]):
    html_header = "<!doctype html>"

    def __init__(
        self, *children: *tuple[head, body], **attrs: Unpack[HtmlTagAttrs]
    ) -> None: ...

class iframe(Element[NoChildren, IframeAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[IframeAttrs]) -> None: ...

class article(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class address(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class caption(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class col(Element[NoChildren, ColAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[ColAttrs]) -> None: ...

class colgroup(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class area(Element[NoChildren, AreaAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[AreaAttrs]) -> None: ...

class aside(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class source(Element[NoChildren, SourceAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[SourceAttrs]) -> None: ...

class audio(Element[AnyChildren, AudioAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[AudioAttrs]) -> None: ...

class base(Element[NoChildren, BaseAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[BaseAttrs]) -> None: ...

class bdi(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class bdo(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class canvas(Element[AnyChildren, CanvasAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[CanvasAttrs]
    ) -> None: ...

class data(Element[AnyChildren, DataAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[DataAttrs]) -> None: ...

class datalist(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class details(Element[AnyChildren, DetailsAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[DetailsAttrs]
    ) -> None: ...

class dfn(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class dialog(Element[AnyChildren, DialogAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[DialogAttrs]
    ) -> None: ...

class embed(Element[NoChildren, EmbedAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[EmbedAttrs]) -> None: ...

class figcaption(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class figure(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class hrgroup(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class hr(Element[NoChildren, GlobalAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None: ...

class kbd(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class map(Element[AnyChildren, MapAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[MapAttrs]) -> None: ...

class menu(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class meter(Element[AnyChildren, MeterAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[MeterAttrs]) -> None: ...

class nav(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class object(Element[AnyChildren, ObjectAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[ObjectAttrs]
    ) -> None: ...

class param(Element[NoChildren, ParamAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[ParamAttrs]) -> None: ...

class picture(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class progress(Element[AnyChildren, ProgressAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[ProgressAttrs]
    ) -> None: ...

class q(Element[AnyChildren, QAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[QAttrs]) -> None: ...

class rp(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class rt(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class ruby(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class samp(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class search(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class sub(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class summary(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class sup(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class template(Element[AnyChildren, HtmlAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[HtmlAttrs]) -> None: ...

class time(Element[AnyChildren, TimeAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[TimeAttrs]) -> None: ...

class track(Element[NoChildren, TrackAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[TrackAttrs]) -> None: ...

class var(Element[AnyChildren, GlobalAttrs]):
    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None: ...

class video(Element[AnyChildren, VideoAttrs]):
    def __init__(self, *children: AnyChildren, **attrs: Unpack[VideoAttrs]) -> None: ...

class wbr(Element[NoChildren, GlobalAttrs]):
    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None: ...
