# Component Catalog

The `ludic.catalog` module is meant as a collection of components that could be useful for building applications with the Ludic framework.

* Any contributor is welcome to add new components or helpers.
* It also serves as a showcase of possible implementations.

## Typography

The module `ludic.catalog.typography` contains the following components:

* `Link`
* `Paragraph`

### `Link` Component

Definition:

```python
# ludic/catalog/typography.py

class LinkAttrs(Attrs):
    to: str

class Link(ComponentStrict[PrimitiveChildren, LinkAttrs]):
    def render(self) -> a: ...
```

Usage:

```python
from ludic.catalog.typography import Link

Link("github", to="https://github.com")
```

### `Paragraph` Component

Definition:

```python
# ludic/catalog/typography.py

class Paragraph(Component[AnyChildren, GlobalAttrs]):
    def render(self) -> p: ...
```

Usage:

```python
from ludic.catalog.typography import Paragraph

Paragraph(f"Hello, {b("World")}!")
```

## Buttons

The module `ludic.catalog.buttons` contains the following components:

* `Button` - regular button with the `btn` class
* `ButtonPrimary` - regular button with the `btn btn-primary` class
* `ButtonSecondary` - regular button with the `btn btn-secondary` class
* `ButtonDanger` - regular button with the `btn btn-danger` class
* `ButtonWarning` - regular button with the `btn btn-warning` class
* `ButtonInfo` - regular button with the `btn btn-info` class

## Navigation

The module `ludic.catalog.navigation` contains the following components:

* `NavItem`
* `Navigation`

These components have the following definition:

```python
# ludic/catalog/navigation.py

class NavItemAttrs(GlobalAttrs):
    to: str

class NavItem(Component[PrimitiveChildren, NavItemAttrs]):
    def render(self) -> li: ...

class Navigation(Component[NavItem, GlobalAttrs]):
    def render(self) -> ul: ...
```

Here is the usage:

```python
from ludic.catalog.navigation import Navigation, NavItem

Navigation(
    NavItem("Home", to="/"),
    NavItem("About", to="/about"),
)
```

This would render as the following HTML tree:

```html
<ul class="navigation">
    <li id="home">
        <a href="/">Home</a>
    </li>
    <li id="about">
        <a href="/about">About</a>
    </li>
</ul>
```

## Items

The module `ludic.catalog.items` contains the following components:

* `Pairs`
* `Key`
* `Value`

Here is the definition:

```python
# ludic/catalog/items.py

class Key(Component[PrimitiveChildren, GlobalAttrs]):
    def render(self) -> dt: ...

class Value(Component[PrimitiveChildren, GlobalAttrs]):
    def render(self) -> dd: ...

class PairsAttrs(GlobalAttrs, total=False):
    items: Iterable[tuple[str, PrimitiveChildren]]

class Pairs(Component[Key | Value, PairsAttrs]):
    def render(self) -> dl: ...
```

There are two possible ways to instantiate these components:

```python
from ludic.catalog.items import Pairs, Key, Value

Pairs(
    Key("Name"),
    Value("John"),
    Key("Age"),
    Value(42),
)
```

Or passing the `items` attribute:

```python
Pairs(
    items={"name": "John", "age": 42}.items(),
)
```

## Forms

These components located in `ludic.catalog.forms` are in an experimental mode. There is the possibility to automatically create form fields from annotations, but it is far from production-ready.

Here is the definition:

```python
# ludic/catalog/forms.py

class FieldAttrs(Attrs, total=False):
    label: str
    class_div: str

class InputFieldAttrs(FieldAttrs, InputAttrs): ...
class TextAreaFieldAttrs(FieldAttrs, TextAreaAttrs): ...

class FormField(Component[TChildren, TAttrs]): ...
class InputField(FormField[NoChildren, InputFieldAttrs]): ...
class TextAreaField(FormField[PrimitiveChildren, TextAreaFieldAttrs]): ...

class Form(Component[ComplexChildren, FormAttrs]):
    def render(self) -> form: ...
```

Here is how you would use these components:

```python
from ludic.catalog.forms import Form, InputField, TextAreaField
from ludic.catalog.buttons import Button

Form(
    InputField(value="John", label="Name", type="input", name="person_name"),
    TextAreaField("...", label="About you", name="person_about"),
    Button("Update", type="submit"),
    hx_get="/people/1",
)
```

Which would render as:

```html
<form hx-get="/people/1">
    <div class="form-group">
        <label for="person_name">Name</label>
        <input type="input" name="person_name" id="person_name" />
    </div>
    <div class="form-group">
        <label for="person_about">About you</label>
        <textarea name="person_about" id="person_about">...</textarea>
    </div>
    <button type="submit" class="btn">Update</button>
</form>
```

