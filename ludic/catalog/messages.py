from typing import override

from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import div, style
from ludic.types import AnyChildren


class Title(Component[AnyChildren, GlobalAttrs]):
    classes = ["title"]

    @override
    def render(self) -> div:
        return div(*self.children)


class Message(Component[AnyChildren, GlobalAttrs]):
    classes = ["message"]
    styles = style.use(
        lambda theme: {
            ".message": {
                "background-color": theme.colors.white,
                "border": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
                "border-radius": theme.rounding.less,
                "font-size": theme.fonts.size * 0.9,
            },
            ".message > .title": {
                "padding-inline": theme.sizes.l,
                "padding-block": theme.sizes.s,
                "color": theme.colors.light.readable(),
                "background-color": theme.colors.light,
            },
            ".message > .content": {
                "padding-inline": theme.sizes.l,
                "padding-block": theme.sizes.s,
            },
        }
    )

    @override
    def render(self) -> div:
        if self.children and isinstance(self.children[0], Title):
            return div(
                self.children[0],
                div(*self.children[1:], classes=["content"]),
                **self.attrs,
            )
        else:
            return div(div(*self.children, classes=["content"]), **self.attrs)


class MessageSuccess(Message):
    classes = ["message", "success"]
    styles = style.use(
        lambda theme: {
            ".message.success > .title": {
                "color": theme.colors.success.lighten(1).readable(),
                "background-color": theme.colors.success.lighten(1),
            },
            ".message.success": {
                "border-color": theme.colors.success,
            },
        }
    )


class MessageInfo(Message):
    classes = ["message", "info"]
    styles = style.use(
        lambda theme: {
            ".message.info > .title": {
                "color": theme.colors.info.lighten(1).readable(),
                "background-color": theme.colors.info.lighten(1),
            },
            ".message.info": {
                "border-color": theme.colors.info,
            },
        }
    )


class MessageWarning(Message):
    classes = ["message", "warning"]
    styles = style.use(
        lambda theme: {
            ".message.warning > .title": {
                "color": theme.colors.warning.lighten(1).readable(),
                "background-color": theme.colors.warning.lighten(1),
            },
            ".message.warning": {
                "border-color": theme.colors.warning,
            },
        }
    )


class MessageDanger(Message):
    classes = ["message", "danger"]
    styles = style.use(
        lambda theme: {
            ".message.danger > .title": {
                "color": theme.colors.danger.lighten(1).readable(),
                "background-color": theme.colors.danger.lighten(1),
            },
            ".message.danger": {
                "border-color": theme.colors.danger,
            },
        }
    )
