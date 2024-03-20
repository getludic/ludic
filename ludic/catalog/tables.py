"""An experimental module for creating HTML tables."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, cast, get_type_hints, override

from typing_extensions import TypeVar

from ludic.attrs import GlobalAttrs
from ludic.html import table, tbody, td, th, thead, tr
from ludic.types import (
    AnyChildren,
    BaseElement,
    Component,
    ComponentStrict,
    PrimitiveChildren,
    TAttrs,
)
from ludic.utils import get_annotations_metadata_of_type

from .forms import FieldMeta
from .utils import attr_to_camel


@dataclass
class ColumnMeta:
    """Class to be used as an annotation for attributes.

    Example:

        class PersonAttrs(Attrs):
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
    parser: Callable[[Any], PrimitiveChildren] | None = None

    def format(self, key: str, value: Any) -> Any:
        if isinstance(self.kind, FieldMeta):
            return self.kind.format(key, value)
        return value

    def parse(self, value: Any) -> PrimitiveChildren:
        if self.kind == "text":
            return value if self.parser is None else self.parser(value)
        return self.kind(value)

    def __call__(self, value: Any) -> PrimitiveChildren:
        return self.parse(value)


class TableRow(Component[AnyChildren, GlobalAttrs]):
    """Simple component rendering as the HTML ``tr`` element."""

    def get_text(self, index: int) -> str:
        if len(self.children) > index:
            child = self.children[index]
            return child.text if isinstance(child, BaseElement) else str(child)
        return ""

    @override
    def render(self) -> tr:
        return tr(
            *(child if isinstance(child, td) else td(child) for child in self.children),
            **self.attrs,
        )


class TableHead(Component[AnyChildren, GlobalAttrs]):
    """Simple component rendering as the HTML ``tr`` element."""

    @property
    def header(self) -> tuple[PrimitiveChildren, ...]:
        return tuple(
            child.text if isinstance(child, BaseElement) else str(child)
            for child in self.children
            if self.children
        )

    @override
    def render(self) -> tr:
        return tr(
            *(child if isinstance(child, th) else th(child) for child in self.children),
            **self.attrs,
        )


THead = TypeVar("THead", bound=BaseElement, default=TableHead)
TRow = TypeVar("TRow", bound=BaseElement, default=TableRow)


class TableType(ComponentStrict[THead, *tuple[TRow, ...], GlobalAttrs]):
    """A component rendering as the HTML ``table`` element.

    The component allows specifying the table head and rows types:

        TableType[PersonHead, PersonRow](
            PersonHead("Name", "Age"),
            PersonRow("John", 42),
            PersonRow("Jane", 23),
        )
    """

    @override
    def render(self) -> table:
        return table(thead(self.children[0]), tbody(*self.children[1:]), **self.attrs)


class Table(TableType[TableHead, TableRow]):
    """A component rendering as the HTML ``table`` element.

    The component only allows :class:`TableHead` and :class:`TableRow` types.

    Example:

        Table(
            TableHead("Name", "Age"),
            TableRow("John", 42),
            TableRow("Jane", 23),
        )
    """

    @property
    def header(self) -> tuple[PrimitiveChildren, ...]:
        return self.children[0].header

    def getlist(self, key: str) -> list[PrimitiveChildren | None]:
        result: list[PrimitiveChildren | None] = []

        for idx, head in enumerate(self.header):
            if key != head:
                continue

            rows: list[TableRow] = cast(list[TableRow], self.children[1:])
            for row in rows:
                if value := row.get_text(idx):
                    result.append(value)

        return result


def create_rows(
    attrs_list: list[TAttrs], spec: type[TAttrs], include_id_column: bool = False
) -> tuple[TableHead, *tuple[TableRow, ...]]:
    """Create table rows from the given attributes.

    Example:

        class PersonAttrs(Attrs):
            id: Annotated[int, ColumnMeta(identifier=True)]
            name: Annotated[str, ColumnMeta(label="Full Name")]
            email: Annotated[str, ColumnMeta(label="Email")]

        people = [
            {"id": 1, "name": "John Doe", "email": "john@j.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@s.com"},
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
        cells: list[AnyChildren] = []

        for key, value in attrs.items():
            if meta := matadata.get(key):
                if meta.identifier and not include_id_column:
                    continue
                name = f"{key}:{id_col_name}:{attrs.get(id_col_name, str(idx))}"
                cells.append(meta.format(name, value))

        if cells:
            rows.append(TableRow(*cells))

    return TableHead(*headers), *rows
