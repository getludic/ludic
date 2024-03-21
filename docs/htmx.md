# Using HTMX with Ludic

[HTMX](https://htmx.org/) is a powerful library that simplifies the creation of dynamic, interactive web pages. It lets you achieve the responsiveness of single-page applications without the complexity of writing extensive JavaScript code. HTMX works by extending standard HTML with special attributes that control how elements interact with the server.

## HTMX Integration in Ludic

The `ludic.html` module seamlessly supports HTMX attributes, making it easy to add dynamic functionality to your pages. Let's see a simple example:

```python
from ludic.html import button

button("Click Me", hx_post="/clicked", hx_swap="outerHTML")
```

This code would generate the following HTML:

```html
<button hx-post="/clicked" hx-swap="outerHTML">
  Click Me
</button>
```

## Setting up an HTMX-Enabled Page

1. **Include the HTMX library:** Add the HTMX script to your base HTML component:

    ```python
    from ludic.html import html, head, body, style, title, main, script
    from ludic.types import AnyChildren, Component, NoAttrs


    class Page(Component[AnyChildren, NoAttrs]):
        @override
        def render(self) -> html:
            return html(
                head(
                    title("Example"),
                    style.load()
                ),
                body(
                    main(*self.children),
                    script(src="https://unpkg.com/htmx.org@latest"),
                ),
            )
    ```

2. **Use the `Page` component:** Employ the `Page` component as the foundation for your HTML documents to ensure they load the necessary HTMX script.

## A Practical Example

Let's illustrate how to create a dynamic page with HTMX and Ludic:

```python
from ludic.html import div, h1, p, button
from ludic.web import LudicApp, Request

from your_app.pages import Page

app = LudicApp()

@app.get("/")
def homepage(request: Request) -> Page:
    return Page(
        h1("Hello Stranger!"),
        p("This is a simple example with one button performing the hx-swap operation."),
        button("Show Content", hx_get=request.url_for(content), hx_swap="outerHTML"),
    )

@app.get("/content")
def content() -> div:
    return div(h2("Content"), p("This is the content."))
```

**Explanation:**

* **Button Behavior:** Clicking the button triggers an HTTP GET request to `/content`. The response replaces the original button with the content returned from the `/content` endpoint due to the `hx_swap="outerHTML"` attribute.
* **Web Framework:** Ludic acts as a web framework (built on [Starlette](https://www.starlette.io/responses/)), empowering you to define endpoints and handle requests. Explore the [Web Framework section](web-framework.md) of the documentation for in-depth information.

## Headers

It is possible to append custom HTMX headers in responses, here is an example:

```python
from ludic import types
from ludic.html import div

from your_app.server import app

@app.get("/")
def index() -> tuple[div, types.HXHeaders]:
    return div("Example"), {"HX-Location": {"path": "/", "target": "#test"}}
```

You can also type your endpoint with `tuple[div, types.Headers]` which allows arbitrary headers, not just HTMX-specific ones.

## Rendering JavaScript

In some cases, HTMX components require some JavaScript code. For that purpose, there is the `ludic.types.JavaScript` class:

```python
from ludic.html import button, div, h2, table
from ludic.types import JavaScript

from your_app.server import app

@app.get("/data")
def data() -> div:
    return div(
        h2("Data"),
        table(...),
        button("Click Here", onclick=JavaScript("alert('test')")),
    )
```
