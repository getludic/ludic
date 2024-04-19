from typing import override

from ludic.attrs import GlobalAttrs
from ludic.html import div, style
from ludic.types import ComponentStrict


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
                "inline-size": "100%",
            },
            ".stack > *": {
                "margin-block": "0",
            },
            ".stack > * + *": {
                "margin-block-start": theme.sizes.l,
            },
            ".stack.stack-recursive *": {
                "margin-block": "0",
            },
            ".stack.stack-recursive * + *": {
                "margin-block-start": theme.sizes.l,
            },
            ".stack.stack-small > * + *": {
                "margin-block-start": theme.sizes.s,
            },
            ".stack.stack-large > * + *": {
                "margin-block-start": theme.sizes.xxl,
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
                "padding": theme.sizes.l,
                "border": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(0.05)}"
                ),
                "border-radius": theme.rounding.more,
                "color": theme.colors.dark,
                "background-color": theme.colors.light,
            },
            ".box *": {
                "color": "inherit",
            },
            ".box.invert": {
                "color": theme.colors.light,
                "background-color": theme.colors.dark,
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
                "padding-inline-start": theme.sizes.l,
                "padding-inline-end": theme.sizes.l,
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
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
                "gap": theme.sizes.m,
                "justify-content": "flex-start",
                "align-items": "center",
            },
            ".cluster.cluster-small": {
                "gap": theme.sizes.xxs,
            },
            ".cluster.cluster-large": {
                "gap": theme.sizes.xl,
            },
        }
    )


class Sidebar(div):
    """The sidebar part of a WithSidebar component."""

    classes = ["sidebar"]
    styles = {
        ".with-sidebar > .sidebar": {
            "flex-grow": 1,
        },
    }


class NotSidebar(div):
    """The content part of a WithSidebar component."""

    classes = ["not-sidebar"]
    styles = {
        ".with-sidebar > .not-sidebar": {
            "flex-basis": 0,
            "flex-grow": 999,
            "min-inline-size": "50%",
        },
    }


class WithSidebar(
    ComponentStrict[NotSidebar | Sidebar, Sidebar | NotSidebar, GlobalAttrs]
):
    """A component with a content and a sidebar.

    Example usage:

        WithSidebar(
            Sidebar(...),
            NotSidebar(...),
        )

    Or you can put the sidebar on the right side:

        WithSidebar(
            NotSidebar(...),
            Sidebar(...),
        )
    """

    classes = ["with-sidebar"]
    styles = style.use(
        lambda theme: {
            ".with-sidebar": {
                "display": "flex",
                "flex-wrap": "wrap",
                "gap": theme.sizes.xl,
            },
        }
    )

    @override
    def render(self) -> div:
        return div(self.children[0], self.children[1])
