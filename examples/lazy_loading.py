import asyncio

from examples import Body, Header, Page

from ludic.catalog.loaders import LazyLoader
from ludic.catalog.quotes import Quote
from ludic.html import div, svg
from ludic.types import Safe
from ludic.web import LudicApp, Request

app = LudicApp(debug=True)


@app.get("/")
async def index(request: Request) -> Page:
    return Page(
        Header("Lazy Loading"),
        Body(
            Quote(
                "This example shows how to lazily load an element on a page.",
                source_url="https://htmx.org/examples/lazy-load/",
            ),
            div(
                LazyLoader(load_url=request.url_for(load_svg, seconds=3)),
                style={"text-align": "center"},
            ),
        ),
    )


@app.get("/load/{seconds:int}")
async def load_svg(seconds: int) -> svg:
    await asyncio.sleep(seconds)
    return svg(
        Safe(
            '<rect width="100%" height="100%" fill="#eee" />\n'
            '<text x="350" y="225" font-size="60" text-anchor="middle" fill="#555">'
            "Content Loaded"
            "</text>"
        ),
        version="1.1",
        width="700",
        height="400",
    )
