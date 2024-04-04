from typing import Self, override

from examples import Body, Header, Page, app
from ludic.catalog.quotes import Quote
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.types import Attrs, Blank, Component
from ludic.web import Endpoint
from ludic.web.datastructures import QueryParams


class ContactAttrs(Attrs):
    id: str
    name: str
    email: str


class ContactsSliceAttrs(Attrs):
    page: int
    contacts: list[ContactAttrs]


def load_contacts(page: int) -> list[ContactAttrs]:
    return [
        ContactAttrs(
            id=str(page * 10 + idx),
            email=f"void{page * 10 + idx}@null.org",
            name="Agent Smith",
        )
        for idx in range(10)
    ]


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
        Header("Infinite Scroll"),
        Body(
            Quote(
                "The infinite scroll pattern provides a way to load content dynamically"
                "on user scrolling action.",
                source_url="https://htmx.org/examples/infinite-scroll/",
            ),
            ContactsTable(*slice.render().children),
        ),
    )


@app.endpoint("/contacts/")
class ContactsSlice(Endpoint[ContactsSliceAttrs]):
    @classmethod
    async def get(cls, params: QueryParams) -> Self:
        page = int(params.get("page", 1))
        return cls(page=page, contacts=load_contacts(page))

    @override
    def render(self) -> Blank[TableRow]:
        *init, last = (
            (contact["id"], contact["name"], contact["email"])
            for contact in self.attrs["contacts"]
        )
        return Blank(
            *(TableRow(*rows) for rows in init),
            TableRow(
                *last,
                hx_get=self.url_for(ContactsSlice).query(page=self.attrs["page"] + 1),
                hx_trigger="revealed",
                hx_swap="afterend",
            ),
        )
