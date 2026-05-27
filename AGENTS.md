# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Ludic is a Python framework for building HTML pages with a typed, React-like component model designed to pair with htmx. v1.x targets Python 3.14+ and uses **t-strings** (PEP 750 template strings) rather than f-strings for templating — code mixing HTML elements with interpolated text is written `t"Hello {b('World')}"`, not `f"..."`.

## Requirements

Python **3.14+** is mandatory for the 1.x stream (t-string support). The legacy 0.5.x line on Python 3.12/3.13 uses f-strings — do not mix that style into v1.x code.

## Release streams and backporting

The project maintains two parallel streams on GitHub:

- **1.x** — Python 3.14+, uses t-strings. Lives on the `main` branch.
- **0.5.x** — Python 3.12+ (3.12/3.13), uses f-strings + `FormatContext`. Lives on the `0.5.x` branch.

When opening a PR against `main`, you usually also need to **backport the change to the `0.5.x` branch**. The backport must translate any `t"..."` templates back to the f-string style used in 0.5.x. Bug fixes and non–t-string-specific features should land in both streams; features that depend on Python 3.14 (t-strings, newer typing) are 1.x-only.

## Common commands

Prefer `uv` for running commands in this repo. It pins Python 3.14 and resolves the optional extras without needing a hand-managed venv:

```bash
uv run --python 3.14 --with ".[full,test]" pytest
uv run --python 3.14 --with ".[full,test]" pytest tests/test_components.py::test_name
uv run --python 3.14 --with ".[full,test]" mypy ludic
```

Install for development (editable, with all extras):

```bash
python -m pip install -e ".[full,test]"
```

Or use the Hatch env (uses Python 3.14, installs `dev`, `full`, `django`, `test`):

```bash
hatch shell
```

Run tests / single test / coverage:

```bash
pytest
pytest tests/test_components.py::test_name
pytest --cov=ludic
```

Lint and type-check:

```bash
ruff check .
ruff format .
mypy ludic   # uses the in-tree plugin at ludic/mypy_plugin.py
```

Docs (MkDocs Material):

```bash
mkdocs serve
```

Pre-commit hooks are expected before submitting:

```bash
pre-commit install --install-hooks
```

## Architecture

The library is organized around a single rendering pipeline; understanding these layers is necessary to make non-trivial changes.

### Core rendering layer (`ludic/`)

- `base.py` — `BaseElement`, the metaclass-driven root of every node. Its `__init__` walks `*children`, detects t-string `Template` instances, and expands them via `process_template` from `format.py`. `to_html()` / `_format_attributes` / `_format_children` produce the final HTML string.
- `format.py` — t-string processing, attribute formatting (key aliasing, style dicts, class lists), HTML escaping, and the trusted/untrusted content boundary. Most security-relevant logic lives here.
- `elements.py` — generic `Element` / `ElementStrict` / `Blank` wrappers used to build the typed HTML element classes.
- `html.py` — concrete HTML element classes (`div`, `a`, `html`, `head`, `body`, ...). Element-specific child/attribute typing is declared here and enforced by mypy via the plugin.
- `attrs.py` — `Attrs`, `GlobalAttrs`, `NoAttrs`, and per-element TypedDicts describing allowed HTML attributes.
- `components.py` — `Component[TChildren, TAttrs]`, `ComponentStrict[*TChildrenArgs, TAttrs]`, `Block`, `Inline`. Subclasses implement `render()` and may declare `classes` and `styles`. A global `COMPONENT_REGISTRY` collects every subclass at definition time (used by the style collector).
- `types.py`, `utils.py` — the generic type aliases (`AnyChildren`, `TAttrs`, etc.) and reflection helpers used by both the runtime and the mypy plugin.
- `mypy_plugin.py` — declared in `pyproject.toml` as `plugins = "ludic/mypy_plugin.py"`. It synthesizes `__init__` signatures for `Component` / `ComponentStrict` / `web.endpoints.Endpoint` so that children and attrs are type-checked at call sites. Changes to component generics typically require touching this plugin.

### Styling (`ludic/styles/`)

`Theme`, `get_default_theme`, style collection (`collect.py`), and Pygments-based syntax highlighting (`highlight.py`). Components read the theme via `self.theme`, which falls back to the default when no theme is set in the context dict propagated down the tree by `_format_children`.

### Component catalog (`ludic/catalog/`)

Higher-level, opinionated components (layouts, forms, tables, navigation, typography, ...) built on top of the core. Treat this as reference implementations and as the main consumer of the public API — when changing core types, run the catalog and its tests to catch fallout.

### Web integration (`ludic/web/`)

Thin Starlette wrapper: `LudicApp`, `routing`, `endpoints` (the `Endpoint` class is also special-cased by the mypy plugin), `responses`, `parsers`, `requests`, `datastructures`. Optional — the core has no Starlette dependency.

### Framework contrib (`ludic/contrib/`)

`django/` and `fastapi/` integrations. Each is gated behind its own optional extra in `pyproject.toml` (`[django]`, `[fastapi]`).

### Examples (`examples/`)

Each file is a runnable htmx pattern (click-to-edit, infinite scroll, lazy loading, FastAPI integration, ...). `tests/test_examples.py` imports and exercises these, so breaking an example breaks CI.

## Conventions worth knowing

- Ruff config in `pyproject.toml` selects bandit (`S`), bugbear (`B`), pyupgrade (`UP`), pydocstyle D2, and complexity (`C901`); target is `py314`. `ludic` is treated as first-party and `examples` as third-party for isort.
- mypy runs in `strict` mode with `disallow_subclassing_any = false` and `disable_error_code = ["misc"]`. The plugin is load-bearing — running mypy without it will produce false positives on every component.
- Tests live under `tests/` and mirror the package layout. `tests/test_examples.py` covers `examples/`. Coverage paths remap `examples/` onto `ludic/` (see `[tool.coverage.paths]`).
- The version is derived from VCS via `hatch-vcs` and written to `_version.py` at build time — do not edit `_version.py` by hand.
