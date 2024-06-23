from collections.abc import Callable, Iterator
from typing import Self, Unpack

import ludicrous

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

from .format import format_attrs
from .styles import (
    Theme,
    format_styles,
    from_components,
    from_loaded,
    get_default_theme,
)
from .styles.types import CSSProperties, GlobalStyles
from .types import AnyChildren, ComplexChildren, NoChildren, PrimitiveChildren


class style(ludicrous.BaseElement, GlobalStyles):
    children: tuple[GlobalStyles | Callable[[Theme], GlobalStyles] | str]
    attrs: StyleAttrs

    def __init__(
        self,
        styles: GlobalStyles | Callable[[Theme], GlobalStyles] | str,
        theme: Theme | None = None,
        **attrs: Unpack[StyleAttrs],
    ) -> None:
        self.html_name = "style"
        self.html_header = None

        self.children = (styles,)
        self.attrs = attrs
        self.context = {}

        if theme:
            self.context["theme"] = theme

    @classmethod
    def use(cls, styles: GlobalStyles | Callable[[Theme], GlobalStyles]) -> Self:
        return cls(styles)

    @classmethod
    def from_components(
        cls, *components: type[ludicrous.BaseElement], theme: Theme | None = None
    ) -> Self:
        return cls(from_components(*components, theme=theme), type="text/css")

    @classmethod
    def load(cls, cache: bool = False, theme: Theme | None = None) -> Self:
        return cls(from_loaded(cache=cache, theme=theme), type="text/css")

    def __getitem__(self, key: str | tuple[str, ...]) -> CSSProperties | GlobalStyles:
        return self.styles[key]

    def __iter__(self) -> Iterator[str | tuple[str, ...]]:
        return iter(self.styles.keys())

    def __len__(self) -> int:
        return len(self.styles)

    @property
    def theme(self) -> Theme:
        return self.context.get("theme", get_default_theme())

    @property
    def styles(self) -> GlobalStyles:
        if isinstance(self.children[0], str):
            return {}
        elif callable(self.children[0]):
            return self.children[0](self.theme)
        else:
            return self.children[0]

    @styles.setter
    def styles(self, value: GlobalStyles) -> None:
        self.children = (value,)

    def to_html(self) -> str:
        attributes = ""
        if formatted_attrs := format_attrs(type(self), self.attrs):
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


class div(ludicrous.div):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class span(ludicrous.span):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class main(ludicrous.main):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class p(ludicrous.p):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class a(ludicrous.a):
    children: tuple[AnyChildren, ...]
    attrs: HyperlinkAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[HyperlinkAttrs]) -> None:
        pass


class br(ludicrous.br):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class button(ludicrous.button):
    children: tuple[AnyChildren, ...]
    attrs: ButtonAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ButtonAttrs]) -> None:
        pass


class label(ludicrous.label):
    children: tuple[AnyChildren, ...]
    attrs: LabelAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[LabelAttrs]) -> None:
        pass


class td(ludicrous.td):
    children: tuple[AnyChildren, ...]
    attrs: TdAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[TdAttrs]) -> None:
        pass


class th(ludicrous.th):
    children: tuple[AnyChildren, ...]
    attrs: ThAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ThAttrs]) -> None:
        pass


class tr(ludicrous.tr):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class thead(ludicrous.thead):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class tbody(ludicrous.tbody):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class tfoot(ludicrous.tfoot):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class table(ludicrous.table):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class li(ludicrous.li):
    children: tuple[AnyChildren, ...]
    attrs: LiAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[LiAttrs]) -> None:
        pass


class ul(ludicrous.ul):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class ol(ludicrous.ol):
    children: tuple[ComplexChildren, ...]
    attrs: OlAttrs

    def __init__(self, *children: ComplexChildren, **attrs: Unpack[OlAttrs]) -> None:
        pass


class dt(ludicrous.dt):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class dd(ludicrous.dd):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class dl(ludicrous.dl):
    children: tuple[ComplexChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: ComplexChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class section(ludicrous.section):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class input(ludicrous.input):
    children: tuple[NoChildren, ...]
    attrs: InputAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[InputAttrs]) -> None:
        pass


class output(ludicrous.output):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[OutputAttrs]) -> None:
        pass


class legend(ludicrous.legend):
    children: tuple[PrimitiveChildren, ...]
    attrs: GlobalAttrs

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[GlobalAttrs]
    ) -> None:
        pass


