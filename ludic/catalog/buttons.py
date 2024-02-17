from ludic.attrs import ButtonAttrs
from ludic.html import button
from ludic.types import BaseElement, Component, PrimitiveChild


class Button(Component[PrimitiveChild, ButtonAttrs]):
    def render(self) -> BaseElement:
        self.attrs.setdefault("class_", "btn")
        return button(self.children[0], **self.attrs_for(button))


class ButtonPrimary(Button):
    def render(self) -> Button:
        self.attrs.setdefault("class_", "btn btn-primary")
        return Button(self.children[0], **self.attrs_for(Button))


class ButtonSecondary(Button):
    def render(self) -> Button:
        self.attrs.setdefault("class_", "btn btn-secondary")
        return Button(self.children[0], **self.attrs_for(Button))


class ButtonDanger(Button):
    def render(self) -> Button:
        self.attrs.setdefault("class_", "btn btn-danger")
        return Button(self.children[0], **self.attrs_for(Button))


class ButtonWarning(Button):
    def render(self) -> Button:
        self.attrs.setdefault("class_", "btn btn-warning")
        return Button(self.children[0], **self.attrs_for(Button))


class ButtonInfo(Button):
    def render(self) -> Button:
        self.attrs.setdefault("class_", "btn btn-info")
        return Button(self.children[0], **self.attrs_for(Button))
