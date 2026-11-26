#!/usr/bin/env bash
# Workspace: a project on Ludic 1.x and Python 3.14.
set -euo pipefail

cat > pyproject.toml <<'EOF'
[project]
name = "acme-web"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = ["ludic[full]>=1.1.2,<2"]
EOF
