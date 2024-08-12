"""An experimental module for creating HTML forms."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, Literal, NotRequired, get_type_hints, override

from ludic.attrs import (
    Attrs,
    FormAttrs,
    InputAttrs,
    OptionAttrs,
    SelectAttrs,
    TextAreaAttrs,
)
from ludic.base import BaseElement
from ludic.catalog.typography import Paragraph
from ludic.components import Component
from ludic.html import div, form, input, label, option, select, style, textarea
from ludic.types import (
    ComplexChildren,
    NoChildren,
    PrimitiveChildren,
    TAttrs,
    TChildren,
)
from ludic.utils import get_annotations_metadata_of_type

from .utils import attr_to_camel

DEFAULT_FIELD_PARSERS: Mapping[str, Callable[[Any], PrimitiveChildren]] = {
    "checkbox": lambda value: True if value == "on" else False,
}


class SelectMetaAttrs(SelectAttrs):
    options: list[OptionAttrs]


@dataclass
class FieldMeta:
    """Class to be used in attributes annotations to create form fields.

    Example:

        def parse_email(email: str) -> str:
            if len(email.split("@")) != 2:
                raise ValidationError("Invalid email")
            return email

        class CustomerAttrs(Attrs):
            id: str
            name: Annotated[
                str,
                FieldMeta(label="Email", parser=parse_email),
            ]
    """

    label: str | Literal["auto"] | None = "auto"
    kind: Literal["input", "textarea", "checkbox", "select"] = "input"
    type: Literal["text", "email", "password", "hidden"] = "text"
    attrs: InputAttrs | TextAreaAttrs | SelectMetaAttrs | None = None
    parser: Callable[[Any], PrimitiveChildren] | None = None

    def format(self, key: str, value: Any) -> BaseElement:
        attrs = {} if self.attrs is None else dict(self.attrs)
        attrs["name"] = key

        if self.label == "auto":
            attrs["label"] = attr_to_camel(key)
        elif self.label:
            attrs["label"] = self.label

        match self.kind:
            case "input":
                return InputField(value=value, type=self.type, **attrs)
            case "checkbox":
                return InputField(checked=value, type="checkbox", **attrs)
            case "select":
                options: list[Option] = []

                for option_dict in attrs.pop("options", []):  # type: ignore
                    text = option_dict.pop("label", attr_to_camel(option_dict["value"]))
                    options.append(Option(text, **option_dict))

                return SelectField(*options, **attrs)
            case "textarea":
                return TextAreaField(value=value, **attrs)

    def parse(self, value: Any) -> PrimitiveChildren:
        if self.parser:
            return self.parser(value)
        else:
            return DEFAULT_FIELD_PARSERS.get(self.kind, str)(value)

    def __call__(self, value: Any) -> PrimitiveChildren:
        return self.parse(value)


class FieldAttrs(Attrs, total=False):
    """Shared attributes between custom form fields."""

    label: str


class InputFieldAttrs(FieldAttrs, InputAttrs):
    """Attributes of the component ``InputField``.

    The attributes are subclassed from :class:`FieldAttrs` and :class:`InputAttrs`.
    """


class SelectFieldAttrs(FieldAttrs, SelectAttrs):
    """Attributes of the component ``SelectField``.

    The attributes are subclassed from :class:`FieldAttrs` and :class:`SelectAttrs`.
    """


class TextAreaFieldAttrs(FieldAttrs, TextAreaAttrs):
    """Attributes of the component ``TextAreaField``.

    The attributes are subclassed from :class:`FieldAttrs` and :class:`TextAreaAttrs`.
    """


class FormField(Component[TChildren, TAttrs]):
    """Base class for form fields."""

    classes = ["form-field"]
    styles = style.use(
        lambda theme: {
            ".form-field label": {
                "display": "block",
                "font-weight": "bold",
                "margin-block-end": theme.sizes.xxs,
            },
            (".form-field input", ".form-field textarea", ".form-field select"): {
                "inline-size": "100%",
                "padding": f"{theme.sizes.xxxxs} {theme.sizes.xs}",
                "border": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(2)}"
                ),
                "border-radius": theme.rounding.normal,
                "box-sizing": "border-box",
                "font-size": theme.fonts.size * 0.9,
                "transition": "all 0.3s ease-in-out",
                "resize": "vertical",
                "background-color": theme.colors.white,
            },
            (".form-field input", ".form-field select"): {
                "height": theme.sizes.xxxxl,
            },
            ".form-field input[type=checkbox]": {
                "height": theme.sizes.m,
                "width": theme.sizes.m,
            },
            (
                ".form-field input:focus",
                ".form-field textarea:focus",
                ".form-field select:focus",
            ): {
                "outline": "none",
                "border-color": theme.colors.light.darken(7),
                "border-width": theme.borders.thin,
            },
        }
    )

    def create_label(self, text: PrimitiveChildren, for_: str = "") -> label:
        if for_:
            return label(text, for_=for_)
        else:
            return label(text)


class InputField(FormField[NoChildren, InputFieldAttrs]):
    """Represents the HTML ``input`` element with an optional ``label`` element."""

    @override
    def render(self) -> div:
        attrs = self.attrs_for(input)
        if "name" in self.attrs:
            attrs["id"] = self.attrs["name"]

        elements: list[ComplexChildren] = []
        if text := self.attrs.get("label"):
            elements.append(self.create_label(text=text, for_=attrs.get("id", "")))
        elements.append(input(**attrs))

        return div(*elements)


class Option(Component[PrimitiveChildren, OptionAttrs]):
    """Represents the HTML ``option`` element."""

    @override
    def render(self) -> option:
        return option(*self.children, **self.attrs)


class SelectField(FormField[Option, SelectFieldAttrs]):
    """Represents the HTML ``input`` element with an optional ``label`` element."""

    @override
    def render(self) -> div:
        attrs = self.attrs_for(select)
        if "name" in self.attrs:
            attrs["id"] = self.attrs["name"]

        elements: list[ComplexChildren] = []
        if text := self.attrs.get("label"):
            elements.append(self.create_label(text=text, for_=attrs.get("id", "")))
        elements.append(select(*self.children, **attrs))

        return div(*elements)


class ChoiceFieldAttrs(FieldAttrs, InputAttrs):
    """Attributes of the component ``InputField``.

    The attributes are subclassed from :class:`FieldAttrs` and :class:`InputAttrs`.
    """

    choices: list[tuple[str, str]]
    selected: NotRequired[str]


class ChoiceField(FormField[NoChildren, ChoiceFieldAttrs]):
    """Represents the HTML ``input`` element with an optional ``label`` element."""

    styles = style.use(
        lambda theme: {
            ".form-field p.form-label": {
                "margin-block-end": theme.sizes.xxs,
                "font-weight": "bold",
            },
            ".form-field * + *": {
                "margin-block-start": theme.sizes.xxxxs,
            },
            ".form-field input[type=radio]": {
                "inline-size": "auto",
                "vertical-align": "middle",
                "height": theme.sizes.m,
                "margin-inline": theme.sizes.m,
            },
            ".form-field input[type=radio] + label": {
                "display": "inline-block",
                "height": theme.sizes.m,
                "font-weight": "normal",
                "margin-block": "0",
            },
        }
    )

    @override
    def render(self) -> div:
        attrs = self.attrs_for(input)
        attrs.setdefault("type", "radio")

        elements: list[ComplexChildren] = []

        if text := self.attrs.get("label"):
            elements.append(Paragraph(text, classes=["form-label"]))

        for value, text in self.attrs["choices"]:
            elements.append(
                div(
                    input(
                        id=value,
                        value=value,
                        checked=bool(value and value == self.attrs.get("selected")),
                        **attrs,
                    ),
                    label(text, for_=value),
                    classes=["choice-field"],
                )
            )

        return div(*elements)


class TextAreaField(FormField[PrimitiveChildren, TextAreaFieldAttrs]):
    """Represents the HTML ``textarea`` element with an optional ``label`` element."""

    @override
    def render(self) -> div:
        attrs = self.attrs_for(textarea)
        if "name" in self.attrs:
            attrs["id"] = self.attrs["name"]

        elements: list[ComplexChildren] = []
        if text := self.attrs.get("label"):
            elements.append(self.create_label(text=text, for_=attrs.get("id", "")))
        elements.append(textarea(*self.children, **attrs))

        return div(*elements)


class Form(Component[ComplexChildren, FormAttrs]):
    """A component helper for creating HTML forms."""

    classes = ["form", "stack"]

    @override
    def render(self) -> form:
        return form(*self.children, **self.attrs)


def create_fields(attrs: Any, spec: type[TAttrs]) -> tuple[ComplexChildren, ...]:
    """Create form fields from the given attributes.

    Example:

        class CustomerAttrs(Attrs):
            id: str
            name: Annotated[
                str,
                FieldMeta(label="Customer Name"),
            ]

        customer = CustomerAttrs(id=1, name="John Doe")
        fields = create_fields(customer, spec=CustomerAttrs)

        form = Form(*fields)

    Args:
        attrs (Any): The attributes to create form fields from.
        spec (type[TAttrs]): The specification of the attributes.

    Returns:
        ComplexChild: list of form fields.
    """
    annotations = get_type_hints(spec, include_extras=True)
    metadata_list = get_annotations_metadata_of_type(annotations, FieldMeta)
    fields: list[ComplexChildren] = []

    for name, metadata in metadata_list.items():
        if value := (attrs.get(name) or getattr(attrs, name, None)):
            field = metadata.format(name, value)
            fields.append(field)

    return tuple(fields)
