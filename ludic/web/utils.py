import inspect
from collections.abc import Callable
from typing import Any, get_origin

from starlette.datastructures import FormData, Headers, QueryParams
from starlette.requests import Request

from ludic.web.parsers import Parser


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
        if (
            get_origin(param.annotation) is not None
            and issubclass(get_origin(param.annotation), Parser)
        ) or issubclass(param.annotation, FormData):
            async with request.form() as form:
                if isinstance(param.annotation, FormData):
                    handler_kwargs[name] = form
                else:
                    handler_kwargs[name] = param.annotation(form)
                    handler_kwargs[name].__post_init__()
        elif issubclass(param.annotation, QueryParams):
            handler_kwargs[name] = request.query_params
        elif issubclass(param.annotation, Request):
            handler_kwargs[name] = request
        elif issubclass(param.annotation, Headers):
            handler_kwargs[name] = request.headers

    return handler_kwargs
