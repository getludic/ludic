from typing import Self

from examples import Body, Header, Page, app, db
from ludic.catalog.buttons import ButtonDanger
from ludic.catalog.tables import TableHead, TableRow
from ludic.html import table, tbody, thead
from ludic.types import BaseAttrs, GlobalStyles
from ludic.web.endpoints import Endpoint
from ludic.web.exceptions import NotFoundError


class PersonAttrs(BaseAttrs):
    id: str
    name: str
    email: str
    active: bool


class PeopleAttrs(BaseAttrs):
    people: list[PersonAttrs]


@app.get("/")
async def index() -> Page:
    return Page(
        Header("Delete Row"),
        Body(await PeopleTable.get()),
    )


@app.endpoint("/people/{id}")
class PersonRow(Endpoint[PersonAttrs]):
    @classmethod
    async def delete(cls, id: str) -> None:
        try:
            db.people.pop(id)
        except KeyError:
            raise NotFoundError("Person not found")

    def render(self) -> TableRow:
        return TableRow(
            self.attrs["name"],
            self.attrs["email"],
            "Active" if self.attrs["active"] else "Inactive",
            ButtonDanger("Delete", hx_delete=self.url_for(PersonRow)),
        )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleAttrs]):
    styles: GlobalStyles = {
        "tr.htmx-swapping td": {
            "opacity": "0",
            "transition": "opacity 1s ease-out",
        },
    }

    @classmethod
    async def get(cls) -> Self:
        return cls(people=[person.dict() for person in db.people.values()])

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
