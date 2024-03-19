# CSS Styling Options

There are two primary ways to apply CSS properties to components within your application:

1. The `style` HTML Attribute
3. The `styles` Class Property

## The `style` HTML Attribute

You can directly embed styles within an HTML element using the `style` attribute. Here's an example:

```python
from ludic.css import CSSProperties
from ludic.html import form

form(..., style=CSSProperties(color="#fff"))
```

- The `CSSProperties` class is a `TypedDict` for convenience since type checkers can highlight unknown or incorrect usage.
- You can also use a regular Python dictionary, which might be better in most cases since CSS properties often contain hyphens:

```python
form(..., style={"background-color": "#fff"})
```

## The `styles` Class Property

Define CSS properties within your component using the `styles` class property. Example:

```python
from typing import override

from ludic.attrs import ButtonAttrs
from ludic.html import button
from ludic.types import ComponentStrict


class Button(ComponentStrict[str, ButtonAttrs]):
    styles = {
        "button.btn": {
            "background-color": "#fab",
            "font-size": "16px",
        }
    }

    @override
    def render(self) -> button:
        return button(self.children[0], **self.attrs_for(button))
```

In this case, you need to make sure you collect and render the styles. See [Collecting The Styles](#collecting-the-styles) and [Integration In a Page Component](#integration-in-a-page-component).

It is also possible to nest styles similar to how you would nest them in SCSS. The only problem is that you might get typing errors if you are using `mypy` or `pyright`:

```python
class Button(ComponentStrict[str, ButtonAttrs]):
    styles = {
        "p": {
            "color": "#eee",  # type: ignore[dict-item]
            ".big": {
                "font-size": "16px",
            }
        }
    }
    ...
```

### Collecting The Styles

1. **Load Styles**: Use the `style.load()` method to gather styles from all components in your project. This generates a `<style>` element:

    ```python
    from ludic.html import style

    styles = style.load()
    ```

    The `styles` variable now contains renders the following element:

    ```html
    <style>
    button.btn { background-color: #fab; font-size: 16px; }
    </style>
    ```

    You can also pass `styles.load(cache=True)` in order to cache the styles.

2. **Targeted Loading**: For more control, use `style.from_components(...)` to load styles from specific components:

    ```python
    from ludic.html import style

    from your_app.components import Button, Form

    styles = style.from_components(Button, Form)
    ```

### Integration In a Page Component

Create a `Page` component responsible for rendering collected styles in the HTML `<head>`:

```python
from typing import override

from ludic.html import html, head, body, style
from ludic.types import AnyChildren, Component, NoAttrs


class Page(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> html:
        return html(
            head(
                style.load(cache=True)
            ),
            body(
                ...
            ),
        )
```

### Caching The Styles

As mentioned before, passing `cache=True` to `style.load` caches loaded elements' styles during the first render. The problem is that the first request to your application renders the styles without the cache, so the response is a bit slower. If you want to cache the styles before your component even renders for the first time, you can use the `lifespan` argument of the `LudicApp` class:

```python
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from ludic.web import LudicApp


@asynccontextmanager
async def lifespan(_: LudicApp) -> AsyncIterator[None]:
    style.load(cache=True)  # cache styles before accepting requests
    yield


app = LudicApp(lifespan=lifespan)
```

You can read more about `Lifespan` in [Starlette's documentation](https://www.starlette.io/lifespan/).

## The `style` HTML Element

You can also directly embed styles within a `Page` component using the `style` element. Here's an example:

```python
from ludic.html import style

style(
    {
        "a": {
            "text-decoration": "none",
            "color": "red",
        },
        "a:hover": {
            "color": "blue",
            "text-decoration": "underline",
        },
    }
)
```

It is also possible to pass raw CSS styles as a string:

```python
from ludic.html import style

style("""
.button {
    padding: 3px 10px;
    font-size: 12px;
    border-radius: 3px;
    border: 1px solid #e1e4e8;
}
""")
```
