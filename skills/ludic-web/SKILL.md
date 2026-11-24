---
name: ludic-web
description: >-
  Build web apps with Ludic's web integration — Starlette-based LudicApp,
  typed Endpoint classes, and the FastAPI / Django integrations. Use this
  skill whenever the user is wiring Ludic components into HTTP handlers:
  routing requests with LudicApp, declaring async endpoints that return
  components, subclassing ludic.web.Endpoint, parsing form data with
  Parser, reading path and query parameters, returning htmx partials and
  htmx response headers, raising HTTP errors, mounting Ludic inside an
  existing FastAPI or Django app, or generating URLs from a request
  (request.url_for, request.url_path_for, Endpoint.url_for). Always trigger
  this skill on any code that generates absolute URLs from request data —
  there is a host header poisoning class of vulnerability that affects every
  Ludic web app and needs explicit guarding. Also trigger on questions about
  ludic.web.Request, LudicResponse, the Starlette/FastAPI/Django bridge, or
  htmx response patterns (HX-Trigger, HX-Redirect, HX-Push-Url headers). For
  pure component authoring without an HTTP layer, use the companion
  `ludic-components` skill.
metadata:
  type: framework-guide
  framework: ludic
  version: "1.x"
---

# Ludic Web

This skill covers the **web integration** side of Ludic — how to serve components over HTTP. The component authoring side (writing `Component` subclasses, t-strings, the catalog, the `Safe` boundary) is covered in the companion `ludic-components` skill.

Ludic's web layer is a thin wrapper around [Starlette](https://www.starlette.io/). Components also work in FastAPI and Django via the optional integrations in `ludic.contrib`.

Ludic 1.x needs Python 3.14+ and writes text mixed with elements as t-strings (`t"..."`). A project on Ludic 0.5.x (Python 3.12 or 3.13) uses f-strings instead; the `ludic-components` skill explains the difference.

## The basic shape

```python
from ludic.html import b, p
from ludic.web import LudicApp

app = LudicApp()


@app.get("/")
async def homepage() -> p:
    return p(t"Hello {b('Stranger')}!")
```

What's happening:

