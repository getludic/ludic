from ..elements import a, li, ul
from ..elements.base import Attributes, Element, HTMLAttributes, Text
from .base import Component


class LinkAttributes(Attributes):
    to: str


class NavigationAttributes(HTMLAttributes):
    items: dict[str, str]


class Link(Component[*tuple[Text, ...]], LinkAttributes):
    def render(self) -> Element:
        return a(href=self.to)(self[0])


class Navigation(Component, NavigationAttributes):
    def render(self) -> Element:
        attrs = self.attrs
        attrs.pop("items")

        return ul(**attrs)(
            *(li(Link(to=link)(name)) for name, link in self.items.items())
        )
