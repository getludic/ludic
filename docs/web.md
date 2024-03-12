# Web Framework

The Ludic library provides wrappers around [Starlette](https://www.starlette.io/) framework to make it easy to write asynchronous web applications based on HTMX and Ludic Components.

Ludic includes an application class `LudicApp` that tight together all other functionality. Here is how you can create an instance of the class:

```python
from ludic.web import LudicApp

app = LudicApp()
```

The `LudicApp` class supports the same parameters as the `Starlette` class from the *Starlette* framework.

## Routing

To register handlers in your app, you can use the `routes` arguments of the `LudicApp` class like this:

```python
from ludic.web import LudicApp, Request
from ludic.web.routing import Route


def homepage(request: Request) -> p:
    return p("Hello, world!")


def startup():
    print('Ready to go')


routes = [
    Route("/", homepage),
]

app = LudicApp(debug=True, routes=routes, on_startup=[startup])
```

## Instantiating The Application

*class* `ludic.app.LudicApp`*(debug=False, routes=None, middleware=None, exception_handlers=None, on_startup=None, on_shutdown=None, lifespan=None)*

Creates an application instance.

**Parameters:**

The list of parameters can be found in the [Starlette documentation](https://www.starlette.io/applications/#instantiating-the-application).

**Methods:**

- `app.register_route`*(path: str, method: str = "GET")* - decorator to register function based endpoint handler
- `app.get`*(path: str, **kwargs: Any)* - decorator to register function endpoint handling GET HTTP method
- `app.post`*(path: str, **kwargs: Any)* - decorator to register function endpoint handling POST HTTP method
- `app.put`*(path: str, **kwargs: Any)* - decorator to register function endpoint handling PUT HTTP method
- `app.patch`*(path: str, **kwargs: Any)* - decorator to register function endpoint handling PATCH HTTP method
- `app.delete`*(path: str, **kwargs: Any)* - decorator to register function endpoint handling DELETE HTTP method
- `app.endpoint`*(path: str)* - decorator to register component based endpoint
- `app.add_route`*(path: str, route: Callable[..., Any], method: str, **kwargs: Any)* - register any endpoint handler
- `app.url_path_for`*(name: str, /, **path_params: Any)* - get URL path for endpoint of given name
- `app.exception_handler`*(exc_class_or_status_code: int | type[Exception])* - register exception handler

## Endpoints

There are three types of endpoints that you can create:

* [Function Based](#function-based)
* [Component Based](#component-based)

### Function Based

These are functions returning Ludic components, a tuple or the [Starlette's Response class](https://www.starlette.io/responses/).

Here are some examples of function handlers registered in Ludic:

```python
from ludic.web.datastructures import FormData
from ludic.web.exceptions import NotFoundError

from your_app.pages import Page
from your_app.models import Person
from your_app.components import Header


@app.get("/people/{id}")
async def show_person(id: str) -> Page:
    person: Person = db.people.get(id)

    if person is None:
        raise NotFoundError("Contact not found")

    return Page(
        Header(person.name),
        ...
    )


@app.post("/people/")
async def register_person(data: FormData) -> Page:
    person: Person = Person.objects.create(**data)
    return await show_person(person.id), 202
```

### Component Based

While it is possible to use function based handlers everywhere, in case of HTMX based web applications, we want to also create a lot of endpoints rendering only single form element, table, and so on. We don't need to always return the whole HTML document in `<html>` tag. We could use function based handlers for that, however, it is often better to think of endpoints as just another components.

Component based endpoints can only have one generic argument which is the type of attributes. They cannot have children.

Here is an example where we create two component based endpoints:

```python
from ludic.web import Endpoint
from ludic.web.datastructures import FormData

from your_app.pages import Page
from your_app.models import Person
from your_app.components import Header, Body


@app.get("/")
async def index() -> Page:
    return Page(
        Header("Click To Edit"),
        Body(*[await Contact.get(contact_id) for contact_id in db.contacts]),
    )


@app.endpoint("/contacts/{id}")
class Contact(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        contact = db.contacts.get(id)
        return cls(**contact.as_dict())

    @classmethod
    async def put(cls, id: str, data: FormData) -> Self:
        contact = db.contacts.get(id)
        contact.update(**data)
        return await cls.get(id)

    @override
    def render(self) -> div:
        return div(
            Pairs(items=self.attrs.items()),
            ButtonPrimary(
                "Click To Edit",
                hx_get=self.url_for(ContactForm),
            ),
            hx_target="this",
            hx_swap="outerHTML",
        )


@app.endpoint("/contacts/{id}/form/")
class ContactForm(Endpoint[ContactAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        contact = db.contacts.get(id)
        return cls(**contact.as_dict())

    @override
    def render(self) -> Form:
        return Form(
            # ... form fields definition here ...,
            ButtonPrimary("Submit"),
            ButtonDanger("Cancel", hx_get=self.url_for(Contact)),
            hx_put=self.url_for(Contact),
            hx_target="this",
        )
```

The benefit of this approach is that you can create components which generate the URL path for other component based endpoints with the `url_for` method. More about that in the next section.

### Reverse URL Lookups

There are two possible ways to generate the URL for a particular route handled by an endpoint:

- `Request.url_for`
- `Endpoint.url_for`

**`Request.url_for(endpoint: Callable[..., Any] | str, ...)`**

This method is available on the `ludic.web.requests.Request` object. It generates and `URLPath` object for given endpoint.

**`Endpoint.url_for(endpoint: type[RoutedProtocol] | str, ...)`**

This method is available on a component based endpoint. It has one small advantage over the `request`'s method -- if the destination component defines the same attributes, the path parameters are automatically extracted so you don't need to pass them via key-word arguments. Here are examples:

- `ContactForm(...).url_for(Contact)` - Even though the `ContactForm` endpoint requires the `id` path parameter, it is automatically taken from `ContactForm(...).attrs` since the type of `ContactForm[ContactAttrs]` and `Contact[ContactAttrs]` are the same.
- If these attributes types are not equal, you need to specify the URL path parameter explicitly, e.g. `ContactForm(...).url_for(Foo, id=self.attrs["foo_id"])`
- if the first argument to `url_for` is a the name of the endpoint, you need to always specify the URL path parameters explicitly.

### Handler Responses

Your handler is not required to return only a valid element or component, you can also modify headers, status code, or return a `JSONResponse`:

```python
from ludic import types
from ludic.html import div

@app.get("/")
def index() -> tuple[div, types.Headers]:
    return div("Headers Example"), {"Content-Type": "..."}
```

When it comes to handler's return type, you have the following options:

- `BaseElement` - any element or component
- `tuple[BaseElement, int]` - any element or component and a status code
- `tuple[BaseElement, types.Headers]` - any element or component and headers as a dict
- `tuple[BaseElement, int, types.Headers]` - any element or component, status code, and headers
- `starlette.responses.Response` - valid Starlette `Response` object

### Handler Arguments

Here is a list of arguments that your handlers can optionally define (they need to be correctly type annotated):

- `<name>: <type>` - if the endpoint accepts path parameters, they can be specified in the handler's arguments
- `request: Request` - the Ludic's slightly modified `ludic.web.requests.Request` class based on [Starlette's one](https://www.starlette.io/requests/).
- `params: QueryParams` - contain query string parameters and can be imported from `ludic.web.datastructures.QueryParams`
- `data: FormData` - an immutable multi-dict, containing both file uploads and text input from form submission
- `headers: Headers` - HTTP headers exposed as an immutable, case-insensitive, multi-dict

## Parsers

!!! warning "Experimental"

    This module is in an experimental state. It is not clear yet how to make parse and validate form data.

The `ludic.parsers` module contains helpers for parsing `FormData`. The way it works is that You define `Attrs` class with `Annotated` arguments like here:

```python
class PersonAttrs(Attrs):
    id: NotRequired[int]
    name: Annotated[str, parse_name]
    email: Annotated[str, parse_email]
```

Now you can use the `Parser` class to annotate arguments of your handler. The parser will attempt to parse form data if any `Callable` is found in the metadata argument of `Annotated`:

```python
from ludic.web.parsers import Parser


@app.put("/people/{id}")
async def update_person(cls, id: str, data: Parser[PersonAttrs]) -> div:
    person = db.people.get(id)
    person.update(data.validate())
    return div(...)  # return updated user
```

The `Parser.validate()` method raises `ludic.parsers.ValidationError` if the request's form data are not valid. If unhandled, this results in `403` status code.

## Error Handlers

You can use error handlers for custom pages for non-ok HTTP status codes. You can register a handler with the `app.exception_handler` decorator:

```python
from your_app.pages import Page


@app.exception_handler(404)
async def not_found() -> Page:
    return Page(
        Header("Page Not Found"),
        Body(Paragraph("The page you are looking for was not found.")),
    )


@app.exception_handler(500)
async def server_error() -> Page:
    return Page(
        Header("Server Error"),
        Body(Paragraph("Server encountered an error during processing.")),
    )
```

Optionally, you can use the `request: Request` and `exc: Exception` arguments for the handler:

```python
@app.exception_handler(500)
async def server_error(request: Request, exc: Exception) -> Page: ...
```

## Exceptions

The `ludic.web.exceptions` contains a lot of useful exception that can be raised in your views and caught in you custom error handlers:

- `ClientError(HTTPException)` - default status code `400`
- `BadRequestError(ClientError)` - default status code `400`
- `UnauthorizedError(ClientError)` - default status code `401`
- `PaymentRequiredError(ClientError)` - default status code `402`
- `ForbiddenError(ClientError)` - default status code `403`
- `NotFoundError(ClientError)` - default status code `404`
- `MethodNotAllowedError(ClientError)` - default status code `405`
- `TooManyRequestsError(ClientError)` - default status code `429`
- `ServerError(HTTPException)` - default status code `500`
- `InternalServerError(ServerError)` - default status code `500`
- `NotImplementedError(ServerError)` - default status code `501`
- `BadGatewayError(ServerError)` - default status code `502`
- `ServiceUnavailableError(ServerError)` - default status code `503`
- `GatewayTimeoutError(ServerError)` - default status code `504`

## WebSockets

WebSockets support is not yet fully tested in Ludic. However, Starlette has a good support for WebSockets so it should be possible tu use Ludic as well.

## Testing

Testing Ludic Web Apps is basically the same as testing Starlette apps which use a `TestClient` class exposing the same interface as `httpx` library. Read more about testing in the [Starlette documentation](https://www.starlette.io/testclient/).