### Generating Form Fields

!!! warning "Experimental"

    This module is in an experimental state. It is not clear yet how to make the generation of form fields from annotations flexible enough.

Here is what you can do:

```python
from typing import Annotated
from ludic.catalog.forms import Form, FieldMeta, create_fields
from ludic.types import Attrs

class CustomerAttrs(Attrs):
    id: str
    name: Annotated[
        str,
        FieldMeta(label="Customer Name"),
    ]

customer = Customer(id=1, name="John Doe")
fields = create_fields(customer, spec=CustomerAttrs)

form = Form(*fields)
```

The `create_fields` function generates form fields from annotations. It generates only fields that are annotated with the `FieldMeta` dataclass:

```python
@dataclass
class FieldMeta:
    label: str | Literal["auto"] | None = "auto"
    kind: Literal["input", "textarea", "checkbox"] = "input"
    type: Literal["text", "email", "password", "hidden"] = "text"
    attrs: InputAttrs | TextAreaAttrs | None = None
    parser: Callable[[Any], PrimitiveChildren] | None = None
```

The `parser` attribute validates and parses the field. Here is how you would use it:

```python
def parse_email(email: str) -> str:
    if len(email.split("@")) != 2:
        raise ValidationError("Invalid email")
    return email

class CustomerAttrs(Attrs):
    id: str
    name: Annotated[
        str,
        FieldMeta(label="Email", parser=parse_email),
    ]
```

## Tables

These components located in `ludic.catalog.tables` are in an experimental mode. There is the possibility to automatically create tables even containing form fields and actions from annotations, but it is far from production-ready.

Here is the definition:

```python
# ludic/catalog/tables.py

class TableRow(Component[AnyChildren, GlobalAttrs]): ...
    def render(self) -> tr: ...

class TableHead(Component[AnyChildren, GlobalAttrs]):
    def render(self) -> tr: ...

THead = TypeVar("THead", bound=BaseElement, default=TableHead)
TRow = TypeVar("TRow", bound=BaseElement, default=TableRow)

class Table(ComponentStrict[THead, *tuple[TRow, ...], GlobalAttrs]): ...
    def render(self) -> table: ...
```

This allows the following instantiations:

```python
from ludic.catalog.tables import Table, TableHead, TableRow

Table(
    TableHead("Name", "Age"),
    TableRow("John", 42),
    TableRow("Jane", 23),
)
```

You can also specify different types of header and body:

```python
from ludic.catalog.tables import Table

from your_app.components import PersonHead, PersonRow

Table[PersonHead, PersonRow](
    PersonHead("Name", "Age"),
    PersonRow("John", 42),
    PersonRow("Jane", 23),
)
```

### Generating Table Rows

!!! warning "Experimental"

    This module is in an experimental state. It is not clear yet how to make the generation of tables from annotations and combine them with forms, button actions, and so on. The idea is to make it flexible and extensible.

Here is what you can do:

```python
from typing import Annotated
from ludic.catalog.tables import Table, create_rows
from ludic.types import Attrs

class PersonAttrs(Attrs):
    id: Annotated[int, ColumnMeta(identifier=True)]
    name: Annotated[str, ColumnMeta(label="Full Name")]
    email: Annotated[str, ColumnMeta(label="Email")]

people = [
    {"id": 1, "name": "John Doe", "email": "john@j.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@s.com"},
]
rows = create_rows(people, spec=PersonAttrs)

table = Table(*rows)
```

The `create_rows` function expects people and a specification using the `ColumnMeta` annotation. It generates a table from that. Here are all the properties of the `ColumnMeta` dataclass:

```python
@dataclass
class ColumnMeta:
    identifier: bool = False
    label: str | None = None
    kind: Literal["text"] | FieldMeta = "text"
    parser: Callable[[Any], PrimitiveChildren] | None = None
```

The `kind` can be a simple text or a `FieldMeta` instance which generates a form field.

## Lazy Loader

The module `ludic.catalog.loaders` contains the following component:

* `LazyLoader`

This component allows lazy loading data after it is rendered in the browser. For this component to work, you need to have HTMX script loaded.

```python
# ludic/catalog/loaders.py

class LazyLoaderAttrs(GlobalAttrs):
    load_url: str
    placeholder: NotRequired[AnyChildren]  # default is "Loading..."

class LazyLoader(Component[AnyChildren, LazyLoaderAttrs]):
    @override
    def render(self) -> div: ...
```

Here is how you would use the component:

```python
from ludic.catalog.loaders import LazyLoader
from ludic.html import span

LazyLoader(load_url="/content-to-load", placeholder=span(...))
```

The placeholder will be shown while the data is loading.
