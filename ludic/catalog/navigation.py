from typing import override

from ludic.attrs import HtmxAttrs
from ludic.base import Component, PrimitiveChild
from ludic.html import li, ul

from .typography import Link


class NavItemAttrs(HtmxAttrs):
    to: str


class NavItem(Component[PrimitiveChild, NavItemAttrs]):
    """Simple component simulating a navigation item.

    This component is supposed to be used as a child of the :class:`Navigation`
    component.
    """

    @override
    def render(self) -> li:
        label = str(self.children[0])
        return li(Link(label, to=self.attrs["to"]), id=label.lower())


class Navigation(Component[*tuple[NavItem, ...], HtmxAttrs]):
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
