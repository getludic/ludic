from typing import NotRequired, override

from ..elements import a, body, head, html, li, link, meta, p, title, ul
from ..elements.base import (
    AnyChildren,
    AnyElement,
    Attributes,
    NoChildren,
    SimpleChildren,
)
from ..elements.html import HtmlAttributes
from .base import Component


class LinkAttributes(Attributes):
    to: str


class Link(Component[*SimpleChildren, LinkAttributes]):
    @override
    def render(self) -> AnyElement:
        return a(href=self.attrs["to"])(self[0])


class Paragraph(Component[*SimpleChildren, LinkAttributes]):
    @override
    def render(self) -> AnyElement:
        return p(**self.attrs)(*self.children)


class NavigationAttributes(HtmlAttributes):
    items: dict[str, str]


class Navigation(Component[*NoChildren, NavigationAttributes]):
    @override
    def render(self) -> AnyElement:
        return ul(**self.attrs_for(ul))(
            *(li(Link(to=link)(name)) for name, link in self.attrs["items"].items())
        )


class PageAttributes(HtmlAttributes):
    metadata: NotRequired[list[meta]]
    links: NotRequired[list[link]]


class Page(Component[*AnyChildren, PageAttributes]):
    @override
    def render(self) -> AnyElement:
        return html(
            head(
                title(self.attrs["title"]),
                *self.attrs.get("metadata", []),
                *self.attrs.get("links", []),
            ),
            body(*self.children),
        )
