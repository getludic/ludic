from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, override

from ludic.attrs import BaseAttrs, FormAttrs, InputAttrs, TextAreaAttrs
from ludic.html import div, form, input, label, textarea
from ludic.types import (
    BaseElement,
    ComplexChild,
    Component,
    PrimitiveChild,
    TAttrs,
    TChildren,
)
from ludic.utils import get_annotations_metadata_of_type, get_element_attrs_annotations

from .utils import attr_to_camel


class ValidationError(Exception):
    reason: str

    def __init__(self, reason: str) -> None:
        self.reason = reason


@dataclass
class FieldMeta:
    """Class to be used as an annotation for attributes.

    Example:
        def validate_email(email: str) -> str:
            if len(email.split("@")) != 2:
                raise ValidationError("Invalid email")
            return email

        class CustomerAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                FieldMeta(label="Email", validator=validate_email),
            ]
    """

    label: str | None = None
    kind: Literal["input", "textarea"] = "input"
    type: Literal["text", "number", "email", "password", "hidden"] = "text"
    attrs: InputAttrs | TextAreaAttrs | None = None
    validator: Callable[[Any], PrimitiveChild] = str

    def create_field(self, key: str, value: Any) -> BaseElement:
        value = self.validator(value)
        attrs = self.attrs or {}
        attrs["name"] = key

        match self.kind:
            case "input":
                return InputField(value, label=self.label, type=self.type, **attrs)
            case "textarea":
                return TextAreaField(value, label=self.label, **attrs)


class FieldAttrs(BaseAttrs, total=False):
    label: str
    class_div: str


class InputFieldAttrs(FieldAttrs, InputAttrs):
    pass


class TextAreaFieldAttrs(FieldAttrs, TextAreaAttrs):
    pass


class FormField(Component[TChildren, TAttrs]):
    def get_label_text(self) -> str:
        return f"{self.attrs.get("label") or attr_to_camel(str(self.children[0]))}: "


class InputField(FormField[PrimitiveChild, InputFieldAttrs]):
    @override
    def render(self) -> div:
        label_attrs = {}
        input_attrs = self.attrs_for(input)
        if "name" in self.attrs:
            input_attrs["id"] = label_attrs["for_"] = self.attrs["name"]

        return div(
            label(self.get_label_text(), **label_attrs),
            input(value=self.children[0], **input_attrs),
            class_=self.attrs.get("class_div", "form-input"),
        )


class TextAreaField(FormField[PrimitiveChild, TextAreaFieldAttrs]):
    @override
    def render(self) -> div:
        label_attrs = {}
        textarea_attrs = self.attrs_for(textarea)
        if "name" in self.attrs:
            textarea_attrs["id"] = label_attrs["for_"] = self.attrs["name"]

        return div(
            label(self.get_label_text(), **label_attrs),
            textarea(self.children[0], **textarea_attrs),
            class_=self.attrs.get("class_div", "form-textarea"),
        )


class Form(Component[ComplexChild, FormAttrs]):
    """A component helper for creating HTML forms."""

    @staticmethod
    def create_fields(element: BaseElement) -> tuple[ComplexChild, ...]:
        """Create form fields from the given attributes.

        Example:

            class CustomerAttrs(BaseAttrs):
                id: str
                name: Annotated[
                    str,
                    InputMeta(label="Customer Name"),
                ]

            class Customer(Component[BaseAttrs]):
                def render(self): ...

            customer = Customer(id=1, name="John Doe")
            fields = Form.create_fields(customer)

            form = Form(*fields)

        Args:
            element (Element): The element to create forms from.

        Returns:
            ComplexChild: list of form fields.
        """
        annotations = get_element_attrs_annotations(element, include_extras=True)
        metadata_list = get_annotations_metadata_of_type(annotations, FieldMeta)
        fields: list[ComplexChild] = []

        for name, metadata in metadata_list.items():
            if name in element.attrs:
                field = metadata.create_field(name, element.attrs[name])
                fields.append(field)

        return tuple(fields)

    @override
    def render(self) -> form:
        return form(*self.children, **self.attrs)
