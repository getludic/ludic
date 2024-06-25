"""An experimental module for creating HTML tables."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal, cast, get_type_hints, override

from typing_extensions import TypeVar

from ludic.attrs import GlobalAttrs
from ludic.base import BaseElement
from ludic.components import Component, ComponentStrict
from ludic.html import div, style, table, tbody, td, th, thead, tr
from ludic.types import (
    AnyChildren,
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

    def get_value(self, index: int) -> PrimitiveChildren | None:
        if len(self.children) > index:
            child = self.children[index]
            return child.text if isinstance(child, BaseElement) else child
        return None

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


class TableAttrs(GlobalAttrs, total=False):
    head_attrs: GlobalAttrs
    body_attrs: GlobalAttrs


class Table(ComponentStrict[THead, *tuple[TRow, ...], TableAttrs]):
    """A component rendering as the HTML ``table`` element.

    The component allows :class:`TableHead` and :class:`TableRow` types by default.

    Example:

        Table(
            TableHead("Name", "Age"),
            TableRow("John", 42),
            TableRow("Jane", 23),
        )

    You can also specify different types of header and body:

        Table[PersonHead, PersonRow](
            PersonHead("Name", "Age"),
            PersonRow("John", 42),
        )
    """

    classes = ["table"]
    styles = style.use(
        lambda theme: {
            ".table": {
                "overflow": "auto",
            },
            ".table > table": {
                "inline-size": "100%",  # type: ignore
                "border-collapse": "collapse",  # type: ignore
                "thead": {
                    "background-color": theme.colors.light,
                },
                "tr th": {
                    "border": (
                        f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                    ),
                    "padding": f"{theme.sizes.xxs} {theme.sizes.xxxs}",
                },
                "tr td": {
                    "border": (
                        f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                    ),
                    "padding": f"{theme.sizes.xxs} {theme.sizes.xxxs}",
                },
            },
        }
    )

    @property
    def header(self) -> tuple[PrimitiveChildren, ...]:
        if isinstance(self.children[0], TableHead):
            return self.children[0].header
        return ()

    def getlist(self, key: str) -> list[PrimitiveChildren | None]:
        result: list[PrimitiveChildren | None] = []

        for idx, head in enumerate(self.header):
            if key != head:
                continue

            rows: list[TableRow] = cast(list[TableRow], self.children[1:])
            for row in rows:
                if value := row.get_value(idx):
                    result.append(value)

        return result

    @override
    def render(self) -> div:
        return div(
            table(
                thead(self.children[0], **self.attrs.get("head_attrs", {})),
                tbody(*self.children[1:], **self.attrs.get("body_attrs", {})),
                **self.attrs_for(table),
            ),
        )


def create_rows(
    attrs_list: list[TAttrs], spec: type[TAttrs], include_id_column: bool = True
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
