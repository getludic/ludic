from dataclasses import dataclass
from typing import Any, Literal, cast, get_type_hints, override

from ludic.attrs import GlobalAttrs
from ludic.html import table, tbody, td, th, thead, tr
from ludic.types import (
    AnyChild,
    BaseElement,
    Component,
    ComponentStrict,
    PrimitiveChild,
    TAttrs,
)
from ludic.utils import get_annotations_metadata_of_type

from .forms import FieldMeta
from .utils import attr_to_camel


@dataclass
class ColumnMeta:
    """Class to be used as an annotation for attributes.

    Example:

        class PersonAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                ColumnMeta(label="Full Name"),
            ]
            email: Annotated[
                str,
                ColumnMeta(label="Email"),
            ]
    """

    identifier: bool = False
    label: str | None = None
    kind: Literal["text"] | FieldMeta = "text"

    def __call__(self, value: Any) -> PrimitiveChild:
        if self.kind == "text":
            return value
        return self.kind(value)


class TableRow(Component[AnyChild, GlobalAttrs]):
    def get_text(self, index: int) -> str:
        if len(self.children) > index:
            child = self.children[index]
            return child.text if isinstance(child, BaseElement) else str(child)
        return ""

    @override
    def render(self) -> tr:
        return tr(*map(td, self.children), **self.attrs)


class TableHead(Component[AnyChild, GlobalAttrs]):
    @property
    def header(self) -> tuple[PrimitiveChild, ...]:
        return tuple(
            child.text if isinstance(child, BaseElement) else str(child)
            for child in self.children
            if self.children
        )

    @override
    def render(self) -> tr:
        return tr(*map(th, self.children), **self.attrs)


class Table(ComponentStrict[TableHead, *tuple[TableRow, ...], GlobalAttrs]):
    @property
    def header(self) -> tuple[PrimitiveChild, ...]:
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


def create_rows(
    attrs_list: list[TAttrs], spec: type[TAttrs], include_id_column: bool = False
) -> tuple[TableHead, *tuple[TableRow, ...]]:
    """Create table rows from the given attributes.

    Example:

        class PersonAttrs(BaseAttrs):
            id: str
            name: Annotated[
                str,
                ColumnMeta(label="Full Name"),
            ]
            email: Annotated[
                str,
                ColumnMeta(label="Email"),
            ]

        people = [
            Person(id=1, name="John Doe", email="john@j.com"),
            Person(id=2, name="Jane Smith", email="jane@s.com"),
        ]
        rows = create_rows(people, spec=PersonAttrs)

        table = Table(*rows)

    Args:
        attrs_list (list[TAttrs]): The list of attributes to create table rows from.
        spec (type[TAttrs]): The specification of the attributes.

    Returns:
        tuple[TableHead, *tuple[TableRow, ...]]: list of table rows including header.
    """
    annotations = get_type_hints(spec, include_extras=True)
    matadata = get_annotations_metadata_of_type(annotations, ColumnMeta)

    id_col_name: str = "_index"
    headers = []
    for key, col_meta in matadata.items():
        if col_meta.identifier:
            id_col_name = key
        if not col_meta.identifier or include_id_column:
            headers.append(col_meta.label or attr_to_camel(key))

    rows: list[TableRow] = []
    for idx, attrs in enumerate(attrs_list):
        cells: list[AnyChild] = []
        for key, value in attrs.items():
            if meta := matadata.get(key):
                if meta.identifier and not include_id_column:
                    continue
                if isinstance(meta.kind, FieldMeta):
                    name = f"{key}:{id_col_name}:{attrs.get(id_col_name, str(idx))}"
                    cells.append(meta.kind.create_field(name, value))
                else:
                    cells.append(value)  # type: ignore
        if cells:
            rows.append(TableRow(*cells))

    return TableHead(*headers), *rows