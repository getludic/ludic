# Components

In Ludic, you can create components similar to React components. These components don't have anything like a state similar to React, but they do consist of children and attributes.

## Key Concepts

- **Components**: a component is reusable chunk of code that defines a piece of your user interface. Think of it like a blueprint for an HTML element, but more powerful.
- **Elements**: these represent the individual HTML tags (like `<a>`, `<div>`, `<h1>`, etc.) that make up the structure of your page.
- **Attributes**: These help define properties on your components and elements. They let you modify things like a link's destination, text color, or an element's size.
- **Hierarchy**: Components can contain other components or elements, creating a tree-like structure.
- **Types**: A safety net to help you write correct code, preventing errors just like making sure LEGO pieces fit together properly.

## Types of Components

- **Regular**: These are flexible, letting you have multiple children of any type.
- **Strict**: Perfect for when you need precise control over the structure of your component – like a table where you must have a *head* and a *body*.

## Regular Components

Let's break down the simple Link component example from the README:

```python
from typing import override

from ludic.types import Attrs, Component


class LinkAttrs(Attrs):
    to: str


class Link(Component[str, LinkAttrs]):
    @override
    def render(self):
        return a(
            *self.children,
            href=self.attrs["to"],
            style={"color": "#abc"},
        )
```

- *HTML Rendering*: This component renders as the following HTML element:
    - `<a href="..." style="color:#abc">...</a>`
- *Type Hints*: `Component[str, LinkAttrs]` provides type safety:
    - `str`: Enforces that all children of the component must be strings.
    - `LinkAttrs`: Ensures the required to attribute is present.
- *Attributes*: LinkAttrs inherits from `Attrs`, which is a `TypedDict` (a dictionary with defined types for its keys).

The component would be instantiated like this:

```python
Link("here", to="https://example.org")
```

Static type checkers will validate that you're providing the correct arguments and their types.

**Multiple Children**

The current definition doesn't strictly enforce a single child. This means you could technically pass multiple strings (`Link("a", "b")`). To create a stricter component, inherit from `ComponentStrict`: This subclass of Component allows for finer control over children. More about this in the next section.

## Strict Components

Strict components offer more precise control over the types and structure of their children compared to regular components. Let's illustrate this with a Table component example:

```python
from ludic.attrs import GlobalAttrs
from ludic.html import thead, tbody, tr


class TableHead(ComponentStrict[tr, GlobalAttrs]):
    @override
    def render(self) -> thead:
        return thead(*self.children, **self.attrs)


class TableBody(ComponentStrict[*tuple[tr, ...], GlobalAttrs]):
    @override
    def render(self) -> tbody:
        return tbody(*self.children, **self.attrs)


class Table(ComponentStrict[TableHead, TableBody, GlobalAttrs]):
    @override
    def render(self) -> table:
        return table(
            self.children[0],
            self.children[1],
            **self.attrs,
        )
```

**Explanation**

- *Strictness*: The `ComponentStrict` class allows you to enforce the exact types and order of children.
- *Table Structure*:
    - `Table`: Expects precisely two children: a `TableHead` followed by a `TableBody`.
    - `TableHead`: Accepts only a single `tr` (table row) element as its child.
    - `TableBody`: Accepts a variable number of `tr` elements as children.
- *Type Hints*: The `*tuple[tr, ...]` syntax indicates that `TableBody` accepts zero or more tr elements.

**Valid Usage (Passes Type Checking)**

```python
Table(
    TableHead(tr(...)),  # Table head with a single row
    TableBody(tr(...), tr(...))  # Table body with multiple rows
)
```

**Key Benefits**

Strict components help you:

- *Enforce Structure*: Prevent incorrect usage that could break your component's layout or functionality.
- *Type Safety*: Static type checkers ensure you're building valid component hierarchies.


## Attributes

To ensure type safety and clarity, define your component attributes using a subclass of the `Attrs` class. Here's how:

```python
from typing import NotRequired

from ludic.types import Attrs


class PersonAttrs(Attrs):
    id: str
    name: str
    is_active: NotRequired[bool]
```

**Understanding `Attrs` and `TypedDict`**

- The `Attrs` class is built upon Python's `TypedDict` concept (see [PEP-589](https://peps.python.org/pep-0589/) for details). This provides type hints for dictionary-like data structures.

**Controlling Required Attributes**

- In the above case, all attributes except for `is_active` are required. If you want to make all attributes NOT required by default, you can pass the `total=False` keyword argument to the class definition:

```python
from typing import Required

from ludic.types import Attrs

class PersonAttrs(Attrs, total=False):
    id: Required[str]
    name: str
    is_active: bool
```

In this case all attributes are optional except for the `id` attribute.

!!! note "The `Attrs` declaration is an information for type checkers"

    `Attrs` class just provides typing information for static type checkers. Your code will work even if you pass key-word arguments to components without declaring them first.

**Extending HTML Attributes**

All attributes can also subclass from other classes, for example, you can extend the attributes for the `<button>` HTML element:

```python
from ludic.html import TdAttrs
from ludic.types import Attrs


class TableCellAttrs(TdAttrs):
    is_numeric: bool
```

When implementing the component's `render()` method, you might find the `attrs_for(...)` helper useful too:

