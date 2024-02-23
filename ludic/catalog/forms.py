from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, get_type_hints, override

from ludic.attrs import BaseAttrs, FormAttrs, InputAttrs, TextAreaAttrs
from ludic.html import div, form, input, label, textarea
from ludic.types import (
    BaseElement,
    ComplexChild,
    Component,
    NoChild,
    PrimitiveChild,
    TAttrs,
    TChild,
)
from ludic.utils import get_annotations_metadata_of_type

from .utils import attr_to_camel

DEFAULT_FIELD_PARSERS: dict[str, Callable[[Any], PrimitiveChild]] = {
    "input": lambda value: value,
    "textarea": lambda value: value,
    "checkbox": lambda value: True if value == "on" else False,
}


@dataclass
class FieldMeta:
    """Class to be used in attributes annotations to create form fields.

    Example:
        def parse_email(email: str) -> str:
            if len(email.split("@")) != 2:
                raise ValidationError("Invalid email")
            return email

        class CustomerAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                FieldMeta(label="Email", parser=parse_email),
            ]
    """

    label: str | Literal["auto"] | None = "auto"
    kind: Literal["input", "textarea", "checkbox"] = "input"
    type: Literal["text", "email", "password", "hidden"] = "text"
    attrs: InputAttrs | TextAreaAttrs | None = None
    parser: Callable[[Any], PrimitiveChild] | None = None

    def create_field(self, key: str, value: Any) -> BaseElement:
        attrs = {} if self.attrs is None else dict(self.attrs)
        attrs["name"] = key

        if self.label:
            attrs["label"] = self.label
        elif self.label == "auto":
            attrs["label"] = attr_to_camel(key)

        match self.kind:
            case "input":
                return InputField(value=value, type=self.type, **attrs)
            case "checkbox":
                return InputField(checked=value, type="checkbox", **attrs)
            case "textarea":
                return TextAreaField(value=value, **attrs)

    def __call__(self, value: Any) -> PrimitiveChild:
        if self.parser:
            return self.parser(value)
        else:
            return DEFAULT_FIELD_PARSERS[self.kind](value)


class FieldAttrs(BaseAttrs, total=False):
    label: str
    class_div: str


class InputFieldAttrs(FieldAttrs, InputAttrs):
    pass


class TextAreaFieldAttrs(FieldAttrs, TextAreaAttrs):
    pass


class FormField(Component[TChild, TAttrs]):
    def create_label(self, text: PrimitiveChild, for_: str = "") -> label:
        if for_:
            return label(text, for_=for_)
        else:
            return label(text)


class InputField(FormField[NoChild, InputFieldAttrs]):
    @override
    def render(self) -> div:
        attrs = self.attrs_for(input)
        if "name" in self.attrs:
            attrs["id"] = self.attrs["name"]

        elements: list[ComplexChild] = []
        if text := self.attrs.get("label"):
            elements.append(self.create_label(text=text, for_=attrs.get("id", "")))
        elements.append(input(**attrs))

        return div(*elements, class_=self.attrs.get("class_div", "form-group"))


class TextAreaField(FormField[PrimitiveChild, TextAreaFieldAttrs]):
    @override
    def render(self) -> div:
        attrs = self.attrs_for(textarea)
        if "name" in self.attrs:
            attrs["id"] = self.attrs["name"]

        elements: list[ComplexChild] = []
        if text := self.attrs.get("label"):
            elements.append(self.create_label(text=text, for_=attrs.get("id", "")))
        elements.append(textarea(self.children[0], **attrs))

        return div(*elements, class_=self.attrs.get("class_div", "form-group"))


class Form(Component[ComplexChild, FormAttrs]):
    """A component helper for creating HTML forms."""

    @override
    def render(self) -> form:
        return form(*self.children, **self.attrs)


def create_fields(attrs: BaseAttrs, spec: type[TAttrs]) -> tuple[ComplexChild, ...]:
    """Create form fields from the given attributes.

    Example:

        class CustomerAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                FieldMeta(label="Customer Name"),
            ]

        customer = Customer(id=1, name="John Doe")
        fields = create_fields(customer, spec=CustomerAttrs)

        form = Form(*fields)

    Args:
        attrs (BaseAttrs): The attributes to create form fields from.
        spec (type[TAttrs]): The specification of the attributes.

    Returns:
        ComplexChild: list of form fields.
    """
    annotations = get_type_hints(spec, include_extras=True)
    metadata_list = get_annotations_metadata_of_type(annotations, FieldMeta)
    fields: list[ComplexChild] = []

    for name, metadata in metadata_list.items():
        if value := attrs.get(name):
            field = metadata.create_field(name, value)
            fields.append(field)

    return tuple(fields)
