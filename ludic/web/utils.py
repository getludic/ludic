import inspect
from collections.abc import Callable
from typing import Any, get_origin

from starlette.datastructures import FormData, Headers, QueryParams
from starlette.requests import Request

from ludic.web.parsers import BaseParser


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
                validator = param.annotation(form)
                validator._load_parsers()
                handler_kwargs[name] = validator
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
