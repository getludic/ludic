from typing import Self, override

from examples import Body, Header, Page, app, init_db
from ludic.catalog.buttons import ButtonDanger
from ludic.catalog.tables import TableHead, TableRow
from ludic.html import table, tbody, thead
from ludic.types import Attrs
from ludic.web.endpoints import Endpoint
from ludic.web.exceptions import NotFoundError

db = init_db()


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
        Header("Delete Row"),
        Body(PeopleTable.get()),
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
            ButtonDanger("Delete", hx_delete=self.url_for(PersonRow)),
        )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleAttrs]):
    styles = {
        "tr.htmx-swapping td": {
            "opacity": "0",
            "transition": "opacity 1s ease-out",
        },
    }

    @classmethod
    def get(cls) -> Self:
        return cls(people=[person.dict() for person in db.people.values()])

    @override
    def render(self) -> table:
        return table(
            thead(TableHead("Name", "Email", "Active", "")),
            tbody(
                *(PersonRow(**person) for person in self.attrs["people"]),
                hx_confirm="Are you sure?",
                hx_target="closest tr",
                hx_swap="outerHTML swap:1s",
            ),
            style={"text-align": "center"},
        )
