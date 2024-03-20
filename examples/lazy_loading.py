import asyncio

from examples import Body, Header, Loading, Page, app
from ludic.catalog.loading import LazyLoader
from ludic.html import div, svg
from ludic.types import Safe
from ludic.web import Request


@app.get("/")
async def homepage(request: Request) -> Page:
    return Page(
        Header("Lazy Loading"),
        Body(
            div(
                LazyLoader(
                    load_url=request.url_for(load_svg, seconds=3), placeholder=Loading()
                ),
                style={"text-align": "center"},
            )
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
