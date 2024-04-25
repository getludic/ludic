from typing import override

from ludic.attrs import GlobalAttrs
from ludic.html import div, style
from ludic.types import AnyChildren, ComponentStrict


class Stack(div):
    """Stack is a block component which renders its children with a space between them.

    Example usage:

        Stack(
            h2("Header 2"),
            p("Hello, World!"),
            p("Goodbye, World!"),
        )

    All children components will have a space (margin) separating them.
    """

    classes = ["stack"]
    styles = style.use(
        lambda theme: {
            ".stack": {
                "display": "flex",
                "flex-direction": "column",
                "justify-content": "flex-start",
            },
            ".stack > *": {
                "margin-block": "0",
                "inline-size": "100%",
            },
            ".stack > * + *": {
                "margin-block-start": theme.sizes.xl,
            },
            ".stack.recursive *": {
                "margin-block": "0",
            },
            ".stack.recursive * + *": {
                "margin-block-start": theme.sizes.xl,
            },
            ".stack.tiny > * + *": {
                "margin-block-start": theme.sizes.xxxxs,
            },
            ".stack.small > * + *": {
                "margin-block-start": theme.sizes.s,
            },
            ".stack.large > * + *": {
                "margin-block-start": theme.sizes.xxxxl,
            },
        }
    )


class Box(div):
    """A component which applies padding from all sides.

    Thus the inner content of the `Box` is spaced in all directions equally.

    Example usage:

        Box(
            h2("List of Things"),
            ul(
                li("Thing 1"),
                li("Thing 2"),
            )
        )
    """

    classes = ["box"]
    styles = style.use(
        lambda theme: {
            ".box": {
                "padding": theme.sizes.xl,
                "color": theme.colors.dark,
            },
            ".box:not(.transparent)": {
                "border": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
                "border-radius": theme.rounding.more,
                "background-color": theme.colors.light,
            },
            ".box:not(.transparent) *": {
                "color": "inherit",
            },
            ".box.invert": {
                "color": theme.colors.light,
                "background-color": theme.colors.dark,
                "border": f"{theme.borders.thin} solid {theme.colors.dark}",
                "border-radius": theme.rounding.more,
            },
        }
    )


class Center(div):
    """A component which horizontally centers its children.

    Example usage:

        Center(
            h2("Lorem Ipsum"),
            p("Dolor sit amet..."),
        )
    """

    classes = ["center"]
    styles = style.use(
        lambda theme: {
            ".center": {
                "box-sizing": "content-box",
                "margin-inline": "auto",
                "max-inline-size": theme.measure,
                "padding-inline-start": theme.sizes.xxxl,
                "padding-inline-end": theme.sizes.xxxl,
            }
        }
    )


class Cluster(div):
    """A component for inline children to be rendered in a row.

    All contained children have a space (margin) between them.

    Example usage:

        Cluster(
            button("button 1"),
            button("button 2"),
        )
    """

    classes = ["cluster"]
    styles = style.use(
        lambda theme: {
            ".cluster": {
                "display": "flex",
                "flex-wrap": "wrap",
                "gap": theme.sizes.l,
                "justify-content": "flex-start",
                "align-items": "center",
            },
            ".cluster.centered": {
                "justify-content": "center",
            },
            ".cluster.flex-end": {
                "justify-content": "flex-end",
            },
            ".cluster.small": {
                "gap": theme.sizes.xxs,
            },
            ".cluster.large": {
                "gap": theme.sizes.xxl,
            },
        }
    )


class Sidebar(div):
    """The sidebar part of a WithSidebar component."""

    classes = ["sidebar"]


class WithSidebar(ComponentStrict[AnyChildren, AnyChildren, GlobalAttrs]):
    """A component with a content and a sidebar.

    Example usage:

        WithSidebar(
            Sidebar(...),
            div(...),
        )

    Or you can put the sidebar on the right side:

        WithSidebar(
            div(...),
            Sidebar(...),
        )
    """

    classes = ["with-sidebar"]
    styles = style.use(
        lambda theme: {
            ".with-sidebar": {
                "display": "flex",
                "flex-wrap": "wrap",
                "gap": theme.sizes.xxxxl,
            },
            ".with-sidebar > .sidebar": (
                {
                    "flex-basis": theme.layouts.sidebar.side_width,
                    "flex-grow": 1,
                }
                if theme.layouts.sidebar.side_width
                else {
                    "flex-grow": 1,
                }
            ),
            ".with-sidebar > :not(.sidebar)": {
                "flex-basis": 0,
                "flex-grow": 999,
                "min-inline-size": theme.layouts.sidebar.content_min_width,
            },
        }
    )

    @override
    def render(self) -> div:
        return div(self.children[0], self.children[1])


class Switcher(div):
    """A component switching between horizontal and vertical layouts.

    All the children are either composed horizontally or vertically
    depending on the width of the viewport.

    Example usage:

        Switcher(
            div(...),
            div(...),
            div(...),
        )
    """

    classes = ["switcher"]
    styles = style.use(
        lambda theme: {
            ".switcher": {
                "display": "flex",
                "flex-wrap": "wrap",
                "gap": theme.sizes.xxl,
            },
            ".switcher > *": {
                "flex-grow": 1,
                "flex-basis": (
                    f"calc(({theme.layouts.switcher.threshold} - 100%) * 999)"
                ),
            },
            (
                f".switcher > :nth-last-child(n+{theme.layouts.switcher.limit+1})",
                f".switcher > :nth-last-child(n+{theme.layouts.switcher.limit+1}) ~ *",
            ): {
                "flex-basis": "100%",
            },
        }
    )
