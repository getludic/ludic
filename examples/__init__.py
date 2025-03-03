import json
from dataclasses import asdict, dataclass
from typing import Any, Self, override

from ludic.attrs import NoAttrs
from ludic.catalog.layouts import Center, Stack
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.components import Component
from ludic.html import meta
from ludic.styles import set_default_theme, themes, types
from ludic.types import AnyChildren

set_default_theme(themes.LightTheme(measure=types.Size(90, "ch")))


@dataclass
class Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ContactData(Model):
    id: str
    first_name: str
    last_name: str
    email: str


@dataclass
class PersonData(Model):
    id: str
    name: str
    email: str
    active: bool = True


@dataclass
class CarData(Model):
    name: str
    models: list[str]


@dataclass
class DB(Model):
    contacts: dict[str, ContactData]
    people: dict[str, PersonData]
    cars: dict[str, CarData]

    def find_all_cars_names(self) -> list[str]:
        return [car.name for car in self.cars.values()]

    def find_first_car(self) -> CarData:
        return self.cars["1"]

    def find_car_by_name(self, name: str | None) -> CarData | None:
        for car in self.cars.values():
            if car.name.lower() == name:
                return car
        return None

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            contacts={k: ContactData(**v) for k, v in data.get("contacts", {}).items()},
            people={k: PersonData(**v) for k, v in data.get("people", {}).items()},
            cars={k: CarData(**v) for k, v in data.get("cars", {}).items()},
        )


def init_contacts() -> dict[str, ContactData]:
    return {
        "1": ContactData(
            id="1",
            first_name="John",
            last_name="Doe",
            email="qN6Z8@example.com",
        )
    }


def init_people() -> dict[str, PersonData]:
    return {
        "1": PersonData(
            id="1",
            name="Joe Smith",
            email="joe@smith.org",
            active=True,
        ),
        "2": PersonData(
            id="2",
            name="Angie MacDowell",
            email="angie@macdowell.org",
            active=True,
        ),
        "3": PersonData(
            id="3",
            name="Fuqua Tarkenton",
            email="fuqua@tarkenton.org",
            active=True,
        ),
        "4": PersonData(
            id="4",
            name="Kim Yee",
            email="kim@yee.org",
            active=False,
        ),
    }


def init_cars() -> dict[str, CarData]:
    return {
        "1": CarData(
            name="Audi",
            models=["A1", "A4", "A6"],
        ),
        "2": CarData(
            name="Toyota",
            models=["Landcruiser", "Tacoma", "Yaris"],
        ),
        "3": CarData(
            name="BMW",
            models=["325i", "325ix", "X5"],
        ),
    }


def init_db() -> DB:
    return DB(contacts=init_contacts(), people=init_people(), cars=init_cars())


class Page(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> HtmlPage:
        return HtmlPage(
            Head(
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                title="HTMX Examples",
            ),
            Body(
                Center(
                    Stack(*self.children, id="content"),
                    style={"padding": self.theme.sizes.xxl},
                ),
                htmx_version="2.0.2",
            ),
        )
