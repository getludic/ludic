from collections.abc import Callable, Mapping, MutableMapping, Sequence
from typing import Any, Unpack

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
    StyleAttrs,
    SvgAttrs,
    TdAttrs,
    TextAreaAttrs,
    ThAttrs,
    TimeAttrs,
    TrackAttrs,
    VideoAttrs,
)
from ludic.styles import Theme
from ludic.styles.types import GlobalStyles
from ludic.types import AnyChildren, ComplexChildren, NoChildren, PrimitiveChildren


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
    def __str__(self) -> str: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def is_simple(self) -> bool: ...
    def has_attributes(self) -> bool: ...
    def to_string(self) -> str: ...
    def to_html(self) -> str: ...

class div(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> div: ...

class span(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> span: ...

class main(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> main: ...

class p(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> p: ...

class a(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: HyperlinkAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[HyperlinkAttrs]) -> a: ...

class br(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> br: ...

class button(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: ButtonAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[ButtonAttrs]) -> button: ...

class label(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: LabelAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[LabelAttrs]) -> label: ...

class td(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: TdAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[TdAttrs]) -> td: ...

class th(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: ThAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[ThAttrs]) -> th: ...

class tr(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[GlobalAttrs]) -> tr: ...

class thead(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[GlobalAttrs]) -> thead: ...

class tbody(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[GlobalAttrs]) -> tbody: ...

class tfoot(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[GlobalAttrs]) -> tfoot: ...

class table(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[GlobalAttrs]) -> table: ...

class li(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: LiAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[LiAttrs]) -> li: ...

class ul(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[GlobalAttrs]) -> ul: ...

class ol(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: OlAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[OlAttrs]) -> ol: ...

class dt(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> dt: ...

class dd(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> dd: ...

class dl(BaseElement):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: ComplexChildren, **attrs: Unpack[GlobalAttrs]) -> dl: ...

class section(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> section: ...

class input(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: InputAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[InputAttrs]) -> input: ...

class output(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[OutputAttrs]) -> output: ...

class legend(BaseElement):
    children: tuple[PrimitiveChildren, ...]
    attrs: GlobalAttrs

    def __new__(
        *children: PrimitiveChildren, **attrs: Unpack[GlobalAttrs]
    ) -> legend: ...

class option(BaseElement):
    children: tuple[PrimitiveChildren, ...]
    attrs: OptionAttrs

    def __new__(
        *children: PrimitiveChildren, **attrs: Unpack[OptionAttrs]
    ) -> option: ...

class optgroup(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: OptgroupAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[OptgroupAttrs]) -> optgroup: ...

class select(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: SelectAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[SelectAttrs]) -> select: ...

class textarea(BaseElement):
    children: tuple[PrimitiveChildren, ...]
    attrs: TextAreaAttrs

    def __new__(
        *children: PrimitiveChildren, **attrs: Unpack[TextAreaAttrs]
    ) -> textarea: ...

class fieldset(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: FieldsetAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[FieldsetAttrs]) -> fieldset: ...

class form(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: FormAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[FormAttrs]) -> form: ...

class img(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: ImgAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[ImgAttrs]) -> img: ...

class svg(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: SvgAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[SvgAttrs]) -> svg: ...

class circle(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: CircleAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[CircleAttrs]) -> circle: ...

class line(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: LineAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[LineAttrs]) -> line: ...

class path(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: PathAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[PathAttrs]) -> path: ...

class polyline(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: PolylineAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[PolylineAttrs]) -> polyline: ...

class b(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> b: ...

class i(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> i: ...

class s(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> s: ...

class u(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> u: ...

class strong(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> strong: ...

class style(BaseElement):
    children: tuple[GlobalStyles | Callable[[Theme], GlobalStyles] | str]
    attrs: StyleAttrs

    def __init__(
        self,
        styles: GlobalStyles | Callable[[Theme], GlobalStyles] | str,
        theme: Theme | None = None,
        **attrs: Unpack[StyleAttrs],
    ) -> None:
        ...

class em(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> em: ...

class mark(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> mark: ...

class del_(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: DelAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[DelAttrs]) -> del_: ...

class ins(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: InsAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[InsAttrs]) -> ins: ...

class header(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> header: ...

class big(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> big: ...

class small(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> small: ...

class code(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> code: ...

class pre(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> pre: ...

class cite(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> cite: ...

class blockquote(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: BlockquoteAttrs

    def __new__(
        *children: AnyChildren, **attrs: Unpack[BlockquoteAttrs]
    ) -> blockquote: ...

class abbr(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> abbr: ...

class h1(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> h1: ...

class h2(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> h2: ...

class h3(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> h3: ...

class h4(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> h4: ...

class h5(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> h5: ...

class h6(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> h6: ...

class title(BaseElement):
    children: tuple[PrimitiveChildren, ...]
    attrs: NoAttrs

    def __new__(*children: PrimitiveChildren, **attrs: Unpack[NoAttrs]) -> title: ...

class link(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: HeadLinkAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[HeadLinkAttrs]) -> link: ...

class script(BaseElement):
    children: tuple[PrimitiveChildren, ...]
    attrs: ScriptAttrs

    def __new__(
        *children: PrimitiveChildren, **attrs: Unpack[ScriptAttrs]
    ) -> script: ...

class noscript(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> noscript: ...

class meta(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: MetaAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[MetaAttrs]) -> meta: ...

class head(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: NoAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[NoAttrs]) -> head: ...

class body(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> body: ...

class footer(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> footer: ...

class html(BaseElement):
    children: tuple[head, body]
    attrs: HtmlTagAttrs

    def __new__(
        *children: *tuple[head, body], **attrs: Unpack[HtmlTagAttrs]
    ) -> html: ...

class iframe(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: IframeAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[IframeAttrs]) -> iframe: ...

class article(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> article: ...

class address(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> address: ...

class caption(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> caption: ...

class col(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: ColAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[ColAttrs]) -> col: ...

class colgroup(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> colgroup: ...

class area(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: AreaAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[AreaAttrs]) -> area: ...

class aside(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> aside: ...

class source(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: SourceAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[SourceAttrs]) -> source: ...

class audio(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: AudioAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[AudioAttrs]) -> audio: ...

class base(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: BaseAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[BaseAttrs]) -> base: ...

class bdi(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> bdi: ...

class bdo(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> bdo: ...

class canvas(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: CanvasAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[CanvasAttrs]) -> canvas: ...

class data(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: DataAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[DataAttrs]) -> data: ...

class datalist(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> datalist: ...

class details(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: DetailsAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[DetailsAttrs]) -> details: ...

class dfn(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> dfn: ...

class dialog(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: DialogAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[DialogAttrs]) -> dialog: ...

class embed(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: EmbedAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[EmbedAttrs]) -> embed: ...

class figcaption(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> figcaption: ...

class figure(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> figure: ...

class hrgroup(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> hrgroup: ...

class hr(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> hr: ...

class kbd(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> kbd: ...

class map(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: MapAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[MapAttrs]) -> map: ...

class menu(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> menu: ...

class meter(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: MeterAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[MeterAttrs]) -> meter: ...

class nav(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> nav: ...

class object(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: ObjectAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[ObjectAttrs]) -> object: ...

class param(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: ParamAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[ParamAttrs]) -> param: ...

class picture(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> picture: ...

class progress(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: ProgressAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[ProgressAttrs]) -> progress: ...

class q(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: QAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[QAttrs]) -> q: ...

class rp(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> rp: ...

class rt(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> rt: ...

class ruby(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> ruby: ...

class samp(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> samp: ...

class search(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> search: ...

class sub(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> sub: ...

class summary(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> summary: ...

class sup(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> sup: ...

class template(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: HtmlAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[HtmlAttrs]) -> template: ...

class time(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: TimeAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[TimeAttrs]) -> time: ...

class track(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: TrackAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[TrackAttrs]) -> track: ...

class var(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> var: ...

class video(BaseElement):
    children: tuple[AnyChildren, ...]
    attrs: VideoAttrs

    def __new__(*children: AnyChildren, **attrs: Unpack[VideoAttrs]) -> video: ...

class wbr(BaseElement):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __new__(*children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> wbr: ...
