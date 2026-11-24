from typing import NotRequired, override

from ludic.attrs import GlobalAttrs
from ludic.base import BaseElement
from ludic.components import Component, ComponentStrict
from ludic.html import a, h2, h3, h4, li, nav, p, style, ul
from ludic.types import AnyChildren, PrimitiveChildren

from .buttons import ButtonLink
from .headers import H2, H3, H4
from .utils import text_to_kebab


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
    styles = style.use(
        lambda theme: {
            "nav.navigation ul": {
                "list-style": "none",
                "padding": "0",
            },
            "nav.navigation .btn": {
                "display": "block",
                "padding": f"{theme.sizes.xxxxs} {theme.sizes.xs}",
                "background": "none",
                "color": theme.colors.dark,
            },
            ("nav.navigation .btn:hover", "nav.navigation .btn:focus-visible"): {
                "background-color": theme.colors.light,
                "filter": "none",
            },
            "nav.navigation .active .btn": {
                "background-color": theme.colors.light,
                "color": theme.colors.primary.darken(1),
                "font-weight": "600",
            },
        }
    )

    @override
    def render(self) -> nav:
        return nav(
            ul(*self.children, classes=["stack", "small"]),
            **self.attrs_for(nav),
        )


class TableOfContentsAttrs(GlobalAttrs, total=False):
    label: str
    max_level: int


class TableOfContents(Component[AnyChildren, TableOfContentsAttrs]):
    """Links to the headings found among the given elements.

    Pass the elements of a page, the table of contents picks the level 2
    headings (``H2`` or ``h2``), and with ``max_level=3`` or ``4`` also the
    deeper ones. A heading links to its ``id``, or to the id a header with an
    anchor gets, which is its text in kebab case. The ``label`` is shown above
    the links.

    Example usage:

        content = [H1("Guide"), H2("Install"), Paragraph("..."), H2("Usage")]
        TableOfContents(*content, label="On this page")
    """

    classes = ["table-of-contents"]
    styles = style.use(
        lambda theme: {
            ".table-of-contents .toc-title": {
                "margin-block-end": theme.sizes.xxs,
                "color": theme.colors.dark,
                "font-size": theme.fonts.size * 0.8,
                "font-weight": "600",
                "text-transform": "uppercase",
                "letter-spacing": "0.05em",
            },
            ".table-of-contents ul": {
                "list-style": "none",
                "padding": "0",
            },
            ".table-of-contents li + li": {
                "margin-block-start": theme.sizes.xxxs,
            },
            ".table-of-contents a": {
                "color": theme.colors.dark.lighten(1),
                "font-size": theme.fonts.size * 0.9,
            },
            ".table-of-contents a:hover": {
                "color": theme.colors.primary.darken(1),
            },
            ".table-of-contents .level-3": {
                "padding-inline-start": theme.sizes.s,
            },
            ".table-of-contents .level-4": {
                "padding-inline-start": theme.sizes.xl,
            },
        }
    )

    @override
    def render(self) -> nav:
        max_level = self.attrs.get("max_level", 2)
        items = []
        for child in self.children:
            level = self._heading_level(child)
            if isinstance(child, BaseElement) and level and level <= max_level:
                target = child.attrs.get("id") or text_to_kebab(child.text)
                items.append(
                    li(a(child.text, href=f"#{target}"), classes=[f"level-{level}"])
                )

        label = self.attrs.get("label")
        self.attrs.setdefault("aria_label", label or "Table of contents")
        return nav(
            *([p(label, classes=["toc-title"])] if label else []),
            ul(*items),
            **self.attrs_for(nav),
        )

    @staticmethod
    def _heading_level(child: AnyChildren) -> int:
        if isinstance(child, H2 | h2):
            return 2
        if isinstance(child, H3 | h3):
            return 3
        if isinstance(child, H4 | h4):
            return 4
        return 0
