from starlette.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
    StreamingResponse,
)

from ludic.types import BaseElement

__all__ = (
    "LudicResponse",
    "Response",
    "HTMLResponse",
    "JSONResponse",
    "PlainTextResponse",
    "FileResponse",
    "StreamingResponse",
    "RedirectResponse",
)


class LudicResponse(HTMLResponse):
    """Response class for Ludic components."""

    def render(self, content: BaseElement) -> bytes:
        return content.to_html().encode("utf-8")
