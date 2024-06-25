from typing import override

from ludic.attrs import ButtonAttrs
from ludic.components import ComponentStrict
from ludic.html import button, style
from ludic.types import PrimitiveChildren

from .typography import Link


class Button(ComponentStrict[PrimitiveChildren, ButtonAttrs]):
    """Simple component creating an HTML button.

    The component creates a button.
    """

    classes = ["btn"]
    styles = style.use(
        lambda theme: {
            ".btn": {
                "display": "inline-block",
                "text-decoration": "none",
                "background-color": theme.colors.light,
                "color": theme.colors.black,
                "padding": f"{theme.sizes.xxxxs * 0.8} {theme.sizes.xs}",
                "border": "none",
                "border-radius": theme.rounding.normal,
                "font-size": theme.fonts.size,
                "transition": "0.1s filter linear, 0.1s -webkit-filter linear",
            },
            ".btn:enabled": {
                "cursor": "pointer",
            },
            ":not(a).btn": {
                "background-color": theme.colors.light.darken(2),
            },
            (".btn:hover", ".btn:focus"): {
                "filter": "brightness(85%)",
                "text-decoration": "none",
            },
            ".btn:disabled": {
                "filter": "opacity(50%)",
            },
            ".btn.small": {
                "font-size": theme.fonts.size * 0.9,
                "padding": f"{theme.sizes.xxxxs * 0.6} {theme.sizes.xxs}",
            },
            ".btn.large": {
                "font-size": theme.fonts.size * 1.2,
                "padding": f"{theme.sizes.xxxxs} {theme.sizes.m}",
            },
            (".invert .btn", ".active .btn"): {
                "background-color": theme.colors.dark,
                "color": theme.colors.light,
                "border-color": theme.colors.dark,
            },
        }
    )

    @override
    def render(self) -> button:
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


class ButtonLink(Link):
    """Simple component creating an HTML button.

    The component creates a button with the ``secondary`` class.
    """

    classes = ["btn"]


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
            },
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
            },
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
