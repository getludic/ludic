from typing import Self, override

from examples import Page

from ludic.attrs import Attrs
from ludic.catalog.headers import H1, H2
from ludic.catalog.quotes import Quote
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.components import Component
from ludic.elements import Blank
from ludic.web import Endpoint, LudicApp
from ludic.web.datastructures import QueryParams

app = LudicApp(debug=True)


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


@app.get("/")
async def index() -> Page:
    return Page(
        H1("Infinite Scroll"),
        Quote(
            "The infinite scroll pattern provides a way to load content dynamically"
            "on user scrolling action.",
            source_url="https://htmx.org/examples/infinite-scroll/",
        ),
        H2("Demo"),
        ContactsTable(await ContactsSlice.get(QueryParams(page=1))),
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
                hx_get=self.url_for(ContactsSlice).include_query_params(
                    page=self.attrs["page"] + 1
                ),
                hx_trigger="revealed",
                hx_swap="afterend",
            ),
        )


class ContactsTable(Component[ContactsSlice, Attrs]):
    @override
    def render(self) -> Table[TableHead, ContactsSlice]:
        return Table(
            TableHead("ID", "Name", "Email"),
            *self.children,
            classes=["text-align-center"],
        )
