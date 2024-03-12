import inspect
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar, get_origin

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
from ludic.web import datastructures as ds
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

T = TypeVar("T")
P = ParamSpec("P")


async def run_in_threadpool_safe(
    func: Callable[P, T], *args: P.args, **kwargs: P.kwargs
) -> T:
    def func_wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        with BaseElement.formatter:
            return func(*args, **kwargs)

    response: T = await run_in_threadpool(func_wrapped, *args, **kwargs)
    return response


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
        with BaseElement.formatter:
            raw_response = await handler(**handler_kw)
    else:
        raw_response = await run_in_threadpool_safe(handler, **handler_kw)

    if isinstance(raw_response, tuple):
        if len(raw_response) == 2:
            raw_response, status_or_headers = raw_response
            if isinstance(status_or_headers, dict):
                headers = ds.Headers(status_or_headers)
            else:
                status_code = status_or_headers
        elif len(raw_response) == 3:
            raw_response, status_code, headers = raw_response
            headers = ds.Headers(headers)
        else:
            raise ValueError(f"Invalid response tuple: {raw_response}")

    if raw_response is None:
        raw_response = ""

    response: Response
    if isinstance(raw_response, BaseElement):
        response = LudicResponse(
            raw_response, status_code=status_code or 200, headers=headers
        )
    elif isinstance(raw_response, str | bool | int | float):
        response = PlainTextResponse(
            str(raw_response), status_code=status_code or 200, headers=headers
        )
    elif isinstance(raw_response, Response):
        response = raw_response
    else:
        raise ValueError(f"Invalid response type: {type(raw_response)}")

    return response


async def extract_from_request(
    handler: Callable[..., Any],
    request: Request,
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
