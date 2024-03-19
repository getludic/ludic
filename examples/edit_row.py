from typing import Annotated, NotRequired, Self, override

from examples import Body, Header, Page, app, init_db
from ludic.catalog.buttons import ButtonPrimary, ButtonSecondary
from ludic.catalog.tables import ColumnMeta, TableHead, TableRow
from ludic.html import div, input, table, tbody, thead
from ludic.types import Attrs, JavaScript
from ludic.web.endpoints import Endpoint
from ludic.web.exceptions import NotFoundError
from ludic.web.parsers import Parser

db = init_db()


class PersonAttrs(Attrs):
    id: NotRequired[str]
    name: Annotated[str, ColumnMeta()]
    email: Annotated[str, ColumnMeta()]


class PeopleAttrs(Attrs):
    people: list[PersonAttrs]


@app.get("/")
async def index() -> Page:
    return Page(
        Header("Edit Row"),
        Body(await PeopleTable.get()),
    )


@app.endpoint("/people/{id}")
class PersonRow(Endpoint[PersonAttrs]):
    onclick_script: JavaScript = JavaScript(
        """
        let editing = document.querySelector('.editing')

        if (editing) {
            alert('You are already editing a row')
        } else {
            htmx.trigger(this, 'edit')
        }
        """
    )

    @classmethod
    async def put(cls, id: str, data: Parser[PersonAttrs]) -> Self:
        person = db.people.get(id)

        if person is None:
            raise NotFoundError("Person not found")

        for attr, value in data.validate().items():
            setattr(person, attr, value)

        return cls(**person.dict())

    @classmethod
    async def get(cls, id: str) -> Self:
        person = db.people.get(id)

        if person is None:
            raise NotFoundError("Person not found")

        return cls(**person.dict())

    @override
    def render(self) -> TableRow:
        return TableRow(
            self.attrs["name"],
            self.attrs["email"],
            ButtonPrimary(
                "Edit",
                hx_get=self.url_for(PersonForm),
                hx_trigger="edit",
                onclick=self.onclick_script,
            ),
        )


@app.endpoint("/people/{id}/form/")
class PersonForm(Endpoint[PersonAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        person = db.people.get(id)

        if person is None:
            raise NotFoundError("Person not found")

        return cls(**person.dict())

    @override
    def render(self) -> TableRow:
        return TableRow(
            input(name="name", value=self.attrs["name"]),
            input(name="email", value=self.attrs["email"]),
            div(
                ButtonSecondary("Cancel", hx_get=self.url_for(PersonRow)),
                ButtonPrimary(
                    "Save",
                    hx_put=self.url_for(PersonRow),
                    hx_include="closest tr",
                ),
            ),
            class_="editing",
        )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleAttrs]):
    @classmethod
    async def get(cls) -> Self:
        return cls(people=[person.dict() for person in db.people.values()])

    @override
    def render(self) -> table:
        return table(
            thead(TableHead("Name", "Email", "Action")),
            tbody(
                *(PersonRow(**person) for person in self.attrs["people"]),
                hx_target="closest tr",
                hx_swap="outerHTML",
            ),
            style={"text-align": "center"},
        )
