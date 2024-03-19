# Getting Started

To show an example how to get started with writing apps using Ludic Framework, here is a bit of an opinionated article where we create almost ready to run web app.

First let's say we create a small app with a file structure somewhat similar to this:

```
your_app
   ├── __init__.py
   ├── components
   │       ├── __init__.py
   │       ├── pages.py
   │       └── ...
   ├── attrs.py
   ├── endpoints.py
   ├── models.py
   ├── server.py
   └── ...
```

For bigger applications, this structure can look completely differently. If you are just getting started, this is a good starting point.

Now we explain what each module represents.

## `pages.py`

The idea is to write a couple of pages (regular components) rendering as a valid HTML document - using the `<html>` root tag.

Here is a sample `Page` component which represents the base for all other pages:

```python
from typing import override

from ludic.html import head, title, style, body, html, main, script
from ludic.types import AnyChildren, Component, NoAttrs


class Page(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> html:
        return html(
            head(
                title("Ludic Example"),
                style.load(cache=True),
            ),
            body(
                main(*self.children),
                script(src="https://unpkg.com/htmx.org@1.9.10"),
            ),
        )
```

Notice the `script` element loading the htmx library.

You probably want to modify this page to include other stuff like fonts, favicon and so on. Now you might create a `Header` and `Body` components and use it like this:

```python
Page(
    Header("Welcome to My App"),
    Body("Lorem ipsum ..."),
)
```

This would render as a valid HTML document.

## `server.py`

The module instantiates the `LudicApp` class and registers routes (by importing the endpoints module). You can also register error handlers. Here is what it can look like:

```python
from ludic.web import LudicApp

from your_app.components import Body, Header
from your_app.components.pages import Page


app = LudicApp(debug=True)


@app.error_handler(404)
async def not_found():
    return Page(
        Header("Not Found"),
        Body("Page you are looking for could not be found"),
    )


from . import endpoints as _  # noqa
```

## `endpoints.py`

Implement all your endpoints in this module:

```python
from typing import Self

from ludic.html import b
from ludic.web import LudicApp, Endpoint
from ludic.web.exceptions import NotFoundError

from .attrs import ContactAttrs
from .models import Contact
from .components import Body, Header, Data, Form
from .components.pages import Page

app = LudicApp(debug=True)


@app.get("/")
async def homepage():
    return Page(
        Header(f"Welcome to {b("My App")}"),
        Body("Lorem ipsum ..."),
    )


@app.endpoint("/contacts/{id}")
class Contact(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        contact = Contact.objects.get(id)

        if contact is None:
            raise NotFoundError("Contact not found")

        return cls(**contact.as_dict())

    @classmethod
    async def delete(cls, id: str) -> None:
        Contact.objects.delete(id)
        return None

    @override
    def render(self) -> Data:
        return Data(...)


@app.endpoint("/contacts/{id}/form/")
class ContactForm(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        contact = Contact.objects.get(id)

        if contact is None:
            raise NotFoundError("Contact not found")

        return cls(**contact.dict())

    @override
    def render(self) -> Form:
        return Form(...)
```

You can create any components you like and combine them in the `render()` method to produce an HTML representation of an entity.

## `attrs.py`

This module can be used to define attributes for your endpoints. Note that it is probably better to keep regular component's attributes close to them, so this module serves for definition of endpoint's attribute only:

```python
from typing import NotRequired

from ludic.types import Attrs


class ContactAttrs(Attrs):
    id: str
    name: str
    is_active: NotRequired[bool]
```

## What Next?

Now you are almost ready to run the up with `uvicorn`:

```
uvicorn your_app.server:app
```

In the next sections of this documentation, you can learn more about how to write components, endpoints, and what kind of other tools there are.
