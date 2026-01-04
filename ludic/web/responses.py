import inspect
from collections.abc import Callable
from types import NoneType, UnionType
from typing import Any, ParamSpec, TypeVar, get_args, get_origin, get_type_hints

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
from starlette.websockets import WebSocket

from ludic.base import BaseElement
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
    """Run a synchronous function in a thread pool.

    With t-strings in Python 3.14, we no longer need the FormatContext
    wrapper, simplifying this function significantly.
    """
    response: T = await run_in_threadpool(func, *args, **kwargs)
    return response


def extract_response_status_headers[T](
    raw_response: T, status_code: int | None = None, headers: Headers | None = None
) -> tuple[T, int | None, Headers | None]:
    """Extracts status code and headers from response if it is a tuple."""
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

    return raw_response, status_code, headers


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
        raw_response = await handler(**handler_kw)
    else:
        raw_response = await run_in_threadpool_safe(handler, **handler_kw)

    raw_response, status_code, headers = extract_response_status_headers(
        raw_response, status_code, headers
    )

    response: Response
    if isinstance(raw_response, BaseElement):
        raw_response.context["request"] = request
        response = LudicResponse(
            raw_response, status_code=status_code or 200, headers=headers
        )
    elif isinstance(raw_response, str | bool | int | float):
        response = PlainTextResponse(
            str(raw_response), status_code=status_code or 200, headers=headers
        )
    elif isinstance(raw_response, Response):
        response = raw_response
    elif raw_response is None:
        response = Response(status_code=204, headers=headers)
    else:
        raise ValueError(f"Invalid response type: {type(raw_response)}")

    return response


async def extract_from_request(  # noqa
    handler: Callable[..., Any],
    request: Request | WebSocket,
) -> dict[str, Any]:
    """Extracts parameters for given handler from the request.

    This function scans the signature of the handler and tries to extract
    the parameters from the request. It passes them to the handler as
    keyword arguments.
    """
    parameters = inspect.signature(handler).parameters
    handler_kwargs: dict[str, Any] = {}
    type_hints = get_type_hints(handler)

    if all(key in parameters for key in request.path_params):
        handler_kwargs.update(request.path_params)

    for name, param in parameters.items():
        annotation = type_hints.get(name, param.annotation)
        # Defensive: skip if annotation is inspect._empty
        if annotation is inspect._empty:
            continue
        try:
            # Defensive: issubclass only if annotation is a class
            if isinstance(request, WebSocket):
                if isinstance(annotation, type) and issubclass(annotation, WebSocket):
                    handler_kwargs[name] = request
            elif (
                (origin := get_origin(annotation)) is not None
                and isinstance(origin, type)
                and issubclass(origin, BaseParser)
            ):
                async with request.form() as form:
                    handler_kwargs[name] = annotation(form)
            elif isinstance(annotation, UnionType):
                args = get_args(annotation)
                # Defensive: Only allow Optional[X] (X | NoneType)
                if not (args and len(args) == 2 and args[1] is NoneType):
                    raise TypeError(
                        f"Request handler has an invalid signature: {annotation!r}"
                    )
                handler_kwargs[name] = request.query_params.get(name)
            elif isinstance(annotation, type) and issubclass(annotation, FormData):
                async with request.form() as form:
                    handler_kwargs[name] = form
            elif isinstance(annotation, type) and issubclass(annotation, Request):
                handler_kwargs[name] = request
            elif isinstance(annotation, type) and issubclass(annotation, QueryParams):
                handler_kwargs[name] = request.query_params
            elif isinstance(annotation, type) and issubclass(annotation, Headers):
                handler_kwargs[name] = request.headers
        except Exception as exc:
            raise TypeError(
                f"Error extracting parameter '{name}' "
                f"with annotation {annotation!r}: {exc}"
            ) from exc

    return handler_kwargs


class LudicResponse(HTMLResponse):
    """Response class for Ludic components."""

    def render(self, content: BaseElement) -> bytes:
        return content.to_html().encode("utf-8")
