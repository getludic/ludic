from ludic.attrs import ButtonAttrs
from ludic.html import button
from ludic.types import BaseElement, ComponentStrict, OnlyPrimitive


class Button(ComponentStrict[OnlyPrimitive, ButtonAttrs]):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn`` class.
    """

    def render(self) -> BaseElement:
        if extra_class := self.attrs.get("class_"):
            self.attrs["class_"] = f"{extra_class} btn"
        return button(self.children[0], **self.attrs)


class ButtonPrimary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-primary`` class.
    """

    def render(self) -> Button:
        if extra_class := self.attrs.get("class_"):
            self.attrs["class_"] = f"{extra_class} btn-primary"
        return Button(self.children[0], **self.attrs)


class ButtonSecondary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-secondary`` class.
    """

    def render(self) -> Button:
        if extra_class := self.attrs.get("class_"):
            self.attrs["class_"] = f"{extra_class} btn-secondary"
        return Button(self.children[0], **self.attrs)


class ButtonDanger(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-danger`` class.
    """

    def render(self) -> Button:
        if extra_class := self.attrs.get("class_"):
            self.attrs["class_"] = f"{extra_class} btn-danger"
        return Button(self.children[0], **self.attrs)


class ButtonWarning(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-warning`` class.
    """

    def render(self) -> Button:
        if extra_class := self.attrs.get("class_"):
            self.attrs["class_"] = f"{extra_class} btn-warning"
        return Button(self.children[0], **self.attrs)


class ButtonInfo(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-info`` class.
    """

    def render(self) -> Button:
        if extra_class := self.attrs.get("class_"):
            self.attrs["class_"] = f"{extra_class} btn-info"
        return Button(self.children[0], **self.attrs)
