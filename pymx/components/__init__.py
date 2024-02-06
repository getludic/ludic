from typing import override

from ..elements import a, li, p, ul
from ..elements.attrs import HtmxAttributes, HyperlinkAttributes
from ..elements.base import Attributes, TextChild, TextChildren
from .base import Component


class LinkAttributes(Attributes):
    to: str


class Link(Component[TextChild, LinkAttributes]):
    @override
    def render(self) -> a:
        return a(self.children[0], href=self.attrs["to"])


class Paragraph(Component[*TextChildren, HyperlinkAttributes]):
    @override
    def render(self) -> p:
        return p(*self.children, **self.attrs)


class NavItemAttributes(HtmxAttributes):
    to: str


class NavItem(Component[TextChild, NavItemAttributes]):
    @override
    def render(self) -> li:
        label = str(self.children[0])
        return li(Link(label, to=self.attrs["to"]), id=label.lower())


class Navigation(Component[*tuple[NavItem, ...], HtmxAttributes]):
    @override
    def render(self) -> ul:
        return ul(*self.children, class_="navigation", **self.attrs_for(cls=ul))
