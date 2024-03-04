from ludic.attrs import ButtonAttrs
from ludic.html import button
from ludic.types import ComponentStrict, PrimitiveChildren


class Button(ComponentStrict[PrimitiveChildren, ButtonAttrs]):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn`` class.
    """

    class_name = "btn"

    def render(self) -> button:
        if extra_class := self.attrs.get("class_", ""):
            self.attrs["class_"] = f"{extra_class} {self.class_name}"
        else:
            self.attrs["class_"] = self.class_name
        return button(self.children[0], **self.attrs)


class ButtonPrimary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-primary`` class.
    """

    class_name = "btn btn-primary"


class ButtonSecondary(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-secondary`` class.
    """

    class_name = "btn btn-secondary"


class ButtonDanger(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-danger`` class.
    """

    class_name = "btn btn-danger"


class ButtonWarning(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-warning`` class.
    """

    class_name = "btn btn-warning"


class ButtonInfo(Button):
    """Simple component creating an HTML button.

    The component creates a button with the ``btn btn-info`` class.
    """

    class_name = "btn btn-info"
