from typing import override

from examples import DB as Database
from examples import Page, init_db
from fastapi import Depends, FastAPI

from ludic.catalog.forms import Option, SelectField, SelectFieldAttrs
from ludic.catalog.headers import H1, H2
from ludic.catalog.layouts import Stack
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.messages import MessageInfo, Title
from ludic.catalog.quotes import Quote
from ludic.catalog.typography import Code
from ludic.components import Component
from ludic.contrib.fastapi import LudicRoute
from ludic.html import b
from ludic.web import Request
from ludic.web.exceptions import NotFoundError

app = FastAPI()
app.router.route_class = LudicRoute


class CarSelect(Component[str, SelectFieldAttrs]):
    """Ludic element representing car select."""

    @override
    def render(self) -> SelectField:
        return SelectField(
            *[Option(child, value=child.lower()) for child in self.children],
            label=self.attrs.pop("label", "Car Manufacturer"),
            name="manufacturer",
            **self.attrs,
        )


class CarModelsSelect(Component[str, SelectFieldAttrs]):
    """Ludic element representing car models select."""

    @override
    def render(self) -> SelectField:
        return SelectField(
            *[Option(child, value=child.lower()) for child in self.children],
            label=self.attrs.pop("label", "Car Model"),
            id="models",
            **self.attrs,
        )


@app.get("/")
async def index(request: Request) -> Page:
    return Page(
        H1("Cascading Select"),
        MessageInfo(
            Title("FastAPI Example"),
            f"This example uses {b("FastAPI")} as backend Web Framework.",
        ),
        Quote(
            f"In this example we show how to make the values in one {Code("select")} "
            f"depend on the value selected in another {Code("select")}.",
            source_url="https://htmx.org/examples/value-select/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for(cars)),
    )


@app.get("/cars/")
def cars(request: Request, db: Database = Depends(init_db)) -> Stack:
    return Stack(
        CarSelect(
            *db.find_all_cars_names(),
            hx_get=request.url_for(models),
            hx_target="#models",
        ),
        CarModelsSelect(*db.find_first_car().models),
    )


@app.get("/models/")
def models(
    manufacturer: str | None = None, db: Database = Depends(init_db)
) -> CarModelsSelect:
    if car := db.find_car_by_name(manufacturer):
        return CarModelsSelect(*car.models, label=None)  # type: ignore
    else:
        raise NotFoundError("Car could not be found")
