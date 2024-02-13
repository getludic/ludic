from starlette.responses import HTMLResponse

from ludic.base import AnyElement


class LudicResponse(HTMLResponse):
    """Response class for PyMX components."""

    def render(self, content: AnyElement) -> bytes:
        return content.to_html().encode("utf-8")
