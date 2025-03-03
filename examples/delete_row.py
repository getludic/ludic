from typing import Self, override

from examples import Page, init_db

from ludic.attrs import Attrs, GlobalAttrs
from ludic.catalog.buttons import ButtonDanger
from ludic.catalog.headers import H1, H2
from ludic.catalog.quotes import Quote
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.web import Endpoint, LudicApp
from ludic.web.exceptions import NotFoundError

db = init_db()
app = LudicApp(debug=True)


class PersonAttrs(Attrs):
    id: str
    name: str
    email: str
    active: bool


class PeopleAttrs(Attrs):
    people: list[PersonAttrs]


@app.get("/")
def index() -> Page:
    return Page(
        H1("Delete Row"),
        Quote(
            "This example shows how to implement a delete button that removes "
            "a table row upon completion.",
            source_url="https://htmx.org/examples/delete-row/",
        ),
        H2("Demo"),
        PeopleTable.get(),
    )


@app.endpoint("/people/{id}")
class PersonRow(Endpoint[PersonAttrs]):
    @classmethod
    def delete(cls, id: str) -> None:
        try:
            db.people.pop(id)
        except KeyError:
            raise NotFoundError("Person not found")

    @override
    def render(self) -> TableRow:
        return TableRow(
            self.attrs["name"],
            self.attrs["email"],
            "Active" if self.attrs["active"] else "Inactive",
            ButtonDanger(
                "Delete", hx_delete=self.url_for(PersonRow), classes=["small"]
            ),
        )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleAttrs]):
    styles = {
        "tr.htmx-swapping td": {
            "opacity": "0",
            "transition": "opacity 1s ease-out",
        }
    }

    @classmethod
    def get(cls) -> Self:
        return cls(people=[person.to_dict() for person in db.people.values()])

    @override
    def render(self) -> Table[TableHead, PersonRow]:
        return Table(
            TableHead("Name", "Email", "Active", ""),
            *(PersonRow(**person) for person in self.attrs["people"]),
            body_attrs=GlobalAttrs(
                hx_confirm="Are you sure?",
                hx_target="closest tr",
                hx_swap="outerHTML swap:1s",
            ),
            classes=["text-align-center"],
        )
