from ludic.attrs import ButtonAttrs
from ludic.base import AnyElement, Component, PrimitiveChild
from ludic.html import button


class Button(Component[PrimitiveChild, ButtonAttrs]):
    def render(self) -> AnyElement:
        return button(self.children[0], class_=self.attrs.get("class_", "btn"))


class ButtonPrimary(Button):
    def render(self) -> Button:
        return Button(self.children[0], class_="btn btn-primary")


class ButtonSecondary(Button):
    def render(self) -> Button:
        return Button(self.children[0], class_="btn btn-primary")


class ButtonDanger(Button):
    def render(self) -> Button:
        return Button(self.children[0], class_="btn btn-danger")


class ButtonWarning(Button):
    def render(self) -> Button:
        return Button(self.children[0], class_="btn btn-warning")


class ButtonInfo(Button):
    def render(self) -> Button:
        return Button(self.children[0], class_="btn btn-info")
