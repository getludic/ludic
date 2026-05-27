---
name: ludic-web
description: >-
  Build web apps with Ludic's web integration — Starlette-based LudicApp,
  typed Endpoint classes, and the FastAPI / Django integrations. Use this
  skill whenever the user is wiring Ludic components into HTTP handlers:
  routing requests with LudicApp, declaring async endpoints that return
  components, subclassing ludic.web.endpoints.Endpoint, parsing form data
  or query params, returning htmx partials, handling redirects, mounting
  Ludic inside an existing FastAPI or Django app, or generating URLs from
  a request (request.url_for / request.url_path_for). Always trigger this
  skill on any code that generates absolute URLs from request data — there
  is a host header poisoning class of vulnerability that affects every
  Ludic web app and needs explicit guarding. Also trigger on questions
  about LudicRequest, LudicResponse, the Starlette/FastAPI/Django bridge,
  or htmx response patterns (HX-Trigger, HX-Redirect, HX-Push-Url
  headers). For pure component authoring without an HTTP layer, use the
  companion `ludic-components` skill.
metadata:
  type: framework-guide
  framework: ludic
  version: "1.x"
---

# Ludic Web

This skill covers the **web integration** side of Ludic — how to serve components over HTTP. The component authoring side (writing `Component` subclasses, t-strings, the catalog, the `Safe` boundary) is covered in the companion `ludic-components` skill.

Ludic's web layer is a thin wrapper around [Starlette](https://www.starlette.io/). The same patterns work in FastAPI and Django via the optional integrations in `ludic.contrib`.

## The basic shape

```python
from ludic.web import LudicApp
from ludic.html import b, p

app = LudicApp()

@app.get("/")
async def homepage() -> p:
    return p(t"Hello {b('Stranger')}!")
```

What's happening:

- `LudicApp` is a Starlette `Starlette` subclass that knows how to serialize a returned `BaseElement` into an HTML response (correct content-type, full document if it's a `<html>` root, otherwise a fragment suitable for htmx).
- The return type annotation (`-> p`) is real — the mypy plugin checks it against the component you actually return.
- Async is the default. Sync handlers are accepted too.

Run it with any ASGI server:

```bash
uvicorn web:app
```

## Endpoints as classes

For anything beyond trivial GETs, prefer the `Endpoint` class — it groups verbs for a single resource and gets the same type-checking treatment as components:

```python
from ludic.web import LudicApp
from ludic.web.endpoints import Endpoint
from ludic.web.parsers import Parser

app = LudicApp()

@app.endpoint("/items/{id:int}")
class Item(Endpoint[ItemAttrs]):
    async def get(self) -> ItemView: ...
    async def put(self, data: Parser[ItemAttrs]) -> ItemView: ...
    async def delete(self) -> None: ...
```

`Parser[SomeAttrs]` validates an incoming form/JSON body against the same TypedDict you'd use for component attrs — one schema, two uses.

## htmx response patterns

When an endpoint is called by htmx, return the swap target as a Ludic element — htmx will replace the target on the page:

```python
@app.post("/items")
async def create_item(request: Request, data: Parser[ItemAttrs]) -> ItemRow:
    item = await db.insert(data.attrs)
    return ItemRow(item)  # htmx swaps this into hx-target
```

For htmx control headers (`HX-Trigger`, `HX-Redirect`, `HX-Push-Url`, ...), set them on the response:

```python
from ludic.web.responses import LudicResponse

resp = LudicResponse(MyComponent(...))
resp.headers["HX-Push-Url"] = "/items/123"
return resp
```

## Generating URLs — beware host header poisoning

`Request.url_for(...)` returns an absolute URL whose scheme and host are derived from the incoming request — ultimately from the HTTP `Host` header (and `X-Forwarded-*` headers when proxy headers are trusted). If your app accepts requests with an untrusted `Host`, an attacker can poison every absolute URL you render — including `hx-get` / `hx-post` attributes, links, redirects, and links sent in outbound messages — pointing the browser at an attacker-controlled domain.

**Mitigations:**

- **Prefer `request.url_path_for(...)`** — or `request.url_for(...).path` — for in-app links and htmx attributes. Relative paths cannot be poisoned and are usually what you want anyway.
- **Install `starlette.middleware.trustedhost.TrustedHostMiddleware`** with an explicit `allowed_hosts` list so the app rejects requests with a forged `Host` header before any handler runs.
- **Behind a reverse proxy or CDN**, configure `ProxyHeadersMiddleware` (or an equivalent) with a trusted-proxy allowlist so `X-Forwarded-Host` / `X-Forwarded-Proto` are only honored from your own infrastructure.

FastAPI users get the same exposure: the FastAPI integration wraps the incoming request as `LudicRequest`, so `Request.url_for(...)` is reachable from FastAPI handlers and the same advice applies.

```python
# good — relative path, can't be poisoned
a("Profile", href=request.url_path_for("profile", user_id=user.id))

button(
    "Refresh",
    hx_get=request.url_path_for("items_partial"),
    hx_target="#items",
)

# avoid for in-app links — host comes from the request
a("Profile", href=str(request.url_for("profile", user_id=user.id)))
```

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

## Parsers, requests, responses

`ludic.web` re-exports / wraps the Starlette pieces you actually need:

- `LudicRequest` — Starlette `Request` with a couple of Ludic conveniences.
- `LudicResponse` — used for explicit response construction (custom headers, status codes).
- `parsers.Parser[TAttrs]` — validates form / JSON / query bodies against a TypedDict and exposes them as `.attrs`.
- `datastructures.FormData`, `QueryParams` — same shapes Starlette uses.
- `routing.Route`, `Mount` — for declaring routes outside the `@app.get(...)` decorators.

## FastAPI integration

```python
from fastapi import FastAPI
from ludic.contrib.fastapi import LudicRoute

app = FastAPI()
app.router.route_class = LudicRoute  # makes returns of Ludic elements render as HTML

@app.get("/", response_class=LudicResponse)
async def home() -> p:
    return p("Hello from FastAPI + Ludic")
```

The `[fastapi]` extra installs the dependency: `pip install "ludic[fastapi]"`. The host-header poisoning advice above applies identically here.

## Django integration

```python
# urls.py
from ludic.contrib.django import LudicView
from .views import HomeView

urlpatterns = [path("", LudicView.as_view(component=HomeView))]
```

The `[django]` extra: `pip install "ludic[django]"`. The Django integration goes through Django's URL resolver and request/response cycle, not Starlette's — so the relevant host-header guard is Django's `ALLOWED_HOSTS` setting and (when proxied) `USE_X_FORWARDED_HOST` / `SECURE_PROXY_SSL_HEADER`. Same threat, framework-native mitigation.

## Endpoint testing

```python
from starlette.testclient import TestClient

def test_homepage():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "Hello" in r.text
```

Because the response body is rendered HTML, you can assert against substrings directly or parse it with whatever HTML library you prefer.

## When in doubt

- The [Ludic web framework docs](https://getludic.dev/docs/web-framework) cover routing, parsers, and responses end-to-end.
- The [examples folder](https://github.com/getludic/ludic/tree/main/examples) has runnable end-to-end htmx apps — click-to-edit, infinite scroll, lazy loading, file upload, FastAPI integration.
- Starlette's docs apply to everything `LudicApp` doesn't override — middleware, lifespan, exception handlers all behave normally.
