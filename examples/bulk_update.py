from typing import Annotated, Self

from examples import Body, Header, Page, app, db
from ludic.catalog.buttons import ButtonPrimary
from ludic.catalog.forms import FieldMeta, Form
from ludic.catalog.tables import ColumnMeta, Table, create_rows
from ludic.css import CSSProperties
from ludic.html import span
from ludic.types import BaseAttrs
from ludic.web.endpoints import Endpoint
from ludic.web.parsers import ListParser


class PersonAttrs(BaseAttrs, total=False):
    id: Annotated[str, ColumnMeta(identifier=True)]
    name: Annotated[str, ColumnMeta()]
    email: Annotated[str, ColumnMeta()]
    active: Annotated[
        bool,
        ColumnMeta(kind=FieldMeta(kind="checkbox", label=None)),
    ]


class PeopleTableAttrs(BaseAttrs):
    people: list[PersonAttrs]


@app.get("/")
async def index() -> Page:
    return Page(
        Header("Bulk Update"),
        Body(await PeopleTable.get()),
    )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleTableAttrs]):
    styles: dict[str, CSSProperties] = {
        "toast": {"margin": "10px 20px", "background": "#E1F0DA"}
    }

    @classmethod
    async def post(cls, data: ListParser[PersonAttrs]) -> span:
        items = {row["id"]: row for row in data.validate()}
        activations = {True: 0, False: 0}

        for person in db.people.values():
            active = items.get(person.id, {}).get("active", False)
            if person.active != active:
                person.active = active
                activations[active] += 1

        return span(
            f"Activated {activations[True]}, deactivated {activations[False]}",
            id="toast",
            style=cls.styles["toast"],
        )

    @classmethod
    async def get(cls) -> Self:
        return cls(people=[person.dict() for person in db.people.values()])

    def render(self) -> Form:
        return Form(
            Table(*create_rows(self.attrs["people"], spec=PersonAttrs)),
            ButtonPrimary("Bulk Update", type="submit"),
            span(
                id="toast",
                style=self.styles["toast"],
            ),
            hx_post=self.url_for(PeopleTable),
            hx_target="#toast",
            hx_swap="outerHTML settle:3s",
        )