```python
class TableCell(ComponentStrict[str, TableCellAttrs]):
    @override
    def render(self) -> td:
        return td(self.children[0], **self.attrs_for(td))
```

The method passes only the attributes registered for the `<td>` element.

### Pre-defined Attributes

The `ludic.attrs` module contains many attributes definition which you can reuse in your components, hare are the most used ones:

- `HtmlAttrs` - Global HTML attributes available in all elements
    - The `class` and `for` attributes have the aliases `class_` and `for_`
- `EventAttrs` - Event HTML attributes like `onclick`, `onkey`, and so on.
- `HtmxAttrs` - All [HTMX attributes](https://htmx.org/reference/) available.
    - All HTMX attributes have aliases with underscore, e.g. `hx_target`
- `GlobalAttrs` subclasses `HtmlAttrs`, `EventAttrs` and `HtmxAttrs`
- `[HtmlElementName]Attrs` - e.g. `ButtonAttrs`, `TdAttrs`, and so on.

## HTML Elements

All available HTML elements can be found in `ludic.html` module. The corresponding attributes are located in the `ludic.attrs` module.

### Rendering

To check how an element or component instance renders in HTML, you can use the `.to_html()` method:

```python
p("click ", Link("here", to="https://example.com")).to_html()
'<p>click <a href="https://example.com">here</a></p>'
```

Any string is automatically HTML escaped:

```python
p("<script>alert('Hello world')</script>").to_html()
'<p>&lt;script&gt;alert(&#x27;Hello world&#x27;)&lt;/script&gt;</p>'
```

## Using `f-strings`

In Ludic, f-strings offer a bit more readable way to construct component content, especially if you need to do a lot of formatting with `<b>`, `<i>` and other elements for improving typography. Let's modify the previous example using f-strings:

```python
p1 = p(f"click {Link("here", to="https://example.com")}")
p2 = p("click ", Link("here", to="https://example.com"))

assert p1 == p2  # Identical components
```
**Important Note: Memory Considerations**

- *Temporary Dictionaries*: to make f-strings safely work, they internally create temporary dictionaries to hold the components instances. To avoid memory leaks, these dictionaries need to be consumed by a component.
- *Potential Leaks*: Memory leaks can occur if:
    - Component initialization with the f-string fails.
    - You store an f-string in a variable but don't pass it to a component.

There are two cases it can create hanging objects (memory leaks):

!!! warning "Possible memory leak"

    The implementation of f-strings requires creation of a temporary dict which can result in hanging objects in memory. To avoid memory leaks, there is the `BaseElement.formatter` attribute which is a context manager clearing the temporary dict on exit.

**The `BaseElement.formatter` Context Manager**

```python
from ludic.types import BaseElement

with BaseElement.formatter:
    # you can do anything with f-strings here, no memory leak
    # is created since formatter dict is cleared on exit
```

**Web Framework Request Handlers**

The Ludic Web Framework (built on Starlette) automatically wraps request handlers with `BaseElement.formatter`, providing a safe environment for f-strings.

**Key Takeaway**

While f-strings are convenient, exercise caution to prevent memory leaks. Use them within the provided safety mechanisms. In contexts like task queues or other web frameworks, you can use similar mechanism of wrapping to achieve memory safety.

## Available Methods

All *components* (and *elements* too) inherit the following properties and methods from the `BaseElement` class:

- `BaseElement`
    - `children` - children of the component
    - `attrs` - dictionary containing attributes
    - `to_html()` - converts the component to HTML document
    - `to_string()` - converts the component to a string representation of the tree
    - `attrs_for(...)` - filter attributes to return only those valid for given element or component
    - `has_attributes()` - whether the component has any attributes
    - `is_simple()` - whether the component contains one primitive child
    - `render()` (*abstract method*) - render the component

## Types and Helpers

The `ludic.types` module contains many useful types:

- `NoChildren` - Makes a component accept no children.
    - example: `class Br(Component[NoChildren, Attrs]): ...`
- `PrimitiveChildren` - Makes a component accept only `str`, `int`, `float` or `bool`
    - example: `class Paragraph(Component[PrimitiveChildren, Attrs]): ...`
- `ComplexChildren` - Makes a component accept only non-primitive types.
    - example: `class Body(Component[ComplexChildren, Attrs]): ...`
- `AnyChildren` - Makes a component accept any children types.
    - example: `class Section(Component[AnyChildren, Attrs]): ...`
- `TAttrs` - type variable for attributes
- `TChildren` - type variable for children of components
- `TChildrenArgs` - type variable for children of strict components
- `Attrs` - base for attributes
- `BaseElement` - base for elements
- `Element` - base for HTML elements
- `ElementStrict` - base for strict HTML elements
    - for example, the `<html>` element passes type checking only if the first child is `<head>` and the second is `<body>`
- `Component` - abstract class for components
- `ComponentStrict` - abstract class for strict components
- `Blank` - represents a blank component which is not rendered, only its children
    - example: `Blank(f"Hello {b("world")}").to_html() == 'Hello <b>world</b>'`
- `Safe` - marker for a safe string which is not escaped
    - example: `a(Safe("This <b>won't</b> be escaped."))`
- `JavaScript` - marker for javascript, subclasses `Safe`
- `GlobalStyles` - type for CSS styles
