from ..elements import a
from ..elements.base import Attributes, Element, Primitives
from .base import Component


class LinkAttributes(Attributes):
    to: str


class Link(Component[Primitives, LinkAttributes]):
    def render(self) -> Element:
        return a(href=self.to)(self[0])
