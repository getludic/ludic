# CSS Styling Options

There are two primary ways to apply CSS properties to components within your application:

1. The `style` HTML Attribute
2. The `styles` Class Property

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

2. **Targeted Loading**: For more control, use `style.from_components(...)` to load styles from specific components:

    ```python
    from ludic.html import style

    from your_app.components import Button, Form

    styles = style.from_components(Button, Form)
    ```

### Integration In a Page Component

Create a `Page` component responsible for rendering collected styles in the HTML `<head>`:

```python
from ludic.html import html, head, body, style, title, main, script
from ludic.types import AnyChildren, Component, NoAttrs


class Page(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> html:
        return html(
            head(
                style.load()
            ),
            body(
                ...
            ),
        )
```
