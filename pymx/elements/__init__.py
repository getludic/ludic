from .base import AnyChildren, Element, NoChildren, SimpleChildren
from .html import (
    Attributes,
    HTMLAttributes,
    HTMXAttributes,
    LinkAttributes,
    MetaAttributes,
)


class div(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "div"


class span(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "span"


class p(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "p"


class a(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "a"


class br(Element[*NoChildren, HTMLAttributes]):
    html_name: str = "br"


class form(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "form"


class button(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "button"


class label(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "label"


class td(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "td"


class th(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "th"


class tr(Element[*tuple[th | td, ...], HTMXAttributes]):
    html_name: str = "tr"


class thead(Element[*tuple[tr, ...], HTMXAttributes]):
    html_name: str = "thead"


class tbody(Element[*tuple[tr, ...], HTMXAttributes]):
    html_name: str = "tbody"


class table(Element[thead, tbody, HTMXAttributes]):
    html_name: str = "table"


class li(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "li"


class ul(Element[*tuple[li, ...], HTMXAttributes]):
    html_name: str = "ul"


class ol(Element[*tuple[li, ...], HTMXAttributes]):
    html_name: str = "ol"


class dt(Element[*SimpleChildren, HTMXAttributes]):
    html_name: str = "dt"


class dd(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "dd"


class dl(Element[*tuple[dt | dd, ...], HTMXAttributes]):
    html_name: str = "dl"


class section(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "section"


class input(Element[*NoChildren, HTMXAttributes]):
    html_name: str = "input"


class option(Element[*SimpleChildren, HTMXAttributes]):
    html_name: str = "option"


class select(Element[*tuple[option, ...], HTMXAttributes]):
    html_name: str = "select"


class img(Element[*NoChildren, HTMXAttributes]):
    html_name: str = "img"


class svg(Element[*NoChildren, HTMXAttributes]):
    html_name: str = "svg"


class b(Element[*SimpleChildren, HTMXAttributes]):
    html_name: str = "b"


class i(Element[*SimpleChildren, HTMXAttributes]):
    html_name: str = "i"


class s(Element[*SimpleChildren, HTMXAttributes]):
    html_name: str = "s"


class u(Element[*SimpleChildren, HTMXAttributes]):
    html_name: str = "u"


class header(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "header"


class small(Element[*SimpleChildren, HTMXAttributes]):
    html_name: str = "small"


class h1(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "h1"


class h2(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "h2"


class h3(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "h3"


class h4(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "h4"


class h5(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "h5"


class h6(Element[*AnyChildren, HTMXAttributes]):
    html_name: str = "h6"


class title(Element[*SimpleChildren, HTMLAttributes]):
    html_name: str = "title"


class link(Element[*SimpleChildren, LinkAttributes]):
    html_name: str = "link"


class style(Element[*SimpleChildren, HTMLAttributes]):
    html_name: str = "style"


class script(Element[*SimpleChildren, HTMLAttributes]):
    html_name: str = "script"


class meta(Element[*SimpleChildren, MetaAttributes]):
    html_name: str = "meta"


class head(Element[*tuple[title | link | style | meta, ...], Attributes]):
    html_name: str = "head"


class body(Element[*AnyChildren, Attributes]):
    html_name: str = "body"


class html(Element[head, body, Attributes]):
    html_name: str = "html"


class iframe(Element[*NoChildren, HTMXAttributes]):
    html_name: str = "iframe"