class option(ludicrous.option):
    children: tuple[PrimitiveChildren, ...]
    attrs: OptionAttrs

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[OptionAttrs]
    ) -> None:
        pass


class optgroup(ludicrous.optgroup):
    children: tuple[AnyChildren, ...]
    attrs: OptgroupAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[OptgroupAttrs]) -> None:
        pass


class select(ludicrous.select):
    children: tuple[AnyChildren, ...]
    attrs: SelectAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[SelectAttrs]) -> None:
        pass


class textarea(ludicrous.textarea):
    children: tuple[PrimitiveChildren, ...]
    attrs: TextAreaAttrs

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[TextAreaAttrs]
    ) -> None:
        pass


class fieldset(ludicrous.fieldset):
    children: tuple[AnyChildren, ...]
    attrs: FieldsetAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[FieldsetAttrs]) -> None:
        pass


class form(ludicrous.form):
    children: tuple[AnyChildren, ...]
    attrs: FormAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[FormAttrs]) -> None:
        pass


class img(ludicrous.img):
    children: tuple[NoChildren, ...]
    attrs: ImgAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[ImgAttrs]) -> None:
        pass


class svg(ludicrous.svg):
    children: tuple[AnyChildren, ...]
    attrs: SvgAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[SvgAttrs]) -> None:
        pass


class circle(ludicrous.circle):
    children: tuple[AnyChildren, ...]
    attrs: CircleAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[CircleAttrs]) -> None:
        pass


class line(ludicrous.line):
    children: tuple[AnyChildren, ...]
    attrs: LineAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[LineAttrs]) -> None:
        pass


class path(ludicrous.path):
    children: tuple[AnyChildren, ...]
    attrs: PathAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[PathAttrs]) -> None:
        pass


class polyline(ludicrous.polyline):
    children: tuple[AnyChildren, ...]
    attrs: PolylineAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[PolylineAttrs]) -> None:
        pass


class b(ludicrous.b):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class i(ludicrous.i):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class s(ludicrous.s):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class u(ludicrous.u):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class strong(ludicrous.strong):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class em(ludicrous.em):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class mark(ludicrous.mark):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class del_(ludicrous.del_):
    children: tuple[AnyChildren, ...]
    attrs: DelAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DelAttrs]) -> None:
        pass


class ins(ludicrous.ins):
    children: tuple[AnyChildren, ...]
    attrs: InsAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[InsAttrs]) -> None:
        pass


class header(ludicrous.header):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class big(ludicrous.big):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class small(ludicrous.small):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class code(ludicrous.code):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class pre(ludicrous.pre):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class cite(ludicrous.cite):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class blockquote(ludicrous.blockquote):
    children: tuple[AnyChildren, ...]
    attrs: BlockquoteAttrs

    def __init__(
        self, *children: AnyChildren, **attrs: Unpack[BlockquoteAttrs]
    ) -> None:
        pass


class abbr(ludicrous.abbr):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class h1(ludicrous.h1):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class h2(ludicrous.h2):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class h3(ludicrous.h3):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class h4(ludicrous.h4):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class h5(ludicrous.h5):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class h6(ludicrous.h6):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class title(ludicrous.title):
    children: tuple[PrimitiveChildren, ...]
    attrs: NoAttrs

    def __init__(self, *children: PrimitiveChildren, **attrs: Unpack[NoAttrs]) -> None:
        pass


class link(ludicrous.link):
    children: tuple[NoChildren, ...]
    attrs: HeadLinkAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[HeadLinkAttrs]) -> None:
        pass


class script(ludicrous.script):
    children: tuple[PrimitiveChildren, ...]
    attrs: ScriptAttrs

    def __init__(
        self, *children: PrimitiveChildren, **attrs: Unpack[ScriptAttrs]
    ) -> None:
        pass


class noscript(ludicrous.noscript):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class meta(ludicrous.meta):
    children: tuple[NoChildren, ...]
    attrs: MetaAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[MetaAttrs]) -> None:
        pass


class head(ludicrous.head):
    children: tuple[AnyChildren, ...]
    attrs: NoAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[NoAttrs]) -> None:
        pass


class body(ludicrous.body):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class footer(ludicrous.footer):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class html(ludicrous.html):
    children: tuple[head, body]
    attrs: HtmlTagAttrs

    def __init__(
        self, *children: *tuple[head, body], **attrs: Unpack[HtmlTagAttrs]
    ) -> None:
        pass


