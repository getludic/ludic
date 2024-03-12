# HTMX Support

[HTMX](https://htmx.org/) is a library that allows you to create web pages with dynamic behavior, like those found in single-page applications, without having to write JavaScript. It's built on top of HTML, CSS, and JavaScript, and it enables you to enhance server-rendered HTML by adding client-side interactivity through simple attributes in your HTML markup.

All elements in the `ludic.html` module automatically support HTMX attributes. Here is an example:

```python
from ludic.html import button

button("Click Me", hx_post="/clicked", hx_swap="outerHTML")
```

This would render as:

```html
<button hx-post="/clicked" hx-swap="outerHTML">
  Click Me
</button>
```

## Creating HTMX Page

You need to add the CDN link for HTMX to all components. Fortunately, you can just create the Page component like this:

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

You should probably replace the link pinning a specific version of HTMX. Or you can download a copy and link the file path.

Now you can use the component everywhere you need to render a valid HTML document, like this:

```python
from ludic.html import div, h1, p, button

from your_app.pages import Page


page = Page(
    div(
        h1("Hello Stranger!"),
        p(
            "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. "
            "Maecenas fermentum, sem in pharetra pellentesque, velit turpis "
            "volutpat ante, in pharetra metus odio a lectus. Nullam sit amet "
            "magna in magna gravida vehicula. Vestibulum fermentum tortor id "
            "mi. Phasellus enim erat, vestibulum vel, aliquam a, posuere eu, "
            "velit."
        ),
        button("Load Content", hx_get="/content", hx_swap="outerHTML"),
        class_="container",
    )
)
```

## Headers

It is possible to return custom HTMX headers in responses, here is an example:

```python
from ludic import types
from ludic.html import div

@app.get("/")
def index() -> tuple[div, types.HXHeaders]:
    return div("Headers Example", id="test"), {"HX-Location": {"path": "/", "target": "#test"}}
```

You can also type your endpoint with `tuple[div, types.Headers]`, however, it allows arbitrary headers.

## Rendering JavaScript

In some cases, HTMX components require some JavaScript code. For that purpose, there is the `ludic.types.JavaScript` class:

```python
from ludic.catalog.buttons import ButtonPrimary
from ludic.types import JavaScript


ButtonPrimary(
    "Click Here",
    onclick=JavaScript("alert('test')")
)
```
