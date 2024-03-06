# Component Catalog

The `ludic.catalog` module is meant as a collection of components that could be useful for building Ludic applications.

* Any contributor is welcome to add new components or helpers.
* It also serves as showcase of possible implementations.

## Typography

This module contains the following components:

* `Link`
* `Paragraph`

### `Link` Component

Definition:

```python
class LinkAttrs(Attrs):
    to: str


class Link(ComponentStrict[PrimitiveChildren, LinkAttrs]):
    def render(self) -> a: ...
```

Usage:

```python
Link("github", to="https://github.com")
```

### `Paragraph` Component

Definition:

```python
class Paragraph(Component[AnyChildren, GlobalAttrs]):
    def render(self) -> p: ...
```

Usage:

```python
Paragraph(f"Hello, {b("World")}!")
```

## Buttons

This module contains the following components:

* `Button` - regular button with the `btn` class
* `ButtonPrimary` - regular button with the `btn btn-primary` class
* `ButtonSecondary` - regular button with the `btn btn-secondary` class
* `ButtonDanger` - regular button with the `btn btn-danger` class
* `ButtonWarning` - regular button with the `btn btn-warning` class
* `ButtonInfo` - regular button with the `btn btn-info` class

## Navigation

This module contains the following components:

* `NavItem`
* `Navigation`

These components work together:

```python

class NavItemAttrs(GlobalAttrs):
    to: str


class NavItem(Component[PrimitiveChildren, NavItemAttrs]):
    def render(self) -> li: ...


class Navigation(Component[NavItem, GlobalAttrs]):
    def render(self) -> ul: ...
```

Here is the usage:

```python
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

## Lists

This module contains the following components:

- `Pairs`
- `Key`
- `Value`

Here is the definition:

```python
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

These components are in an experimental mode. There is the possibility to automatically create form fields from annotations, but it is far from production ready.

Here is the definition:

```python
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
Form(
    InputField("John", label="Name", type="input", name="person_name"),
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

    This module is in an experimental state. It is not clear yet how to make generation of form fields from annotations flexible enough.

Here is what you can do:

```python
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

The `create_fields` function generates form fields from annotations. It generates only fields which are annotated with the `FieldMeta` dataclass:

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

These components are in an experimental mode. There is the possibility to automatically create tables even containing form fields and actions from annotations, but it is far from production ready.

Here is the definition:

```python
class TableRow(Component[AnyChildren, GlobalAttrs]): ...
    def render(self) -> tr: ...


class TableHead(Component[AnyChildren, GlobalAttrs]):
    def render(self) -> tr: ...


THead = TypeVar("THead", bound=BaseElement, default=TableHead)
TRow = TypeVar("TRow", bound=BaseElement, default=TableRow)


class TableType(ComponentStrict[THead, *tuple[TRow, ...], GlobalAttrs]): ...
    def render(self) -> table: ...


class Table(TableType[TableHead, TableRow]): ...
```

This allows the following instantiations:

```python
TableType[PersonHead, PersonRow](
    PersonHead("Name", "Age"),
    PersonRow("John", 42),
    PersonRow("Jane", 23),
)

Table(
    TableHead("Name", "Age"),
    TableRow("John", 42),
    TableRow("Jane", 23),
)
```

### Generating Table Rows

!!! warning "Experimental"

    This module is in an experimental state. It is not clear yet how to make generation of tables from annotations and combine them with forms, button actions and so on. The idea is to make it flexible and extensible.

Here is what you can do:

```python
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

The `create_rows` function expects people and a specification using the `ColumnMeta` annotation. It generates table from that. Here are all the properties of the `ColumnMeta` dataclass:

```python
@dataclass
class ColumnMeta:
    identifier: bool = False
    label: str | None = None
    kind: Literal["text"] | FieldMeta = "text"
    parser: Callable[[Any], PrimitiveChildren] | None = None
```

The `kind` can be a simple text or a `FieldMeta` instance which generates a form field.
