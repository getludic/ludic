from typing import override

from ludic.attrs import GlobalAttrs
from ludic.components import Block, ComponentStrict, Inline
from ludic.html import div, style
from ludic.types import AnyChildren


class Stack(Block):
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
                "margin-block-start": theme.sizes.xxxs,
            },
            ".stack.small > * + *": {
                "margin-block-start": theme.sizes.s,
            },
            ".stack.large > * + *": {
                "margin-block-start": theme.sizes.xxxl,
            },
        }
    )


class Box(Block):
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
                "padding": theme.sizes.m,
                "color": theme.colors.dark,
            },
            ".box.small": {
                "padding": theme.sizes.xs,
            },
            ".box.large": {
                "padding": theme.sizes.xl,
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


class Center(Block):
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
                "padding-inline-start": theme.sizes.xxl,
                "padding-inline-end": theme.sizes.xxl,
            }
        }
    )


class Cluster(Inline):
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


class Sidebar(Block):
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
                "gap": theme.sizes.xxl,
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
        return div(self.children[0], self.children[1], **self.attrs)


class Switcher(Block):
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
                "gap": theme.sizes.xl,
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


class Cover(Block):
    """A component which covers the whole viewport.

    Example usage:

        Cover(
            div(...),
        )
    """

    classes = ["cover"]
    styles = style.use(
        lambda theme: {
            ".cover": {
                "display": "flex",
                "flex-direction": "column",
                "min-block-size": theme.layouts.cover.min_height,
                "padding": theme.sizes.xl,
            },
            ".cover > *": {
                "margin-block": theme.sizes.xl,
            },
            f".cover > :first-child:not({theme.layouts.cover.element})": {
                "margin-block-start": "0",
            },
            f".cover > :last-child:not({theme.layouts.cover.element})": {
                "margin-block-end": "0",
            },
            f".cover > {theme.layouts.cover.element}": {
                "margin-block": "auto",
            },
        }
    )


class Grid(Block):
    """A component which creates a grid layout.

    Example usage:

        Grid(
            div(...),
            div(...),
        )
    """

    classes = ["grid"]
    styles = style.use(
        lambda theme: {
            ".grid": {
                "display": "grid",
                "grid-gap": theme.sizes.xl,
            },
            f"@supports (width: min({theme.layouts.grid.cell_size}, 100%))": {
                ".grid": {
                    "grid-template-columns": (
                        "repeat("
                        "auto-fit,"
                        f"minmax(min({theme.layouts.grid.cell_size},"
                        "100%"
                        "), 1fr))"
                    ),
                },
            },
        }
    )


class Frame(Block):
    """A component which creates a frame layout.

    Example usage:

        Frame(
            div(...),
        )
    """

    classes = ["frame"]
    styles = style.use(
        lambda theme: {
            ".frame": {
                "aspect-ratio": (
                    f"{theme.layouts.frame.numerator}/{theme.layouts.frame.denominator}"
                ),
                "overflow": "hidden",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
            },
            (".frame > img", ".frame > video"): {
                "inline-size": "100%",
                "block-size": "100%",
                "object-fit": "cover",
            },
        }
    )
