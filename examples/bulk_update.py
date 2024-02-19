from typing import Final, Self

from examples import Body, Header, Page, app
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.html import td, th
from ludic.types import BaseAttrs
from ludic.web.endpoints import Endpoint


class PersonAttrs(BaseAttrs):
    id: str
    name: str
    email: str
    active: bool


class PeopleAttrs(BaseAttrs):
    people: list[PersonAttrs]


people = {
    "1": PersonAttrs(
        id="1",
        name="Joe Smith",
        email="joe@smith.org",
        active=True,
    ),
    "2": PersonAttrs(
        id="2",
        name="Angie MacDowell",
        email="angie@macdowell.org",
        active=True,
    ),
    "3": PersonAttrs(
        id="3",
        name="Fuqua Tarkenton",
        email="fuqua@tarkenton.org",
        active=True,
    ),
    "4": PersonAttrs(
        id="2",
        name="Kim Yee",
        email="kim@yee.org",
        active=False,
    ),
}


@app.endpoint("/")
class Index(Endpoint):
    @classmethod
    async def get(cls) -> Self:
        return cls()

    def render(self) -> Page:
        return Page(
            Header("Bulk Update"),
            Body(People(people=list(people.values()))),
        )


@app.endpoint("/people/")
class People(Endpoint[PeopleAttrs]):
    COLUMNS: Final[tuple[str, ...]] = ("Name", "Email", "Active")

    @classmethod
    async def get(cls) -> Self:
        return cls(people=list(people.values()))

    def render(self) -> Table:
        return Table(
            TableHead(*map(th, self.COLUMNS)),
            *(
                TableRow(
                    *(td(person.get(column.lower(), "")) for column in self.COLUMNS)  # type: ignore
                )
                for person in self.attrs["people"]
            ),
        )
