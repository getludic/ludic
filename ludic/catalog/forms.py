from typing import Annotated, get_origin, get_type_hints, override

from ludic.attrs import FormAttrs, GlobalAttrs
from ludic.base import AnyChildren, AnyElement, BaseAttrs, Component
from ludic.html import div, form, input, label, select, textarea

from .utils import attr_to_camel


class FormField(Component[*tuple[label, input | textarea | select], GlobalAttrs]):
    @override
    def render(self) -> div:
        return div(*self.children, **self.attrs)


class Form(Component[*AnyChildren, FormAttrs]):
    @override
    def render(self) -> form:
        return form(*self.children, **self.attrs)


def create_fields[Ta: BaseAttrs](attrs_type: type[Ta], attrs: Ta) -> list[FormField]:
    """Create form fields from the given attributes.

    Example:

        class CustomerAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                FieldAttrs(label="Customer Name", type="input"),
            ]

        attrs = {"id": 1, "name": "John Doe"}
        fields = create_fields(CustomerAttrs, attrs)

        form = Form(*fields)

    Args:
        attrs_type (type[Ta]): The type of the attributes.
        attrs (Ta): The attributes to create the form fields from.
    """
    hints = get_type_hints(attrs_type, include_extras=True)
    elements: list[FormField] = []

    for name, annotation in hints.items():
        if name == "id":
            continue

        label_text: str = attr_to_camel(name)
        value = attrs.get(name, "")
        element_attrs = {
            "value": value,
            "name": name,
            "id": name,
            "class_": "form-control",
        }
        element: AnyElement = input(**element_attrs)

        if get_origin(annotation) is Annotated:
            for metadata in annotation.__metadata__:
                label_text = metadata.get("label", label_text)
                if metadata.get("type", "input") == "textarea":
                    element = textarea(**element_attrs)

        elements.append(
            FormField(
                label(label_text, for_=name, class_="form-label"),
                element,
            )
        )

    return elements