class iframe(ludicrous.iframe):
    children: tuple[NoChildren, ...]
    attrs: IframeAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[IframeAttrs]) -> None:
        pass


class article(ludicrous.article):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class address(ludicrous.address):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class caption(ludicrous.caption):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class col(ludicrous.col):
    children: tuple[NoChildren, ...]
    attrs: ColAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[ColAttrs]) -> None:
        pass


class colgroup(ludicrous.colgroup):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class area(ludicrous.area):
    children: tuple[NoChildren, ...]
    attrs: AreaAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[AreaAttrs]) -> None:
        pass


class aside(ludicrous.aside):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class source(ludicrous.source):
    children: tuple[NoChildren, ...]
    attrs: SourceAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[SourceAttrs]) -> None:
        pass


class audio(ludicrous.audio):
    children: tuple[AnyChildren, ...]
    attrs: AudioAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[AudioAttrs]) -> None:
        pass


class base(ludicrous.base):
    children: tuple[NoChildren, ...]
    attrs: BaseAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[BaseAttrs]) -> None:
        pass


class bdi(ludicrous.bdi):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class bdo(ludicrous.bdo):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class canvas(ludicrous.canvas):
    children: tuple[AnyChildren, ...]
    attrs: CanvasAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[CanvasAttrs]) -> None:
        pass


class data(ludicrous.data):
    children: tuple[AnyChildren, ...]
    attrs: DataAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DataAttrs]) -> None:
        pass


class datalist(ludicrous.datalist):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class details(ludicrous.details):
    children: tuple[AnyChildren, ...]
    attrs: DetailsAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DetailsAttrs]) -> None:
        pass


class dfn(ludicrous.dfn):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class dialog(ludicrous.dialog):
    children: tuple[AnyChildren, ...]
    attrs: DialogAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[DialogAttrs]) -> None:
        pass


class embed(ludicrous.embed):
    children: tuple[AnyChildren, ...]
    attrs: EmbedAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[EmbedAttrs]) -> None:
        pass


class figcaption(ludicrous.figcaption):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class figure(ludicrous.figure):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class hrgroup(ludicrous.hrgroup):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class hr(ludicrous.hr):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class kbd(ludicrous.kbd):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class map(ludicrous.map):
    children: tuple[AnyChildren, ...]
    attrs: MapAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[MapAttrs]) -> None:
        pass


class menu(ludicrous.menu):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class meter(ludicrous.meter):
    children: tuple[AnyChildren, ...]
    attrs: MeterAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[MeterAttrs]) -> None:
        pass


class nav(ludicrous.nav):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class object(ludicrous.object):
    children: tuple[AnyChildren, ...]
    attrs: ObjectAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ObjectAttrs]) -> None:
        pass


class param(ludicrous.param):
    children: tuple[NoChildren, ...]
    attrs: ParamAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[ParamAttrs]) -> None:
        pass


class picture(ludicrous.picture):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class progress(ludicrous.progress):
    children: tuple[AnyChildren, ...]
    attrs: ProgressAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[ProgressAttrs]) -> None:
        pass


class q(ludicrous.q):
    children: tuple[AnyChildren, ...]
    attrs: QAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[QAttrs]) -> None:
        pass


class rp(ludicrous.rp):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class rt(ludicrous.rt):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class ruby(ludicrous.ruby):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class samp(ludicrous.samp):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class search(ludicrous.search):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class sub(ludicrous.sub):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class summary(ludicrous.summary):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class sup(ludicrous.sup):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class template(ludicrous.template):
    children: tuple[AnyChildren, ...]
    attrs: HtmlAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[HtmlAttrs]) -> None:
        pass


class time(ludicrous.time):
    children: tuple[AnyChildren, ...]
    attrs: TimeAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[TimeAttrs]) -> None:
        pass


class track(ludicrous.track):
    children: tuple[NoChildren, ...]
    attrs: TrackAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[TrackAttrs]) -> None:
        pass


class var(ludicrous.var):
    children: tuple[AnyChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass


class video(ludicrous.video):
    children: tuple[AnyChildren, ...]
    attrs: VideoAttrs

    def __init__(self, *children: AnyChildren, **attrs: Unpack[VideoAttrs]) -> None:
        pass


class wbr(ludicrous.wbr):
    children: tuple[NoChildren, ...]
    attrs: GlobalAttrs

    def __init__(self, *children: NoChildren, **attrs: Unpack[GlobalAttrs]) -> None:
        pass
