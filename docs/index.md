# Introduction

Ludic is a lightweight framework for building HTML pages with component approach similar to [React](https://react.dev/). It is built to be used together with [htmx.org](https://htmx.org/) so that developers don't need to write almost any JavaScript to create dynamic web services. It's potential can be leveraged together with its web framework which is a wrapper around powerful [Starlette](https://www.starlette.io/) framework. It is built with the latest Python 3.12 features heavily incorporating typing.

## Features

- Seamless **&lt;/&gt; htmx** integration for rapid web development in **pure Python**
- **React**-like component approach with standard Python type hints
- Uses the power of **Starlette** and **Async** for high-performance web development
- Build HTML with the ease and power of Python **f-strings**

## Example

```python
from ludic.html import b, p
from ludic.web import LudicApp

app = LudicApp()

@app.get("/")
async def homepage() -> div:
    return p(f"Hello {b("world")}!", id="greetings")
```

## Requirements

Python 3.12+

## Installation

```
pip install ludic[web]
```

As similar for Starlette, you'll also want to install an [ASGI](https://asgi.readthedocs.io/en/latest/) server:

```
pip install uvicorn
```
