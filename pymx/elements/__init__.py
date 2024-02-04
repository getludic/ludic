from .base import Complex, Element, HTMXAttributes


class div(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "div"


class span(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "span"


class p(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "p"


class a(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "a"


class br(Element, HTMXAttributes):
    html_name = "br"


class form(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "form"


class button(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "button"


class label(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "label"


class td(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "td"


class th(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "th"


class tr(Element[*tuple[th | td, ...]], HTMXAttributes):
    html_name = "tr"


class thead(Element[*tuple[tr, ...]], HTMXAttributes):
    html_name = "thead"


class tbody(Element[*tuple[tr, ...]], HTMXAttributes):
    html_name = "tbody"


class table(Element[thead, tbody], HTMXAttributes):
    html_name = "table"


class li(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "li"


class ul(Element[*tuple[li, ...]], HTMXAttributes):
    html_name = "ul"


class ol(Element[*tuple[li, ...]], HTMXAttributes):
    html_name = "ol"


class section(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "section"


class input(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "input"


class img(Element, HTMXAttributes):
    html_name = "img"


class h1(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "h1"


class h2(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "h2"


class h3(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "h3"


class h4(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "h4"


class h5(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "h5"


class h6(Element[*tuple[Complex, ...]], HTMXAttributes):
    html_name = "h6"
