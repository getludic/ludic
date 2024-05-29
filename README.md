<p align="center">
    <img width="600px" src="./docs/assets/ludic.png" alt="ludic">
</p>

[![test](https://github.com/paveldedik/ludic/actions/workflows/test.yaml/badge.svg)](https://github.com/paveldedik/ludic/actions) [![codecov](https://codecov.io/gh/paveldedik/ludic/graph/badge.svg?token=BBDNJWHMGX)](https://codecov.io/gh/paveldedik/ludic) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) [![Documentation Status](https://readthedocs.org/projects/ludic/badge/?version=latest)](https://ludic.readthedocs.io/en/latest/?badge=latest)

**Documentation**: https://ludic.readthedocs.io/

Ludic is a lightweight framework for building HTML pages with a component approach similar to [React](https://react.dev/). It is built to be used together with [htmx.org](https://htmx.org/) so that developers don't need to write almost any JavaScript to create dynamic web services. Its potential can be leveraged together with its web framework which is a wrapper around the powerful [Starlette](https://www.starlette.io/) framework. It is built with the latest Python 3.12 features heavily incorporating typing.

> [!IMPORTANT]
> The framework is in a very early development/experimental stage. There are a lot of half-functioning features at the moment. Contributions are welcome to help out with the progress!

## Features

- Seamless **&lt;/&gt; htmx** integration for rapid web development in **pure Python**
- **Type-Guided components** utilizing Python's typing system
- Uses the power of **Starlette** and **Async** for high-performance web development
- Build HTML with the ease and power of Python **f-strings**
- Add CSS styling to your components with **Themes**
- Create simple, responsive layouts adopted from the **Every Layout Book**

## Comparison

Here is a table comparing Ludic to other similar tools:

| Feature                     | Ludic       | FastUI      | Reflex      |
|-----------------------------|-------------|-------------|-------------|
| HTML rendering              | Server Side | Client Side | Client Side |
| Uses a template engine      | No          | No          | No          |
| UI interactivity            | [</> htmx](https://htmx.org)* | [React](https://react.dev/) | [React](https://react.dev/) |
| Backend framework           | [Starlette](https://www.starlette.io)*  | [FastAPI](https://fastapi.tiangolo.com) | [FastAPI](https://fastapi.tiangolo.com) |
| Client-Server Communication | [HTML + REST](https://htmx.org/essays/how-did-rest-come-to-mean-the-opposite-of-rest/) | [JSON + REST](https://github.com/pydantic/FastUI?tab=readme-ov-file#the-principle-long-version) | [WebSockets](https://reflex.dev/blog/2024-03-21-reflex-architecture/) |

<sup>(*) HTMX as well as Starlette are optional dependencies for Ludic, it does not enforce any frontend or backend frameworks. At it's core, Ludic only generates HTML and allows registering CSS.</sup>

## Motivation

This framework allows HTML generation in Python while utilizing Python's typing system. Our goal is to enable the creation of dynamic web applications with reusable components, all while offering a greater level of type safety than raw HTML.

**Key Ideas:**

- **Type-Guided HTML**: Catch potential HTML structural errors at development time thanks to type hints. The framework enforces stricter rules than standard HTML, promoting well-structured and maintainable code.
- **Composable Components**: Define reusable, dynamic HTML components in pure Python. This aligns with modern web development practices, emphasizing modularity.

### Type-Guided HTML

Here is an example of how Python's type system can be leveraged to enforce HTML structure:

```python
br("Hello, World!")        # type error (<br> can't have children)
br()                       # ok

html(body(...))            # type error (first child must be a <head>)
html(head(...), body(...)) # ok

div("Test", href="test")   # type error (unknown attribute)
a("Test", href="...")      # ok
```

### Composable Components

Instead of using only basic HTML elements, it is possible to create modular components with the support of Python's type system. Let's take a look at an example:

```python
Table(
    TableHead("Id", "Name"),
    TableRow("1", "John"),
    TableRow("2", "Jane"),
    TableRow("3", "Bob"),
)
```

This structure can be type-checked thanks to Python's rich type system. Additionally, this `Table` component could have **dynamic properties** like sorting or filtering.

## Requirements

Python 3.12+

## Installation

```
pip install "ludic[full]"
```

Similar to Starlette, you'll also want to install an [ASGI](https://asgi.readthedocs.io/en/latest/) server:

```
pip install uvicorn
```

You can also use a basic cookiecutter template to get quickly started:

```
cookiecutter gh:paveldedik/ludic-template
```

## Full Example

**components.py**:

```python
from typing import override

from ludic.html import a
from ludic.types import Attrs, Component

class LinkAttrs(Attrs):
    to: str

class Link(Component[str, LinkAttrs]):
    classes = ["link"]

    @override
    def render(self) -> a:
        return a(
            *self.children,
            href=self.attrs["to"],
            style={"color": self.theme.colors.primary},
        )
```

Now you can use it like this:

```python
link = Link("Hello, World!", to="/home")
```

**web.py**:

```python
from ludic.web import LudicApp
from ludic.html import b, p

from .components import Link

app = LudicApp()

@app.get("/")
async def homepage() -> p:
    return p(f"Hello {b("Stranger")}! Click {Link("here", to="https://example.com")}!")
```

To run the application:

```python
uvicorn web:app
```

### More Examples

For more complex usage incorporating all capabilities of the framework, please visit the folder with examples [on GitHub](https://github.com/paveldedik/ludic/tree/master/examples/).

## Contributing

Any contributions to the framework are warmly welcome! Your help will make it a better resource for the community. If you're ready to contribute, read the [contribution guide](https://github.com/paveldedik/ludic/tree/master/CONTRIBUTING.md).
