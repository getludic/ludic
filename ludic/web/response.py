from starlette.responses import HTMLResponse

from ludic.types import BaseElement


class LudicResponse(HTMLResponse):
    """Response class for PyMX components."""

    def render(self, content: BaseElement) -> bytes:
        return content.to_html().encode("utf-8")
