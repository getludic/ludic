import inspect
from collections.abc import Callable
from typing import Any

from starlette.datastructures import FormData, Headers, QueryParams
from starlette.requests import Request


async def extract_from_request(
    handler: Callable[..., Any], request: Request
) -> dict[str, Any]:
    parameters = inspect.signature(handler).parameters
    handler_kwargs: dict[str, Any] = {}

    if all(key in parameters for key in request.path_params):
        handler_kwargs.update(request.path_params)

    for name, param in parameters.items():
        if issubclass(param.annotation, FormData):
            async with request.form() as form:
                handler_kwargs[name] = form
        elif issubclass(param.annotation, QueryParams):
            handler_kwargs[name] = request.query_params
        elif issubclass(param.annotation, Request):
            handler_kwargs[name] = request
        elif issubclass(param.annotation, Headers):
            handler_kwargs[name] = request.headers

    return handler_kwargs
