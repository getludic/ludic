from typing import override

from ..elements import a, li, p, ul
from ..elements.attrs import HtmlAttributes, HyperlinkAttributes
from ..elements.base import Attributes, TextChildren
from .base import Component


class LinkAttributes(Attributes):
    to: str


class Link(Component[*TextChildren, LinkAttributes]):
    @override
    def render(self) -> a:
        return a(href=self.attrs["to"])(self.children[0])


class Paragraph(Component[*TextChildren, HyperlinkAttributes]):
    @override
    def render(self) -> p:
        return p(**self.attrs)(*self.children)


class NavigationAttributes(HtmlAttributes):
    items: dict[str, str]


class Navigation(Component[NavigationAttributes]):
    @override
    def render(self) -> ul:
        return ul(**self.attrs_for(cls=ul))(
            *(li(Link(to=link)(name)) for name, link in self.attrs["items"].items())
        )
