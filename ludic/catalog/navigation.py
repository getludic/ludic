from typing import NotRequired, override

from ludic.attrs import GlobalAttrs
from ludic.components import Component, ComponentStrict
from ludic.html import h2, li, nav, style, ul
from ludic.types import PrimitiveChildren

from .buttons import ButtonLink


class NavItemAttrs(GlobalAttrs):
    to: str
    active: NotRequired[bool]
    active_subsection: NotRequired[bool]


class NavHeader(ComponentStrict[str, GlobalAttrs]):
    """Simple component simulating a navigation header.

    This component is supposed to be used as a child of the :class:`Navigation`
    component.
    """

    classes = ["nav-header"]
    styles = style.use(
        lambda theme: {
            "h2.nav-header": {
                "font-size": theme.headers.h2.size * 0.7,
            }
        }
    )

    @override
    def render(self) -> h2:
        return h2(self.children[0], **self.attrs_for(h2))


class NavItem(Component[PrimitiveChildren, NavItemAttrs]):
    """Simple component simulating a navigation item.

    This component is supposed to be used as a child of the :class:`Navigation`
    component.
    """

    classes = ["nav-item"]
    styles = style.use(
        lambda theme: {
            "li.nav-item.section.active-subsection .btn": {
                "font-weight": "bold",
                "background": "none",
            },
            "li.nav-item.subsection": {
                "padding-inline-start": theme.sizes.m,
            },
        }
    )

    @override
    def render(self) -> li:
        self.attrs.setdefault("classes", [])

        if self.attrs.pop("active_subsection", False):
            self.attrs["classes"].append("active-subsection")

        if self.attrs.pop("active", False):
            self.attrs["classes"].append("active")

        return li(
            ButtonLink(
                self.children[0],
                to=self.attrs["to"],
                external=False,
                classes=["small"] if "subsection" in self.attrs["classes"] else [],
            ),
            **self.attrs_for(li),
        )


class NavSection(ComponentStrict[NavHeader, *tuple[NavItem, ...], GlobalAttrs]):
    """Simple component simulating a navigation section.

    This component is supposed to be used as a child of the :class:`Navigation`
    component.
    """

    @override
    def render(self) -> li:
        self.attrs.setdefault("classes", ["stack", "tiny"])
        return li(
            self.children[0],
            ul(*self.children[1:], classes=["stack", "tiny"]),
            **self.attrs_for(li),
        )


class Navigation(Component[NavItem | NavSection, GlobalAttrs]):
    """Simple component simulating a navigation bar.

    Example usage:

        Navigation(
            NavItem("Home", to="/"),
            NavItem("About", to="/about"),
        )
    """

    classes = ["navigation"]
    styles = {
        "nav.navigation ul": {
            "list-style": "none",
            "padding": "0",
        },
    }

    @override
    def render(self) -> nav:
        return nav(
            ul(*self.children, classes=["stack", "small"]),
            **self.attrs_for(nav),
        )
