from dataclasses import asdict, dataclass
from typing import Any

from ludic.catalog.styles import ComponentsStyles
from ludic.catalog.typography import Paragraph
from ludic.html import (
    body,
    div,
    h1,
    head,
    header,
    html,
    main,
    meta,
    script,
    title,
)
from ludic.types import AnyChild, BaseAttrs, BaseElement, Component, PrimitiveChild
from ludic.web import LudicApp


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


db = DB(
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


class Page(Component[AnyChild, BaseAttrs]):
    def render(self) -> BaseElement:
        return html(
            head(
                title("Ludic Example"),
                ComponentsStyles(),
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            ),
            body(
                main(*self.children),
                script(src="https://unpkg.com/htmx.org@1.9.10"),
            ),
        )


class Header(Component[PrimitiveChild, BaseAttrs]):
    def render(self) -> header:
        return header(
            h1(f"Example - {self.children[0]}"),
        )


class Body(Component[AnyChild, BaseAttrs]):
    def render(self) -> div:
        return div(*self.children)


class NotFoundPage(Page):
    def render(self) -> Page:
        return Page(
            Header("Page Not Found"),
            Body(Paragraph("The page you are looking for was not found.")),
        )


class ServerErrorPage(Page):
    def render(self) -> Page:
        return Page(
            Header("Server Error"),
            Body(Paragraph("Server encountered an error during processing.")),
        )


app = LudicApp(debug=True)
