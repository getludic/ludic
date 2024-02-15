from typing import cast, override

from ludic.attrs import GlobalAttrs
from ludic.base import ComplexChildren, Component, PrimitiveChild, PrimitiveChildren
from ludic.html import table, tbody, thead, tr


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
