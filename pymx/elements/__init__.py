from typing import Never

from .base import Element, Elements, HTMXAttributes


class div(Element[Elements, HTMXAttributes]):
    ...


class span(Element[Elements, HTMXAttributes]):
    ...


class p(Element[Elements, HTMXAttributes]):
    ...


class a(Element[Elements, HTMXAttributes]):
    ...


class br(Element[Never, HTMXAttributes]):
    ...


class form(Element[Elements, HTMXAttributes]):
    ...


class button(Element[Elements, HTMXAttributes]):
    ...


class label(Element[Elements, HTMXAttributes]):
    ...


class td(Element[Elements, HTMXAttributes]):
    ...


class th(Element[Elements, HTMXAttributes]):
    ...


class tr(Element[th | td, HTMXAttributes]):
    ...


class thead(Element[tr, HTMXAttributes]):
    ...


class tbody(Element[tr, HTMXAttributes]):
    ...


class table(Element[thead | tbody, HTMXAttributes]):
    ...


class li(Element[Elements, HTMXAttributes]):
    ...


class ul(Element[li, HTMXAttributes]):
    ...


class ol(Element[li, HTMXAttributes]):
    ...


class section(Element[Elements, HTMXAttributes]):
    ...


class input(Element[Elements, HTMXAttributes]):
    ...


class img(Element[Never, HTMXAttributes]):
    ...


class h1(Element[Elements, HTMXAttributes]):
    ...


class h2(Element[Elements, HTMXAttributes]):
    ...


class h3(Element[Elements, HTMXAttributes]):
    ...


class h4(Element[Elements, HTMXAttributes]):
    ...


class h5(Element[Elements, HTMXAttributes]):
    ...


class h6(Element[Elements, HTMXAttributes]):
    ...
