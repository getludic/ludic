from typing import cast, override

from ludic.attrs import GlobalAttrs
from ludic.html import table, tbody, thead, tr
from ludic.types import ComplexChild, Component, ComponentStrict, PrimitiveChild


class TableRow(Component[ComplexChild, GlobalAttrs]):
    def get_text(self, index: int) -> str:
        if len(self.children) > index:
            return self.children[index].text
        return ""

    @override
    def render(self) -> tr:
        return tr(*self.children, **self.attrs)


class TableHead(Component[ComplexChild, GlobalAttrs]):
    @property
    def header(self) -> tuple[PrimitiveChild, ...]:
        return tuple(child.text for child in self.children if self.children)

    @override
    def render(self) -> tr:
        return tr(*self.children, **self.attrs)


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
