# CSS Styling Options

There are three primary ways to apply CSS properties to components within your application:

1. The `style` HTML Attribute
2. The `styles` Class Property
3. The `style` HTML Element

Apart from these options of adding CSS, you can further use **Themes** to customize the look and feel of your application. More about that later.

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

You can also specify a color of a theme:

```python
form(..., style={"background-color": theme.colors.white})
```

## The `styles` Class Property

Define CSS properties within your component using the `styles` class property. Example:

```python
from typing import override

from ludic.attrs import ButtonAttrs
from ludic.html import button
from ludic.types import ComponentStrict


class Button(ComponentStrict[str, ButtonAttrs]):
    classes = ["btn"]
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
    classes = ["btn"]
    styles = {
        "button.btn": {
            "color": "#eee",  # type: ignore[dict-item]
            ".icon": {
                "font-size": "16px",
            }
        }
    }
    ...
```

You can access the `theme` to specify properties like this:

```python
from ludic.html import style


class Button(ComponentStrict[str, ButtonAttrs]):
    classes = ["btn"]
    styles = style.use(lambda theme:{
        "button.btn": {
            "color": theme.colors.primary,
        }
    })
    ...
```

Note that the `classes` attribute contains the list of classes that will be applied to the component when rendered (they will be appended if there are any other classes specified by the `class_` attribute).

### Collecting The Styles

1. **Load Styles**: Use the `style.load()` method to gather styles from all components in your project. This generates a `<style>` element:

    ```python
    from ludic.html import style

    styles = style.load()
    ```

    The `styles` variable now renders as a `<style>` element with the content similar to this:

    ```html
    <style>
      button.btn { background-color: #fab; font-size: 16px; }
    </style>
    ```

    You can also pass `styles.load(cache=True)` to cache the styles.

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

## How to Style Components Using Themes

Themes provide a centralized way to manage the look and feel of your components. You can directly access a component's theme to customize its styling based on your theme's settings. Here's a breakdown of how this works:

### Explanation

* **Theme Definition:** A theme holds predefined styles like colors, fonts, and spacing. You usually define your theme separately.
* **Accessing the Theme:** Components can access the current theme through a special ``theme`` attribute. This gives you direct access to your theme's values.
* **Switching Theme:** Components can switch to a different theme by passing the component to the ``theme.use()`` method. You can also switch theme globally.

### Theme Definition

You have two options how to create a new theme:

1. subclass `Theme` base class and define the theme's attributes
2. instantiate an existing theme and override its attributes

Here is an example of the first approach:

```python
from dataclasses import dataclass

from ludic.styles.themes import Colors, Color, Fonts, Theme


@dataclass
class LightTheme(Theme):
    """Light theme."""

    name: str = "light"

    fonts: Fonts = field(default_factory=Fonts)
    colors: Colors = field(
        default_factory=lambda: Colors(
            primary=Color("#c2e7fd"),
            secondary=Color("#fefefe"),
            success=Color("#c9ffad"),
            info=Color("#fff080"),
            warning=Color("#ffc280"),
            danger=Color("#ffaca1"),
            light=Color("#f8f8f8"),
            dark=Color("#414549"),
        )
    )
```

You can also instantiate an existing theme and override its attributes:

```python
from ludic.styles.themes import Fonts, FontSizes, Size, LightTheme

theme = LightTheme(fonts=Fonts(sizes=FontSizes(medium=Size(1, "em"))))
```

### Accessing The Theme

There are two ways to access the theme:

1. use the component's ``theme`` attribute
2. call `style.use(lambda theme: { ... })` on the component's `styles` class attribute

Here is an example combining both approaches:

```python
from typing import override

from ludic.html import button, style
from ludic.types import Component
from ludic.attrs import ButtonAttrs


class Button(Component[str, ButtonAttrs]):
    classes = ["btn"]
    styles = style.use(lambda theme: {
        "button.btn:hover": {
            "background-color": theme.colors.primary.lighten(0.2)
        }
    })

    @override
    def render(self) -> button:
        return button(
            self.children[0],
            style={
                "background-color": self.theme.colors.primary  # Use primary color from theme
            }
        )
```

### Switching Theme

You can switch the theme globally or for a specific component:

1. use the ``theme.use()`` method to switch theme in a component
2. use the ``set_default_theme()`` method to switch theme globally
3. use the ``style.load()`` to render styles from loaded components with a different theme

Here are some examples:

```python
from ludic.styles import DarkTheme, LightTheme, set_default_theme
from ludic.html import style, div, b, a
from ludic.types import Component
from ludic.attrs import GlobalAttrs

dark = DarkTheme()
light = LightTheme()

set_default_theme(light)

class MyComponent(Component[str, GlobalAttrs]):
    styles = style.use(
        # uses the theme specified by the `style.load(theme)` method
        # or the default theme if `style.load()` was called without a theme
        lambda theme: {
            "#c1 a": {"color": theme.colors.warning},
        }
    )

    @override
    def render(self) -> div:
        return div(
            dark.use(ButtonPrimary("Send")),  # uses the local theme (dark)
            ButtonSecondary("Cancel"),  # uses the global theme (light)
            style={"background-color": self.theme.colors.primary}  # uses the default theme (light)
        )

my_styles = style.load()  # loads styles form all components with the default theme (light)
my_styles = style.load(theme=dark)  # loads style with the specified theme (dark)
```
