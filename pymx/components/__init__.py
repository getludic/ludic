"""A collection of PyMX components.

This module is meant as a collection of components that could be useful
for building PyMX applications. Any contributor is welcome to add new ones.

It also serves as showcase of possible implementations.
"""

from typing import override

from ..elements import a, li, p, ul
from ..elements.attrs import GlobalAttributes, HtmxAttributes
from ..elements.base import AnyChildren, Attributes, PrimitiveChild
from .base import Component


class LinkAttributes(Attributes):
    to: str


class Link(Component[PrimitiveChild, LinkAttributes]):
    """Simple component simulating a link.

    The difference between :class:`Link` and :class:`a` is that this component
    expects only one primitive child, so it cannot contain any nested elements.

    Example usage:

        Link("Hello, World!", to="https://example.com")
    """

    @override
    def render(self) -> a:
        return a(self.children[0], href=self.attrs["to"])


class Paragraph(Component[*AnyChildren, GlobalAttributes]):
    """Simple component simulating a paragraph.

    There is basically just an alias for the :class:`p` element.

    Example usage:

        Paragraph(f"Hello, {b("World")}!")
    """

    @override
    def render(self) -> p:
        return p(*self.children, **self.attrs)


class NavItemAttributes(HtmxAttributes):
    to: str


class NavItem(Component[PrimitiveChild, NavItemAttributes]):
    """Simple component simulating a navigation item.

    This component is supposed to be used as a child of the :class:`Navigation`
    component.
    """

    @override
    def render(self) -> li:
        label = str(self.children[0])
        return li(Link(label, to=self.attrs["to"]), id=label.lower())


class Navigation(Component[*tuple[NavItem, ...], HtmxAttributes]):
    """Simple component simulating a navigation bar.

    Example usage:

        Navigation(
            NavItem("Home", to="/"),
            NavItem("About", to="/about"),
        )
    """

    @override
    def render(self) -> ul:
        return ul(*self.children, class_="navigation", **self.attrs_for(cls=ul))
