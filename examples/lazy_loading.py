import asyncio

from examples import Page

from ludic.catalog.headers import H1, H2, H3
from ludic.catalog.layouts import Box
from ludic.catalog.loaders import LazyLoader
from ludic.catalog.quotes import Quote
from ludic.web import LudicApp, Request

app = LudicApp(debug=True)


@app.get("/")
async def index(request: Request) -> Page:
    return Page(
        H1("Lazy Loading"),
        Quote(
            "This example shows how to lazily load an element on a page.",
            source_url="https://htmx.org/examples/lazy-load/",
        ),
        H2("Demo"),
        LazyLoader(load_url=request.url_for(load_svg, seconds=3)),
    )


@app.get("/load/{seconds:int}")
async def load_svg(seconds: int) -> Box:
    await asyncio.sleep(seconds)
    return Box(
        H3("Content Loaded!", classes=["text-align-center"]),
        classes=["invert"],
        style={"padding-top": "10rem", "padding-bottom": "10rem"},
    )