- `LudicApp` is a subclass of Starlette's `Starlette`. When a handler returns an element, the app renders it with `.to_html()` and sends it as an HTML response.
- The app does not wrap the element in a page. Return a whole document for a full page (see [Whole pages](#whole-pages)) and a fragment for an htmx swap.
- Handlers can be async or sync. Sync handlers run in a thread pool.

Run it with any ASGI server:

```bash
uvicorn web:app
```

### What a handler receives

Ludic calls the handler with keyword arguments, picked by the name and the type annotation of each parameter:

| Parameter | Value |
|---|---|
| a name of a path parameter, e.g. `id` for `"/items/{id}"` | the path parameter; path parameters are passed only when the handler takes all of them |
| `request: Request` | the request, `ludic.web.Request` (a Starlette request) |
| `data: Parser[SomeAttrs]` | the form data; `data.validate()` returns it as `SomeAttrs` |
| `form: FormData` | the raw form data |
| `params: QueryParams` | the query parameters |
| `headers: Headers` | the request headers |
| `page: str \| None` | the query parameter `page`, or `None` |

`FormData`, `QueryParams` and `Headers` come from `ludic.web.datastructures`.

### What a handler returns

| Return value | Response |
|---|---|
| an element | HTML, status 200 |
| `(element, 201)` | HTML with this status |
| `(element, {"HX-Trigger": "saved"})` | HTML with these headers |
| `(element, 201, {"HX-Trigger": "saved"})` | HTML with this status and headers |
| a Starlette `Response` | sent as it is |
| a `str`, `int`, `float` or `bool` | plain text |
| `None` | an empty `204 No Content` |

To answer with an error status, raise an exception from `ludic.web.exceptions`, such as `NotFoundError` (404) or `BadRequestError` (400).

## Endpoints as classes

For anything beyond a trivial GET, use an `Endpoint`. An endpoint is a component bound to a route:

- `@app.endpoint(path)` registers it.
- Its HTTP methods (`get`, `post`, `put`, `patch`, `delete`) are **class methods**. They receive the same arguments as a handler and usually return an instance of the endpoint.
- `render()` turns the instance into HTML, like in any component.

So one class renders the resource both inside a full page and in the htmx response that updates it.

```python
from typing import Self, override

from ludic.attrs import Attrs
from ludic.html import button, form, input, span
from ludic.web import Endpoint, LudicApp
from ludic.web.exceptions import NotFoundError
from ludic.web.parsers import Parser

app = LudicApp()


class ItemForm(Attrs):
    name: str


class ItemAttrs(ItemForm):
    id: str


ITEMS: dict[str, ItemAttrs] = {"1": {"id": "1", "name": "Teapot"}}


@app.endpoint("/items/{id}")
class Item(Endpoint[ItemAttrs]):
    @classmethod
    async def get(cls, id: str) -> Self:
        if id not in ITEMS:
            raise NotFoundError("Item not found")
        return cls(**ITEMS[id])

    @classmethod
    async def put(cls, id: str, data: Parser[ItemForm]) -> Self:
        if id not in ITEMS:
            raise NotFoundError("Item not found")
        ITEMS[id] = {"id": id, "name": data.validate()["name"]}
        return cls(**ITEMS[id])

    @override
    def render(self) -> form:
        return form(
            span(t"Item {self.attrs['id']}"),
            input(name="name", value=self.attrs["name"]),
            button("Save", type="submit"),
            hx_put=self.url_for(Item).path,
            hx_swap="outerHTML",
        )
```

Notes:

- `Parser[ItemForm]` reads the form data. `validate()` checks it against the `ItemForm` TypedDict and raises `ValidationError`, a `400 Bad Request`, when it does not match. Form values are strings; to convert one, annotate the key with a parser, e.g. `count: Annotated[int, int]`.
- `self.url_for(Item)` fills the path parameters from the endpoint's own attributes, so `id` does not have to be passed. Take `.path` of the result: see [Generating URLs](#generating-urls--beware-host-header-poisoning).
- `self.url_for` and `self.request` work only while the endpoint renders as part of a response, because they read the request from the render context.
- `self.lazy_load(OtherEndpoint)` renders a placeholder that htmx replaces with the other endpoint's content once the page loads.

## Whole pages

The catalog's `HtmlPage`, `Head` and `Body` build a complete document. `Head` adds the CSS collected from the components, and `Body(..., htmx_version=...)` adds the htmx script:

```python
from ludic.catalog.layouts import Stack
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.html import h1, p
from ludic.web import LudicApp

app = LudicApp()


@app.get("/")
async def index() -> HtmlPage:
    return HtmlPage(
        Head(title="Items"),
        Body(
            Stack(h1("Items"), p("Click an item to edit it.")),
            htmx_version="2.0.4",
        ),
    )
```

In a real app, write your own page component that returns `HtmlPage` and takes the content as children, so every handler shares the same layout.

## htmx response patterns

A handler called by htmx returns the fragment that htmx swaps into the page. Set htmx response headers (`HX-Trigger`, `HX-Redirect`, `HX-Push-Url`, ...) by returning a tuple:

```python
from ludic.attrs import Attrs
from ludic.html import li
from ludic.web import LudicApp
from ludic.web.parsers import Parser

app = LudicApp()


class TodoForm(Attrs):
    title: str


@app.post("/todos")
async def create_todo(data: Parser[TodoForm]) -> tuple[li, int, dict[str, str]]:
    todo = data.validate()
    return li(todo["title"]), 201, {"HX-Trigger": "todoCreated"}
```

`LudicResponse` does the same when you need a response object, e.g. in a middleware or an exception handler:

```python
from ludic.html import p
from ludic.web import LudicResponse

response = LudicResponse(p("Saved"), headers={"HX-Push-Url": "/items/1"})
```

## Generating URLs — beware host header poisoning

`request.url_for(...)` and `Endpoint.url_for(...)` return an absolute URL whose scheme and host are derived from the incoming request — ultimately from the HTTP `Host` header (and `X-Forwarded-*` headers when proxy headers are trusted). If your app accepts requests with an untrusted `Host`, an attacker can poison every absolute URL you render — including `hx-get` / `hx-post` attributes, links, redirects, and links sent in outbound messages — pointing the browser at an attacker-controlled domain.

**Mitigations:**

- **Prefer `request.url_path_for(...)`**, or the `.path` of a URL from `request.url_for(...)` / `self.url_for(...)`, for in-app links and htmx attributes. Relative paths cannot be poisoned and are usually what you want anyway.
- **Install `starlette.middleware.trustedhost.TrustedHostMiddleware`** with an explicit `allowed_hosts` list so the app rejects requests with a forged `Host` header before any handler runs.
- **Behind a reverse proxy or CDN**, configure `ProxyHeadersMiddleware` (or an equivalent) with a trusted-proxy allowlist so `X-Forwarded-Host` / `X-Forwarded-Proto` are only honored from your own infrastructure.

FastAPI users get the same exposure: `Request.url_for(...)` is reachable from FastAPI handlers and the same advice applies.

```python
from ludic.html import a, button, div, p
from ludic.web import LudicApp, Request

app = LudicApp()


@app.get("/users/{user_id}", name="profile")
async def profile(user_id: str) -> p:
    return p(t"User {user_id}")


@app.get("/")
async def index(request: Request) -> div:
    return div(
        # good — relative path, can't be poisoned
        a("Profile", href=request.url_path_for("profile", user_id="42")),
        button(
            "Refresh",
            hx_get=request.url_path_for("profile", user_id="42"),
            hx_target="#profile",
        ),
        # avoid for in-app links — host comes from the request
        a("Profile", href=str(request.url_for("profile", user_id="42"))),
    )
```

Both methods also accept an endpoint class instead of a route name, e.g. `request.url_path_for(Item, id="1")`.

If you genuinely need an absolute URL (outbound email links, OAuth redirect URIs, sitemap entries, OpenGraph tags), **don't derive it from the request at all** — read it from configuration you control. A `BASE_URL` env var that's validated at startup is fine; a header from a stranger is not.

### A minimal hardened setup

```python
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from ludic.web import LudicApp

middleware = [
    # Behind a known proxy/CDN only — set trusted_hosts to your proxy's IP range
    Middleware(ProxyHeadersMiddleware, trusted_hosts=["127.0.0.1"]),
    # Reject any request whose Host header isn't one of yours
    Middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"]),
]

app = LudicApp(middleware=middleware)
```

Order matters: `ProxyHeadersMiddleware` runs first so it rewrites the client and host info from `X-Forwarded-*`, then `TrustedHostMiddleware` checks the (now-trusted) `Host` against your allowlist.

## Modules at a glance

- `ludic.web` — `LudicApp`, `Endpoint`, `Request`, `LudicResponse`.
- `ludic.web.parsers` — `Parser[TAttrs]` for a form, `ListParser[TAttrs]` for a form editing many rows at once (field names like `name:id:1`), `ValidationError`.
- `ludic.web.datastructures` — `FormData`, `QueryParams`, `Headers`, `URL`, `URLPath`.
- `ludic.web.exceptions` — HTTP errors to raise from handlers: `BadRequestError`, `UnauthorizedError`, `ForbiddenError`, `NotFoundError`, ...
- `ludic.web.routing` — `Route`, `Mount` and `Router`, for declaring routes without the decorators.

## FastAPI integration

```python
from fastapi import FastAPI

from ludic.contrib.fastapi import LudicRoute
from ludic.html import p

app = FastAPI()
app.router.route_class = LudicRoute  # renders returned elements as HTML


@app.get("/")
async def home() -> p:
    return p("Hello from FastAPI + Ludic")
```

The `[fastapi]` extra installs the dependency: `pip install "ludic[fastapi]"`. The host-header poisoning advice above applies identically here.

## Django integration

Wrap the element in Ludic's `LudicResponse` for Django:

```python
from django.http import HttpRequest

from ludic.contrib.django import LudicResponse
from ludic.html import p


def index(request: HttpRequest) -> LudicResponse:
    return LudicResponse(p("Hello, World!"))
```

The `[django]` extra: `pip install "ludic[django]"`. The Django integration goes through Django's URL resolver and request/response cycle, not Starlette's — so the relevant host-header guard is Django's `ALLOWED_HOSTS` setting and (when proxied) `USE_X_FORWARDED_HOST` / `SECURE_PROXY_SSL_HEADER`. Same threat, framework-native mitigation.

## Endpoint testing

```python
from starlette.testclient import TestClient

from ludic.html import p
from ludic.web import LudicApp

app = LudicApp()


@app.get("/")
async def homepage() -> p:
    return p("Hello")


def test_homepage() -> None:
    with TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.text == "<p>Hello</p>"
```

Because the response body is rendered HTML, you can assert against substrings directly or parse it with whatever HTML library you prefer.

## Check your work

Run mypy with the Ludic plugin after changing endpoints; the `ludic-components` skill describes the setup. It checks the attributes passed to `cls(...)` in the class methods and the elements returned by handlers.

## When in doubt

- The [Ludic web framework docs](https://getludic.dev/docs/web-framework) cover routing, parsers, and responses end-to-end.
- The [examples folder](https://github.com/getludic/ludic/tree/main/examples) has runnable end-to-end htmx apps — click-to-edit, infinite scroll, lazy loading, bulk update, FastAPI integration.
- Starlette's docs apply to everything `LudicApp` doesn't override — middleware, lifespan, exception handlers all behave normally.
