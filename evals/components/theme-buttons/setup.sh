#!/usr/bin/env bash
# Workspace: a project on Ludic 1.x with a page that uses catalog components.
set -euo pipefail

cat > pyproject.toml <<'EOF'
[project]
name = "acme-docs"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = ["ludic[full]>=1.1.2,<2"]
EOF

cat > app.py <<'EOF'
from ludic.catalog.buttons import Button, ButtonLink
from ludic.catalog.headers import H1
from ludic.catalog.layouts import Cluster, Stack
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.catalog.typography import CodeBlock, Paragraph
from ludic.web import LudicApp

app = LudicApp()


@app.get("/")
async def index() -> HtmlPage:
    return HtmlPage(
        Head(title="Acme Docs"),
        Body(
            Stack(
                H1("Install"),
                Paragraph("Install the client with pip:"),
                CodeBlock("pip install acme-client", language="bash"),
                Cluster(
                    ButtonLink("Read the guide", to="/guide"),
                    Button("Copy API key", type="button"),
                ),
            ),
            htmx_version="2.0.4",
        ),
    )
EOF
