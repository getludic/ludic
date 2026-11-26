#!/usr/bin/env bash
# Workspace: a project on Ludic 1.x with a page that has a sidebar.
set -euo pipefail

cat > pyproject.toml <<'EOF'
[project]
name = "acme-web"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = ["ludic[full]>=1.1.2,<2"]
EOF

cat > app.py <<'EOF'
from ludic.catalog.headers import H1
from ludic.catalog.layouts import Box, Sidebar, Stack, WithSidebar
from ludic.catalog.navigation import Navigation, NavItem
from ludic.catalog.pages import Body, Head, HtmlPage
from ludic.catalog.typography import Paragraph
from ludic.web import LudicApp

app = LudicApp()


@app.get("/")
async def index() -> HtmlPage:
    return HtmlPage(
        Head(title="Acme"),
        Body(
            WithSidebar(
                Sidebar(
                    Navigation(
                        NavItem("Home", to="/"),
                        NavItem("Reports", to="/reports"),
                    )
                ),
                Box(Stack(H1("Dashboard"), Paragraph("Welcome back."))),
            ),
            htmx_version="2.0.4",
        ),
    )
EOF
