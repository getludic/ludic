---
name: ludic-components
description: >-
  Build typed, React-like HTML components in Python with Ludic — uses PEP 750
  t-strings (Python 3.14+) and pairs with htmx. Use this skill whenever the
  user is writing or modifying Ludic component code: subclassing Component or
  ComponentStrict, declaring Attrs TypedDicts, composing HTML elements from
  ludic.html (div, a, html, head, body, table, form, ...), mixing markup with
  interpolation via t"...", reaching for catalog widgets (Table, PageLayout,
  Form, Button, Navigation), wiring htmx attributes (hx_get, hx_post,
  hx_target, hx_swap) on elements, defining Themes or CSS styles on
  components, or anything involving the trusted-vs-untrusted (Safe) content
  boundary. Also trigger on questions about why mypy is flagging a
  component's children/attrs. Prefer this skill even when the user does not
  explicitly say "Ludic" — the import `from ludic ...` or any usage of
  t-strings to build HTML is a strong signal. For building endpoints,
  request handling, FastAPI/Django integration, or URL generation, use the
  companion `ludic-web` skill instead.
metadata:
  type: framework-guide
  framework: ludic
  version: "1.x"
---

# Ludic Components

Ludic is a Python framework for building HTML pages with a typed, React-like component model that pairs with htmx. v1.x targets **Python 3.14+** and uses **PEP 750 t-strings** (template strings) for templating.

This skill helps you write idiomatic Ludic components: well-composed, type-safe under mypy (with the Ludic mypy plugin), safe by default, and legible. For wiring components into a web app (endpoints, request handling, URL generation, framework integrations), use the companion `ludic-web` skill.

## Check the Ludic version first

Look at the project's dependencies (`pyproject.toml`, the lock file) before writing code:

- **Ludic 1.x** (Python 3.14+): text mixed with elements is a t-string, `t"..."`. Everything in this skill is written for 1.x.
- **Ludic 0.5.x** (Python 3.12 and 3.13): t-strings do not exist yet, so the same code uses f-strings, `p(f"Hello {b('World')}!")`. Ludic 0.5 renders the elements inside these f-strings correctly. The rest of the API is the same, apart from features added in 1.x.

## Mental model

Three layers, top to bottom:

1. **HTML elements** in `ludic.html` (`div`, `a`, `html`, `head`, `body`, `table`, `form`, ...). Each element has a typed signature describing its allowed children and attributes (e.g. `br()` accepts no children; `html(...)` requires `head` as the first child, `body` as the second).
2. **Components** in `ludic.components` — `Component[TChildren, TAttrs]` and the variadic `ComponentStrict[*TChildrenArgs, TAttrs]`. You subclass these and implement `render()`, which returns an element tree. Components are the unit of reuse and can carry CSS via class-level `classes` and `styles` declarations and read the current `Theme` via `self.theme`.
3. **Catalog** in `ludic.catalog` — opinionated widgets built on top of the core: layouts (`PageLayout`, `Stack`, `Cluster`, `Sidebar`), forms (`Form`, `FormField`), tables (`Table`, `TableHead`, `TableRow`), navigation, typography, buttons, messages, etc. Reach for these before composing layouts out of raw `div`s — they encode sensible defaults.

The rendering pipeline runs once when you call `.to_html()`: it walks children, expands any t-string `Template` instances, escapes untrusted text, formats attributes (aliases like `class_` → `class`, dict-style `style={...}`, list-style `classes=[...]`), and emits a single HTML string.

## The two things that surprise people

### 1. Use t-strings, not f-strings

In v1.x, code that mixes HTML elements with interpolated text uses **t-strings** (PEP 750), not f-strings:

```python
from ludic.html import b, div

# correct — v1.x
div(t"Hello {b('World')}!")

# wrong — f-strings eagerly stringify b(...), losing escaping and child-tracking
div(f"Hello {b('World')}!")
```

The `t"..."` literal produces a `Template` object that Ludic's element constructor detects and expands. If you see `f"... {some_element} ..."` mixing HTML elements with text, change it to `t"..."`.

### 2. The trusted/untrusted content boundary

Everything is HTML-escaped by default. To opt out — for content you've already verified is safe HTML — wrap it in `Safe`:

```python
from ludic.html import div
from ludic.types import Safe

div("Hello <b>World</b>").to_html()
# → '<div>Hello &lt;b&gt;World&lt;/b&gt;</div>'   (escaped — safe default)

div(Safe("Hello <b>World</b>")).to_html()
# → '<div>Hello <b>World</b></div>'              (raw — you take responsibility)
```

