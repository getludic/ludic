#!/usr/bin/env bash
# Workspace: a project on Ludic 1.x with a component that mixes elements into
# f-strings, so the elements are rendered as escaped text.
set -euo pipefail

cat > pyproject.toml <<'EOF'
[project]
name = "acme-web"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = ["ludic[full]>=1.1.2,<2"]
EOF

cat > components.py <<'EOF'
from typing import override

from ludic import Attrs, Component
from ludic.catalog.typography import Link
from ludic.html import b, p
from ludic.types import NoChildren


class WelcomeAttrs(Attrs):
    name: str
    unread: int


class Welcome(Component[NoChildren, WelcomeAttrs]):
    @override
    def render(self) -> p:
        return p(
            f"Welcome back, {b(self.attrs['name'])}! "
            f"You have {self.attrs['unread']} unread messages in your "
            f"{Link('inbox', to='/inbox')}."
        )
EOF
