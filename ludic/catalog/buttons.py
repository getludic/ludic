from typing import override

from ludic.attrs import ButtonAttrs
from ludic.html import a, button, style
from ludic.types import ComponentStrict, PrimitiveChildren


class Button(ComponentStrict[PrimitiveChildren, ButtonAttrs]):
    """Simple component creating an HTML button.

    The component creates a button.
    """

    classes = ["btn"]
    styles = style.use(
        lambda theme: {
            ".btn": {
                "background-color": theme.colors.light,
                "color": theme.colors.black,
                "padding": f"{theme.sizes.xxs} {theme.sizes.s}",
                "border": "none",
                "border-radius": theme.rounding.normal,
                "cursor": "pointer",
                "font-size": theme.fonts.size,
                "transition": "0.1s filter linear, 0.1s -webkit-filter linear",
            },
            ".btn:hover": {
                "filter": "brightness(85%)",
            },
            ".btn.small": {
                "font-size": theme.fonts.size * 0.9,
                "padding": f"{theme.sizes.xxxs} {theme.sizes.xs}",
            },
            ".btn.large": {
                "font-size": theme.fonts.size * 1.2,
                "padding": f"{theme.sizes.xs} {theme.sizes.m}",
            },
            ".box .btn": {
                "background-color": theme.colors.dark,
                "color": theme.colors.light,
                "border-color": theme.colors.dark,
            },
        }
    )

    @override
    def render(self) -> button | a:
        return button(self.children[0], **self.attrs)


class ButtonPrimary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``primary`` class.
    """

    classes = ["btn", "primary"]
    styles = style.use(
        lambda theme: {
            ".btn.primary": {
                "color": theme.colors.primary.readable(),
                "background-color": theme.colors.primary,
            }
        }
    )


class ButtonSecondary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``secondary`` class.
    """

    classes = ["btn", "secondary"]
    styles = style.use(
        lambda theme: {
            ".btn.secondary": {
                "color": theme.colors.secondary.readable(),
                "background-color": theme.colors.secondary,
            }
        }
    )


class ButtonLink(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``secondary`` class.
    """

    classes = ["btn", "link"]
    styles = style.use(
        lambda theme: {
            (".btn.link", ".box .btn.link"): {
                "color": theme.colors.dark,
                "background": "none",
                "border": "none",
                "text-decoration": "none",
                "display": "inline-block",
            },
            (".btn.link.active", ".btn.link.active:hover"): {
                "background-color": theme.colors.light,
            },
            (".box .btn.link.active", ".box .btn.link.active:hover"): {
                "color": theme.colors.light,
                "background-color": theme.colors.dark,
            },
            (".btn.link:hover", ".box .btn.link:hover"): {
                "color": theme.colors.dark,
                "background-color": theme.colors.light,
                "text-decoration": "none",
            },
        }
    )

    @override
    def render(self) -> a:
        return a(self.children[0], **self.attrs)


class ButtonSuccess(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``success`` class.
    """

    classes = ["btn", "success"]
    styles = style.use(
        lambda theme: {
            ".btn.success": {
                "color": theme.colors.success.readable(),
                "background-color": theme.colors.success,
            }
        }
    )


class ButtonDanger(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``danger`` class.
    """

    classes = ["btn", "danger"]
    styles = style.use(
        lambda theme: {
            ".btn.danger": {
                "color": theme.colors.danger.readable(),
                "background-color": theme.colors.danger,
            }
        }
    )


class ButtonWarning(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``warning`` class.
    """

    classes = ["btn", "warning"]
    styles = style.use(
        lambda theme: {
            ".btn.warning": {
                "color": theme.colors.warning.readable(),
                "background-color": theme.colors.warning,
            }
        }
    )


class ButtonInfo(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``info`` class.
    """

    classes = ["btn", "info"]
    styles = style.use(
        lambda theme: {
            ".btn.info": {
                "color": theme.colors.info.readable(),
                "background-color": theme.colors.info,
            }
        }
    )
