from typing import Annotated, cast, get_type_hints, override

from typeguard import check_type

from ludic.attrs import BaseAttrs, GlobalAttrs
from ludic.base import ComplexChildren, Component, PrimitiveChild, PrimitiveChildren
from ludic.html import table, tbody, td, th, thead, tr

from .utils import attr_to_camel


class ColumnAttrs(BaseAttrs, total=False):
    label: str
    attrs: GlobalAttrs


class TableRow(Component[*ComplexChildren, GlobalAttrs]):
    def get_text(self, index: int) -> str:
        if len(self.children) > index:
            return self.children[index].text
        return ""

    @override
    def render(self) -> tr:
        return tr(*self.children, **self.attrs)


class TableHead(Component[*ComplexChildren, GlobalAttrs]):
    @property
    def header(self) -> PrimitiveChildren:
        return tuple(child.text for child in self.children if self.children)

    @override
    def render(self) -> tr:
        return tr(*self.children, **self.attrs)


class Table(Component[TableHead, *tuple[TableRow, ...], GlobalAttrs]):
    @property
    def header(self) -> PrimitiveChildren:
        return self.children[0].header

    def getlist(self, key: str) -> list[PrimitiveChild | None]:
        result: list[PrimitiveChild | None] = []

        for idx, head in enumerate(self.header):
            if key != head:
                continue

            rows: list[TableRow] = cast(list[TableRow], self.children[1:])
            for row in rows:
                if value := row.get_text(idx):
                    result.append(value)

        return result

    @override
    def render(self) -> table:
        return table(thead(self.children[0]), tbody(*self.children[1:]), **self.attrs)


def create_table[Ta: BaseAttrs](
    attrs_type: type[Ta], *attrs_list: Ta
) -> tuple[TableHead, list[TableRow]]:
    """Create table from the given attributes.

    Example:

        class CustomerAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                FieldAttrs(label="Customer Name", type="input"),
            ]

        header, rows = create_table(
            CustomerAttrs,
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Doe"},
        )

        table = Table(header, *rows)

    Args:
        attrs_type (type[Ta]): The table header - The names of attributes to create
            the table header from.
        *attrs_list (BaseAttrs): The table body - the values of attributes to create
            the table body from.
    """
    hints = get_type_hints(attrs_type, include_extras=True)

    header_names: list[str] = []
    annotations: dict[str, tuple[str, GlobalAttrs]] = {}
    rows: list[TableRow] = []

    for name, annotation in hints.items():
        label_text: str = attr_to_camel(name)
        column_attrs: GlobalAttrs = {}

        if isinstance(annotation, Annotated):
            check_type(annotation.__metadata__, ColumnAttrs)
            metadata = annotation.__metadata__
            label_text = metadata.get("label", label_text)
            if metadata.get("attrs"):
                column_attrs.update(metadata.attrs)

        annotations[name] = (label_text, column_attrs)
        header_names.append(label_text)

    header = TableHead(*map(th, header_names))

    for attrs in attrs_list:
        values: list[td] = []
        for key, value in attrs.items():
            label_text, column_attrs = annotations[key]
            values.append(td(str(value), **column_attrs))
        rows.append(TableRow(*values))

    return (header, rows)
