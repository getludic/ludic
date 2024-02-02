from .base import Element


class Div(Element):
    html_name = "div"


class Span(Element):
    html_name = "span"


class Paragraph(Element):
    html_name = "p"


class Link(Element):
    html_name = "a"


class Form(Element):
    html_name = "form"


class Button(Element):
    html_name = "button"


class Label(Element):
    html_name = "label"


class TableCell(Element):
    html_name = "td"


class TableHeadCell(Element):
    html_name = "th"


class TableRow(Element[TableHeadCell | TableCell]):
    html_name = "tr"


class TableHead(Element[TableRow]):
    html_name = "thead"


class TableBody(Element[TableRow]):
    html_name = "tbody"


class Table(Element[TableHead | TableBody]):
    html_name = "table"


class ListItem(Element):
    html_name = "li"


class List(Element[ListItem]):
    html_name = "ul"


class OrderedList(Element[ListItem]):
    html_name = "ol"


class Section(Element):
    html_name = "section"


class Input(Element):
    html_name = "input"


class Image(Element[str]):
    html_name = "img"


class H1(Element):
    html_name = "h1"


class H2(Element):
    html_name = "h2"


class H3(Element):
    html_name = "h3"


class H4(Element):
    html_name = "h4"


class H5(Element):
    html_name = "h5"


class H6(Element):
    html_name = "h6"
