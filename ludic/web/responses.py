import inspect
from collections.abc import Callable
from typing import Any, get_origin

from starlette._utils import is_async_callable
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import FormData, Headers, QueryParams
from starlette.requests import Request
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
from ludic.web.parsers import BaseParser

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


async def prepare_response(
    handler: Callable[..., Any],
    request: Request,
    status_code: int | None = None,
    headers: Headers | None = None,
) -> Response:
    """Prepares response for the given handler and request.

    Args:
        handler: The handler to prepare the response for.
        request: The request to prepare the response for.
        status_code: The status code to use for the response.
        headers: The headers to use for the response.

    Returns:
        The prepared response.
    """
    handler_kw = await extract_from_request(handler, request)
    is_async = is_async_callable(handler)

    if is_async:
        response = await handler(**handler_kw)
    else:
        response = await run_in_threadpool(handler, **handler_kw)

    if isinstance(response, tuple):
        if len(response) == 2:
            response, status_code = response
        elif len(response) == 3:
            response, status_code, headers = response
            headers = Headers(headers)
        else:
            raise ValueError(f"Invalid response tuple: {response}")

    if response is None:
        response = ""

    if isinstance(response, BaseElement):
        response = LudicResponse(
            response, status_code=status_code or 200, headers=headers
        )
    elif isinstance(response, str | bool | int | float):
        response = PlainTextResponse(
            str(response), status_code=status_code or 200, headers=headers
        )

    return response


async def extract_from_request(
    handler: Callable[..., Any], request: Request
) -> dict[str, Any]:
    """Extracts parameters for given handler from the request.

    This function scans the signature of the handler and tries to extract
    the parameters from the request. It passes them to the handler as
    keyword arguments.
    """
    parameters = inspect.signature(handler).parameters
    handler_kwargs: dict[str, Any] = {}

    if all(key in parameters for key in request.path_params):
        handler_kwargs.update(request.path_params)

    for name, param in parameters.items():
        if (origin := get_origin(param.annotation)) is not None and issubclass(
            origin, BaseParser
        ):
            async with request.form() as form:
                handler_kwargs[name] = param.annotation(form)
        elif issubclass(param.annotation, FormData):
            async with request.form() as form:
                handler_kwargs[name] = form
        elif issubclass(param.annotation, QueryParams):
            handler_kwargs[name] = request.query_params
        elif issubclass(param.annotation, Request):
            handler_kwargs[name] = request
        elif issubclass(param.annotation, Headers):
            handler_kwargs[name] = request.headers

    return handler_kwargs


class LudicResponse(HTMLResponse):
    """Response class for Ludic components."""

    def render(self, content: BaseElement) -> bytes:
        return content.to_html().encode("utf-8")
