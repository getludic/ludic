from typing import Annotated, Self, override

from examples import Body, Header, Page, init_db

from ludic.catalog.buttons import ButtonPrimary
from ludic.catalog.forms import FieldMeta, Form
from ludic.catalog.quotes import Quote
from ludic.catalog.tables import ColumnMeta, Table, create_rows
from ludic.html import span, style
from ludic.types import Attrs
from ludic.web import Endpoint, LudicApp
from ludic.web.parsers import ListParser

db = init_db()
app = LudicApp(debug=True)


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
    styles = style.use(
        lambda theme: {
            Toast.target: {
                "background": theme.colors.success,
                "margin": "10px 20px",
                "padding": "5px 8px",
                "border-radius": "3px",
                "opacity": "0",
                "transition": "opacity 3s ease-out",
            },
            f"{Toast.target}.htmx-settling": {
                "opacity": "100",
            },
        }
    )

    @override
    def render(self) -> span:
        return span(*self.children, id=self.id)


@app.get("/")
async def index() -> Page:
    return Page(
        Header("Bulk Update"),
        Body(
            Quote(
                "This demo shows how to implement a common pattern where rows are "
                "selected and then bulk updated.",
                source_url="https://htmx.org/examples/bulk-update/",
            ),
            await PeopleTable.get(),
        ),
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
