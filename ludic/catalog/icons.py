from typing import override

from ludic.attrs import GlobalAttrs, ImgAttrs
from ludic.components import Component, ComponentStrict
from ludic.html import img, span, style
from ludic.types import AnyChildren, NoChildren


class Icon(Component[NoChildren, ImgAttrs]):
    classes = ["icon"]
    styles = {
        ".icon": {
            "width": "0.75em",
            "height": "0.75em",
        },
    }

    @override
    def render(self) -> img:
        return img(*self.children, **self.attrs)


class WithIcon(ComponentStrict[Icon, AnyChildren, GlobalAttrs]):
    classes = ["with-icon"]
    styles = style.use(
        lambda theme: {
            ".with-icon": {
                "display": "inline-flex",
                "align-items": "baseline",
            },
            ".with-icon .icon": {
                "margin-inline-end": theme.sizes.s,
            },
        }
    )

    @override
    def render(self) -> span:
        return span(*self.children, **self.attrs)
