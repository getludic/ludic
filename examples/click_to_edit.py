from typing import Annotated, NotRequired, Self

from examples import Body, Header, Page, app, db
from ludic.catalog.buttons import ButtonDanger, ButtonPrimary
from ludic.catalog.forms import FieldMeta, Form, create_fields
from ludic.catalog.lists import Pairs
from ludic.html import div
from ludic.types import BaseAttrs
from ludic.web.endpoints import Endpoint
from ludic.web.exceptions import NotFoundError
from ludic.web.parsers import Parser, ValidationError


def email_validator(email: str) -> str:
    if len(email.split("@")) != 2:
        raise ValidationError("Invalid email")
    return email


class ContactAttrs(BaseAttrs):
    id: NotRequired[str]
    first_name: Annotated[str, FieldMeta(label="First Name")]
    last_name: Annotated[str, FieldMeta(label="Last Name")]
    email: Annotated[
        str, FieldMeta(label="Email", type="email", parser=email_validator)
    ]


@app.endpoint("/")
class Index(Endpoint):
    @classmethod
    async def get(cls) -> Self:
        return cls()

    def render(self) -> Page:
        return Page(
            Header("Click To Edit"),
            Body(*(Contact(**contact.dict()) for contact in db.contacts.values())),
        )


@app.endpoint("/contacts/{id}")
class Contact(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        contact = db.contacts.get(id)
        if contact is None:
            raise NotFoundError("Contact not found")

        return cls(**contact.dict())

    @classmethod
    async def put(cls, id: str, attrs: Parser[ContactAttrs]) -> Self:
        contact = db.contacts.get(id)
        if contact is None:
            raise NotFoundError("Contact not found")

        for key, value in attrs.validate().items():
            setattr(contact, key, value)

        return await cls.get(id)

    def render(self) -> div:
        return div(
            Pairs(items=self.attrs.items()),
            ButtonPrimary(
                "Click To Edit",
                hx_get=self.url_for(ContactForm),
            ),
            hx_target="this",
            hx_swap="outerHTML",
        )


@app.endpoint("/contacts/{id}/form")
class ContactForm(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        contact = db.contacts.get(id)

        if contact is None:
            raise NotFoundError("Contact not found")

        return cls(**contact.dict())

    def render(self) -> Form:
        return Form(
            *create_fields(self.attrs, spec=ContactAttrs),
            ButtonPrimary("Submit"),
            ButtonDanger("Cancel", hx_get=self.url_for(Contact)),
            hx_put=self.url_for(Contact),
            hx_target="this",
        )
