from ludic.base import BaseAttrs, Component
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
from ludic.types import AnyChild, BaseElement, PrimitiveChild
from ludic.web import LudicApp


class Page(Component[AnyChild, BaseAttrs]):
    def render(self) -> BaseElement:
        return html(
            head(
                title("Ludic Example"),
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
