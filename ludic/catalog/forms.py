from typing import Annotated, Any, Literal, get_type_hints, override

from typeguard import check_type

from ludic.attrs import FormAttrs, GlobalAttrs
from ludic.base import AnyChildren, AnyElement, BaseAttrs, Component
from ludic.html import div, form, input, label, textarea


def attr_to_camel(name: str) -> str:
    return " ".join(value.title() for value in name.split("_"))


class FieldAttrs(BaseAttrs, total=False):
    label: str
    type: Literal["input", "textarea"]
    attrs: GlobalAttrs


class FormField(Component[*AnyChildren, GlobalAttrs]):
    @override
    def render(self) -> div:
        return div(*self.children, **self.attrs)


class Form(Component[*AnyChildren, FormAttrs]):
    @override
    def render(self) -> form:
        return form(*self.children, **self.attrs)


def form_fields(attrs: BaseAttrs) -> list[FormField]:
    """Create form fields from the given attributes.

    Example:

        class CustomerAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                FieldAttrs(label="Customer Name", type="input"),
            ]

        fields = form_fields(CustomerAttrs)

    Args:
        attrs (BaseAttrs): The attributes to create the form fields from.
    """
    hints = get_type_hints(attrs, include_extras=True)
    elements: list[FormField] = []

    for name, annotation in hints.items():
        if name == "id":
            continue

        label_text: str = attr_to_camel(name)
        value: str = str(attrs[name])  # type: ignore
        element: AnyElement = input(value=value, name=name, id=name)
        field_attrs: dict[str, Any] = {}

        if isinstance(annotation, Annotated):
            check_type(annotation.__metadata__, FieldAttrs)
            metadata = annotation.__metadata__
            label_text = metadata.get("label", label_text)
            if metadata.get("attrs"):
                field_attrs.update(metadata.attrs)

            match metadata.get("type"):
                case "textarea":
                    element = textarea(value, name=name, id=name)
                case _:
                    break

        elements.append(
            FormField(
                label(label_text, for_=name),
                element,
                **field_attrs,
            )
        )

    return elements
