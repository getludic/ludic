from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from examples import (
    Page,
    bulk_update,
    click_to_edit,
    click_to_load,
    delete_row,
    edit_row,
    infinite_scroll,
    lazy_loading,
)

from ludic.catalog.headers import H1
from ludic.catalog.layouts import Box, NotSidebar, Sidebar, WithSidebar
from ludic.catalog.navigation import Navigation, NavItem
from ludic.catalog.typography import Link, Paragraph
from ludic.html import style
from ludic.web import LudicApp, Request
from ludic.web.routing import Mount


@asynccontextmanager
async def lifespan(_: LudicApp) -> AsyncIterator[None]:
    style.load(cache=True)
    yield


app = LudicApp(
    debug=True,
    lifespan=lifespan,
    routes=[
        Mount("/bulk-update/", bulk_update.app, name="bulk_update"),
        Mount("/click-to-edit/", click_to_edit.app, name="click_to_edit"),
        Mount("/click-to-load/", click_to_load.app, name="click_to_load"),
        Mount("/delete-row/", delete_row.app, name="delete_row"),
        Mount("/edit-row/", edit_row.app, name="edit_row"),
        Mount("/infinite-scroll/", infinite_scroll.app, name="infinite_scroll"),
        Mount("/lazy-loading/", lazy_loading.app, name="lazy_loading"),
    ],
)


@app.get("/")
async def homepage(request: Request) -> Page:
    return Page(
        WithSidebar(
            Sidebar(
                Box(
                    Navigation(
                        NavItem("Bulk Update", to=request.url_for("bulk_update:index")),
                        NavItem(
                            "Click to Edit", to=request.url_for("click_to_edit:index")
                        ),
                        NavItem(
                            "Click to Load", to=request.url_for("click_to_load:index")
                        ),
                        NavItem("Delete Row", to=request.url_for("delete_row:index")),
                        NavItem("Edit Row", to=request.url_for("edit_row:index")),
                        NavItem(
                            "Infinite Scroll",
                            to=request.url_for("infinite_scroll:index"),
                        ),
                        NavItem(
                            "Lazy Loading", to=request.url_for("lazy_loading:index")
                        ),
                    )
                )
            ),
            NotSidebar(
                H1("Ludic Examples"),
                Paragraph(
                    "Here are examples demonstrating how to use the framework "
                    f"together with {Link("htmx.org", to="https://htmx.org")}."
                ),
            ),
        )
    )


@app.exception_handler(404)
async def not_found() -> Page:
    return Page(
        H1("Page Not Found"),
        Paragraph("The page you are looking for was not found."),
    )


@app.exception_handler(500)
async def server_error() -> Page:
    return Page(
        H1("Server Error"),
        Paragraph("Server encountered an error during processing."),
    )
