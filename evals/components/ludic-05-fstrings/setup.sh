#!/usr/bin/env bash
# Workspace: a project on Ludic 0.5 and Python 3.12, which has no t-strings.
set -euo pipefail

cat > pyproject.toml <<'EOF'
[project]
name = "acme-web"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["ludic[full]>=0.5.21,<0.6"]
EOF
echo "3.12" > .python-version
