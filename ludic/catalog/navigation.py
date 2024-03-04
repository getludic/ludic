from typing import override

from ludic.attrs import GlobalAttrs
from ludic.base import Component, PrimitiveChildren
from ludic.html import li, ul

from .typography import Link


class NavItemAttrs(GlobalAttrs):
    to: str


class NavItem(Component[PrimitiveChildren, NavItemAttrs]):
    """Simple component simulating a navigation item.

    This component is supposed to be used as a child of the :class:`Navigation`
    component.
    """

    @override
    def render(self) -> li:
        label = str(self.children[0])
        return li(Link(label, to=self.attrs["to"]), id=label.lower())


class Navigation(Component[NavItem, GlobalAttrs]):
    """Simple component simulating a navigation bar.

    Example usage:

        Navigation(
            NavItem("Home", to="/"),
            NavItem("About", to="/about"),
        )
    """

    @override
    def render(self) -> ul:
        return ul(*self.children, class_="navigation", **self.attrs_for(ul))
