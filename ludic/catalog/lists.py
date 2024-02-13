from typing import Annotated, get_origin, get_type_hints, override

from ludic.attrs import BaseAttrs, GlobalAttrs
from ludic.base import Component, PrimitiveChildren
from ludic.html import dd, dl, dt

from .utils import attr_to_camel


class Key(Component[*PrimitiveChildren, GlobalAttrs]):
    @override
    def render(self) -> dt:
        return dt(*self.children, **self.attrs)


class Value(Component[*PrimitiveChildren, GlobalAttrs]):
    @override
    def render(self) -> dd:
        return dd(*self.children, **self.attrs)


class Items(Component[*tuple[Key | Value, ...], GlobalAttrs]):
    @override
    def render(self) -> dl:
        return dl(*self.children, **self.attrs)


def create_items[Ta: BaseAttrs](attrs_type: type[Ta], attrs: Ta) -> list[Key | Value]:
    """Create description list from the given attributes.

    Example:

        class CustomerAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                {"label": "Customer Name"},
            ]

        attrs = {"id": 1, "name": "John Doe"}
        fields = create_items(CustomerAttrs, attrs)

        items = Items(*fields)

    Args:
        attrs_type (type[Ta]): The type of the attributes.
        attrs (Ta): The attributes to create the description list from.
    """
    hints = get_type_hints(attrs_type, include_extras=True)
    items: list[Key | Value] = []

    for name, annotation in hints.items():
        label_text: str = attr_to_camel(name)

        if get_origin(annotation) is Annotated:
            for metadata in annotation.__metadata__:
                label_text = metadata.get("label", label_text)

        items.append(Key(label_text))
        items.append(Value(str(attrs.get(name, ""))))

    return items
