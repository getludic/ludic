from typing import Self, override

from examples import Page

from ludic.attrs import Attrs, NoAttrs
from ludic.catalog.forms import InputField
from ludic.catalog.headers import H1, H2
from ludic.catalog.quotes import Quote
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.catalog.typography import Paragraph
from ludic.components import Component
from ludic.html import div, style
from ludic.types import NoChildren
from ludic.web import Endpoint, LudicApp

app = LudicApp(debug=True)


class ContactAttrs(Attrs):
    first_name: str
    last_name: str
    email: str


class SearchAttrs(Attrs):
    contacts: list[ContactAttrs]


def load_contacts() -> list[ContactAttrs]:
    first_names = ["Joe", "Angie", "Fuqua", "Kim", "John", "Jane", "Emily", "Sarah"]
    last_names = ["Smith", "MacDowell", "Tarkenton", "Yee", "Doe", "Johnson", "Lee"]
    return [
        ContactAttrs(
            first_name=first,
            last_name=last,
            email=f"{first}.{last}@example.com".lower(),
        )
        for last in last_names
        for first in first_names
    ]


def search_contacts(query: str) -> list[ContactAttrs]:
    query = query.strip().lower()
    matches = [
        contact
        for contact in load_contacts()
        if not query
        or query in contact["first_name"].lower()
        or query in contact["last_name"].lower()
        or query in contact["email"].lower()
    ]
    return matches[:50]


class Spinner(Component[NoChildren, NoAttrs]):
    classes = ["spinner", "htmx-indicator"]
    styles = style.use(
        lambda theme: {
            ".spinner": {
                "display": "inline-block",
                "inline-size": theme.sizes.m,
                "block-size": theme.sizes.m,
                "margin-inline-start": theme.sizes.xs,
                "vertical-align": "middle",
                "border-width": theme.borders.normal,
                "border-style": "solid",
                "border-color": theme.colors.light.darken(3),
                "border-block-start-color": theme.colors.primary,
                "border-radius": "50%",
                "animation": "spinner-rotate 0.6s linear infinite",
            },
            "@keyframes spinner-rotate": {
                "100%": {"transform": "rotate(360deg)"},
            },
            "@media (prefers-reduced-motion: reduce)": {
                ".spinner": {"animation": "none"},
            },
        }
    )

    @override
    def render(self) -> div:
        return div()


@app.get("/")
async def index() -> Page:
    return Page(
        H1("Active Search"),
        Quote(
            "This example actively searches a contacts database as the user "
            "enters text.",
            source_url="https://htmx.org/examples/active-search/",
        ),
        H2("Demo"),
        InputField(
            label="Search Contacts",
            name="search",
            type="search",
            placeholder="Begin typing to search contacts...",
            autocomplete="off",
            hx_get=app.url_path_for("Search"),
            hx_trigger="input changed delay:300ms, search",
            hx_target="#search-results",
            hx_swap="outerHTML",
            hx_indicator=".spinner",
        ),
        Spinner(),
        await Search.get(),
    )


@app.endpoint("/search/")
class Search(Endpoint[SearchAttrs]):
    @classmethod
    async def get(cls, search: str | None = None) -> Self:
        return cls(contacts=search_contacts(search or ""))

    @override
    def render(self) -> div:
        if not self.attrs["contacts"]:
            return div(Paragraph("No matching contacts."), id="search-results")

        return div(
            Table[TableHead, TableRow](
                TableHead("First Name", "Last Name", "Email"),
                *(
                    TableRow(
                        contact["first_name"],
                        contact["last_name"],
                        contact["email"],
                    )
                    for contact in self.attrs["contacts"]
                ),
            ),
            id="search-results",
        )
