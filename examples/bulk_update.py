from typing import Annotated, Self, override

from examples import Body, Header, Page, app, init_db
from ludic.catalog.buttons import ButtonPrimary
from ludic.catalog.forms import FieldMeta, Form
from ludic.catalog.tables import ColumnMeta, Table, create_rows
from ludic.html import span
from ludic.types import Attrs
from ludic.web.endpoints import Endpoint
from ludic.web.parsers import ListParser

db = init_db()


class PersonAttrs(Attrs, total=False):
    id: Annotated[str, ColumnMeta(identifier=True)]
    name: Annotated[str, ColumnMeta()]
    email: Annotated[str, ColumnMeta()]
    active: Annotated[
        bool,
        ColumnMeta(kind=FieldMeta(kind="checkbox", label=None)),
    ]


class PeopleAttrs(Attrs):
    people: list[PersonAttrs]


class Toast(span):
    id: str = "toast"
    target: str = f"#{id}"
    styles = {
        target: {
            "background": "#E1F0DA",
            "margin": "10px 20px",
            "opacity": "0",
            "transition": "opacity 3s ease-out",
        },
        f"{target}.htmx-settling": {
            "opacity": "100",
        },
    }

    @override
    def render(self) -> span:
        return span(*self.children, id=self.id)


@app.get("/")
async def index() -> Page:
    return Page(
        Header("Bulk Update"),
        Body(await PeopleTable.get()),
    )


@app.endpoint("/people/")
class PeopleTable(Endpoint[PeopleAttrs]):
    @classmethod
    async def post(cls, data: ListParser[PersonAttrs]) -> Toast:
        items = {row["id"]: row for row in data.validate()}
        activations = {True: 0, False: 0}

        for person in db.people.values():
            active = items.get(person.id, {}).get("active", False)
            if person.active != active:
                person.active = active
                activations[active] += 1

        return Toast(f"Activated {activations[True]}, deactivated {activations[False]}")

    @classmethod
    async def get(cls) -> Self:
        return cls(people=[person.dict() for person in db.people.values()])

    @override
    def render(self) -> Form:
        return Form(
            Table(*create_rows(self.attrs["people"], spec=PersonAttrs)),
            ButtonPrimary("Bulk Update", type="submit"),
            Toast(),
            hx_post=self.url_for(PeopleTable),
            hx_target=Toast.target,
            hx_swap="outerHTML settle:3s",
        )
