from starlette.responses import HTMLResponse

from ..elements.base import AnyElement


class PyMXResponse(HTMLResponse):
    """Response class for PyMX components."""

    def render(self, content: AnyElement) -> bytes:
        return content.to_html().encode("utf-8")
