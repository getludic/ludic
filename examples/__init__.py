from dataclasses import asdict, dataclass
from typing import Any, override

from ludic.attrs import NoAttrs
from ludic.catalog.layouts import Center, Stack
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.html import meta
from ludic.types import (
    AnyChildren,
    Component,
)


@dataclass
class Model:
    def dict(self) -> dict[str, Any]:
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
class DB:
    contacts: dict[str, ContactData]
    people: dict[str, PersonData]


def init_db() -> DB:
    return DB(
        contacts={
            "1": ContactData(
                id="1",
                first_name="John",
                last_name="Doe",
                email="qN6Z8@example.com",
            )
        },
        people={
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
        },
    )


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
                Center(Stack(*self.children), style={"padding": self.theme.sizes.xxl}),
                htmx_version="1.9.10",
            ),
        )
