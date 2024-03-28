from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass
from typing import Any, override

from ludic.attrs import NoAttrs
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
    style,
    title,
)
from ludic.types import (
    AnyChildren,
    BaseElement,
    Component,
    ComponentStrict,
    PrimitiveChildren,
)
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
    styles = {
        "body": {
            "display": "flex",
            "flex-direction": "column",
            "align-items": "center",
            "min-height": "100vh",
            "margin": "0",
            "font-family": "'Arial', sans-serif",
        },
        "main": {
            "width": "80%",
            "max-width": "800px",
            "padding": "20px",
        },
    }

    @override
    def render(self) -> BaseElement:
        return html(
            head(
                title("Ludic Example"),
                style.load(cache=True),
                meta(charset="utf-8"),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            ),
            body(
                main(*self.children),
                script(src="https://unpkg.com/htmx.org@1.9.10"),
            ),
        )


class Header(ComponentStrict[PrimitiveChildren, NoAttrs]):
    styles = style.use(
        lambda theme: {
            "header": {
                "text-align": "center",
            },
            "header h1": {
                "font-size": "3.5em",
                "line-height": "1.2",
                "margin-bottom": "35px",
                "font-family": theme.fonts.families.headers,
            },
        }
    )

    @override
    def render(self) -> header:
        return header(
            h1(f"Example - {self.children[0]}"),
        )


class Body(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> div:
        return div(*self.children)


@asynccontextmanager
async def lifespan(_: LudicApp) -> AsyncIterator[None]:
    style.load(cache=True)
    yield


app = LudicApp(debug=True, lifespan=lifespan)


@app.exception_handler(404)
async def not_found() -> Page:
    return Page(
        Header("Page Not Found"),
        Body(Paragraph("The page you are looking for was not found.")),
    )


@app.exception_handler(500)
async def server_error() -> Page:
    return Page(
        Header("Server Error"),
        Body(Paragraph("Server encountered an error during processing.")),
    )
