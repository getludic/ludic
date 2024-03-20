from typing import Self, override

from examples import Body, Header, Page, app
from ludic.attrs import ButtonAttrs
from ludic.catalog.buttons import ButtonPrimary
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.html import td
from ludic.types import Attrs, Blank, Component, ComponentStrict
from ludic.web import Endpoint
from ludic.web.datastructures import QueryParams


class ContactAttrs(Attrs):
    id: str
    name: str
    email: str


class ContactsSliceAttrs(Attrs):
    page: int
    contacts: list[ContactAttrs]


class LoadMoreAttrs(ButtonAttrs):
    url: str


def load_contacts(page: int) -> list[ContactAttrs]:
    return [
        ContactAttrs(
            id=str(page * 10 + idx),
            email=f"void{page * 10 + idx}@null.org",
            name="Agent Smith",
        )
        for idx in range(10)
    ]


class LoadMoreButton(ComponentStrict[LoadMoreAttrs]):
    target: str = "replace-me"

    @override
    def render(self) -> ButtonPrimary:
        return ButtonPrimary(
            "Load More Agents...",
            hx_get=self.attrs["url"],
            hx_target=f"#{self.target}",
            hx_swap="outerHTML",
        )


class ContactsTable(Component[TableRow, Attrs]):
    @override
    def render(self) -> Table:
        return Table(
            TableHead("ID", "Name", "Email"),
            *self.children,
            style={"text-align": "center"},
        )


@app.get("/")
async def index() -> Page:
    slice = await ContactsSlice.get(QueryParams(page=1))
    return Page(
        Header("Click To Edit"),
        Body(ContactsTable(*slice.render().children)),
    )


@app.endpoint("/contacts/")
class ContactsSlice(Endpoint[ContactsSliceAttrs]):
    @classmethod
    async def get(cls, params: QueryParams) -> Self:
        page = int(params.get("page", 1))
        return cls(page=page, contacts=load_contacts(page))

    @override
    def render(self) -> Blank[TableRow]:
        next_page = self.attrs["page"] + 1
        return Blank(
            *(
                TableRow(contact["id"], contact["name"], contact["email"])
                for contact in self.attrs["contacts"]
            ),
            TableRow(
                td(
                    LoadMoreButton(
                        url=self.url_for(ContactsSlice).query(page=next_page)
                    ),
                    colspan=3,
                ),
                id=LoadMoreButton.target,
            ),
        )