Only use `Safe` for content you control or have sanitized. **Never wrap user input in `Safe`** — that's the XSS hole this whole system exists to prevent. There's also `JavaScript(Safe)` for inline JS bodies.

Ludic also speaks the `__html__` protocol used by MarkupSafe, Jinja2 and Django, in both directions:

- A child that implements `__html__` (`markupsafe.Markup`, Django's `mark_safe(...)` result) is trusted like `Safe` and written as it is. This applies to children only; attribute values are escaped unless they are `Safe`.
- Every element and `Safe` string implements `__html__`, so `{{ component }}` in a Jinja2 or Django template renders the markup instead of escaping it.

Elements also implement `_repr_html_`, so a notebook cell that ends with an element displays the rendered HTML.

## Writing a component

Two component classes:

- `Component[TChildren, TAttrs]` — accepts a variable number of children all of one type, plus a single `TAttrs` TypedDict for attributes.
- `ComponentStrict[*TChildrenArgs, TAttrs]` — uses a `TypeVarTuple` to enforce an exact positional sequence of child types (e.g. "exactly one `TableHead` followed by zero-or-more `TableRow`").

Use `ComponentStrict` when the shape of children matters structurally; use `Component` when children are a homogeneous list.

```python
from typing import override
from ludic import Attrs, Component
from ludic.html import a

class LinkAttrs(Attrs):
    to: str

class Link(Component[str, LinkAttrs]):
    classes = ["link"]                      # CSS classes added to the rendered root
    styles = {"a.link": {"color": "blue"}}  # collected by the style system

    @override
    def render(self) -> a:
        return a(
            *self.children,
            href=self.attrs["to"],
            style={"color": self.theme.colors.primary},
        )
```

To render several elements without a wrapping element, return `Blank(...)` from `render()`. It renders only its children and escapes text like any other element.

A few rules the Ludic mypy plugin enforces — make sure your app's `pyproject.toml` (or `mypy.ini`) has `plugins = ["ludic.mypy_plugin"]`, otherwise mypy does not check the attributes passed to components (see [Check your work](#check-your-work)):

- The generic parameters on `Component[...]` / `ComponentStrict[...]` synthesize `__init__`, so call sites get checked against `TChildren` and `TAttrs`.
- `Attrs` (and the per-element TypedDicts in `ludic.attrs`) describe **allowed** attributes. Unknown attributes are a type error.
- For HTML attribute names that collide with Python keywords or contain dashes, use the Python-side alias: `class_` → `class`, `for_` → `for`, `hx_get` → `hx-get`, etc. The `style=` attribute accepts a dict; `classes=` accepts a list.

## htmx attributes on elements

htmx attributes are exposed as `hx_*` keyword arguments on every element with `GlobalAttrs`:

```python
from ludic.html import button

button(
    "Load more",
    hx_get="/items?page=2",
    hx_target="#items",
    hx_swap="beforeend",
)
```

When you serve the rendered HTML from an endpoint, htmx swaps it into the page. The endpoint side is covered in the `ludic-web` skill — including how to generate the URLs you pass to `hx_get` / `hx_post` safely.

## Catalog: prefer it to raw HTML

Before composing a layout out of `div`s, check `ludic.catalog`:

- `catalog.pages` — `HtmlPage`, `Head`, `Body`: a whole HTML document with the collected CSS and, optionally, the htmx script (`Body(..., htmx_version="2.0.4")`). `Head(dark_theme=...)` and `ColorSchemeToggle` add a dark mode (see [Theming and styles](#theming-and-styles)).
- `catalog.layouts` — `Stack`, `Box`, `Center`, `Cluster`, `Sidebar`, `WithSidebar`, `Switcher`, `Cover`, `Grid`, `Frame` (adapted from *Every Layout*).
- `catalog.forms` — `Form`, `FormField`, `InputField`, `TextAreaField`, `SelectField` with `Option`, `ChoiceField`, and `create_fields` with `FieldMeta`, which builds form fields from an `Attrs` TypedDict.
- `catalog.tables` — `Table`, `TableHead`, `TableRow`.
- `catalog.navigation` — `Navigation` with `NavItem` for a menu, `NavBar` for a sticky bar at the top of the page, and `TableOfContents(*page_elements)`, which links to the `H2` headings among the elements.
- `catalog.tabs` — `Tabs` with `Tab(content, label="...")`, which switch without JavaScript.
- `catalog.cards` — `Card`, a framed box for short content; put cards in a `Grid` for responsive columns, and pass `to="/url"` to make a card a link.
- `catalog.typography` — `Paragraph`, `Link`, `Code`, and `CodeBlock`, which takes `language=`, a `label=` such as a file name, and `copy_button=True`.
- `catalog.buttons`, `catalog.messages`, `catalog.loaders`, `catalog.headers`, `catalog.items`, `catalog.lists`, `catalog.quotes`, `catalog.icons`.

These are also the best place to learn idiomatic Ludic — they exercise the full surface area of the framework.

## Theming and styles

`Component` subclasses can declare:

- `classes: list[str]` — appended to the root element's class list at render time.
- `styles: GlobalStyles` — collected at startup so you can emit a single `<style>` block for the page.

Read the active theme via `self.theme` (returns the default theme if none is in scope). Themes flow down the tree automatically, so children see the same theme as the parent rendering them.

For a dark mode, give `Head` a second theme. The page then follows the system setting, and `ColorSchemeToggle` lets the visitor switch and remembers the choice:

```python
from ludic.catalog.pages import Body, ColorSchemeToggle, Head, HtmlPage
from ludic.catalog.typography import Paragraph
from ludic.styles.themes import DarkTheme, LightTheme

page = HtmlPage(
    Head(title="My App", theme=LightTheme(), dark_theme=DarkTheme()),
    Body(ColorSchemeToggle(), Paragraph("Hello!"), htmx_version="2.0.4"),
)
assert 'media="(prefers-color-scheme: dark)"' in page.to_html()
```

Both themes must have different names, because the styles are cached per theme name. Put colors in `styles` rather than in inline `style={...}` attributes, because inline styles do not switch with the theme.

To restyle catalog components, change the theme instead of writing CSS for them. Besides `colors`, `fonts` and `sizes`, a theme configures some components directly: `code=CodeBlock(...)` for code blocks, `buttons=Buttons(color=..., background_color=...)` for the default `Button` and `ButtonLink`, and `layouts=Layouts(...)` for the layouts. All of these classes are in `ludic.styles.themes`.

## A complete worked example

```python
from typing import override
from ludic import Attrs, Component
from ludic.catalog.layouts import Stack
from ludic.catalog.typography import Paragraph
from ludic.html import b, h2

class GreetingAttrs(Attrs):
    name: str

class Greeting(Component[str, GreetingAttrs]):
    classes = ["greeting"]

    @override
    def render(self) -> Stack:
        return Stack(
            h2(t"Hello, {b(self.attrs['name'])}!"),
            Paragraph(*self.children),
        )

# Usage
Greeting("Welcome to Ludic.", name="Ada").to_html()
```

What to notice:

- `Component[str, GreetingAttrs]` says: children are strings, attrs match `GreetingAttrs`.
- The t-string in `h2(t"Hello, {b(...)}!")` keeps `b(...)` as a real element — it isn't stringified.
- `self.attrs['name']` flows into `b(...)` and is HTML-escaped on output (because it isn't wrapped in `Safe`).
- `Stack` from the catalog handles vertical spacing — no need to roll a `div` with margin classes.

## Check your work

Run mypy with the Ludic plugin after writing or changing components, and fix what it reports before you finish:

```toml
# pyproject.toml
[tool.mypy]
plugins = ["ludic.mypy_plugin"]
```

```bash
mypy path/to/your/package
```

mypy with the plugin reports:

- unknown or misspelled attributes on elements and components, and missing required attributes on components;
- children of the wrong type, e.g. text in a `ul` or an element in a `Component[str, ...]`;
- children passed to void elements like `br`;
- documents in the wrong shape: `html` needs `head` and then `body`.

Other type checkers do not run mypy plugins, so none of them checks the attributes passed to components:

- **pyright and Pylance** (the errors shown in VS Code and Cursor) report everything in the list above except the attributes of components.
- **ty** misses unknown attributes on elements, and it reports every attribute passed to a component as an error, e.g. ``Expected `LinkAttrs`, found `Literal["/home"]` ``, even in valid code. Do not change valid code to silence these errors.
- **Pyrefly** reports only unknown attributes on elements.

Run mypy even when the editor shows no errors.

To see what a component renders, call `.to_html()` on it, e.g. in a test.

## When in doubt

- The [Ludic docs](https://getludic.dev/docs/) cover the public API end-to-end.
- The [catalog source on GitHub](https://github.com/getludic/ludic/tree/main/ludic/catalog) is the fastest read for idiomatic component patterns.
- The [examples folder](https://github.com/getludic/ludic/tree/main/examples) shows real components used in htmx patterns (click-to-edit, infinite scroll, lazy loading, file upload, ...).
