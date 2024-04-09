from ludic.attrs import ButtonAttrs
from ludic.html import button, style
from ludic.types import ComponentStrict, PrimitiveChildren


class Button(ComponentStrict[PrimitiveChildren, ButtonAttrs]):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn`` class.
    """

    classes = ["btn"]
    styles = style.use(
        lambda theme: {
            "button.btn": {
                "background-color": theme.colors.light,
                "color": theme.colors.black,
                "margin": "8px 10px 8px 0px",
                "padding": "10px 17px",
                "border": f"1px solid {theme.colors.light.darken(0.1)}",
                "border-radius": "4px",
                "cursor": "pointer",
                "font-size": theme.fonts.sizes.medium,
                "transition": "0.1s filter linear, 0.1s -webkit-filter linear",
            },
            "button.btn:hover": {
                "filter": "brightness(85%)",
            },
            "button.btn.small": {
                "font-size": theme.fonts.sizes.small,
            },
            "button.btn.large": {
                "font-size": theme.fonts.sizes.large,
            },
        }
    )

    def render(self) -> button:
        return button(self.children[0], **self.attrs)


class ButtonPrimary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-primary`` class.
    """

    classes = ["btn", "btn-primary"]
    styles = style.use(
        lambda theme: {
            "button.btn-primary": {
                "color": theme.colors.primary.readable(),
                "background-color": theme.colors.primary,
                "border-color": theme.colors.primary.darken(0.05),
            }
        }
    )


class ButtonSecondary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-secondary`` class.
    """

    classes = ["btn", "btn-secondary"]
    styles = style.use(
        lambda theme: {
            "button.btn-secondary": {
                "color": theme.colors.secondary.readable(),
                "background-color": theme.colors.secondary,
                "border-color": theme.colors.secondary.darken(0.05),
            }
        }
    )


class ButtonSuccess(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-success`` class.
    """

    classes = ["btn", "btn-success"]
    styles = style.use(
        lambda theme: {
            "button.btn-success": {
                "color": theme.colors.success.readable(),
                "background-color": theme.colors.success,
                "border-color": theme.colors.success.darken(0.05),
            }
        }
    )


class ButtonDanger(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-danger`` class.
    """

    classes = ["btn", "btn-danger"]
    styles = style.use(
        lambda theme: {
            "button.btn-danger": {
                "color": theme.colors.danger.readable(),
                "background-color": theme.colors.danger,
                "border-color": theme.colors.danger.darken(0.05),
            }
        }
    )


class ButtonWarning(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-warning`` class.
    """

    classes = ["btn", "btn-warning"]
    styles = style.use(
        lambda theme: {
            "button.btn-warning": {
                "color": theme.colors.warning.readable(),
                "background-color": theme.colors.warning,
                "border-color": theme.colors.warning.darken(0.05),
            }
        }
    )


class ButtonInfo(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-info`` class.
    """

    classes = ["btn", "btn-info"]
    styles = style.use(
        lambda theme: {
            "button.btn-info": {
                "color": theme.colors.info.readable(),
                "background-color": theme.colors.info,
                "border-color": theme.colors.info.darken(0.05),
            }
        }
    )
