import functools
import inspect
from collections.abc import Callable, Coroutine
from typing import Any, ParamSpec, get_args, get_origin

from fastapi import Request
from fastapi._compat import lenient_issubclass
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.dependencies.utils import get_typed_return_annotation
from fastapi.routing import APIRoute
from starlette._utils import is_async_callable
from starlette.responses import Response
from starlette.routing import get_name

from ludic.base import BaseElement
from ludic.web.requests import Request as LudicRequest
from ludic.web.responses import LudicResponse, run_in_threadpool_safe

P = ParamSpec("P")


def is_base_element(type_: type[Any]) -> bool:
    """Check if type is ludic's BaseElement"""
    if get_args(type_) and lenient_issubclass(get_origin(type_), BaseElement):
        return True
    return lenient_issubclass(type_, BaseElement)


def function_wrapper(
    handler: Callable[..., Any], status_code: int = 200
) -> Callable[P, Any]:
    """Wraps endpoints to ensure responses are formatted as LudicResponse objects.

    This function determines whether the handler is asynchronous or synchronous and
    executes it accordingly. If the handler returns a BaseElement instance, it wraps
    the response in a LudicResponse object.

    Args:
        handler (Callable[..., Any]): The FastAPI endpoint handler function.
        status_code (int, optional): The HTTP status code for the response.
            Defaults to 200.

    Returns:
        Callable[P, Any]: A wrapped function that ensures proper response handling.
    """

    @functools.wraps(handler)
    async def wrapped_endpoint(*args: P.args, **kwargs: P.kwargs) -> Any:
        if is_async_callable(handler):
            with BaseElement.formatter:
                raw_response = await handler(*args, **kwargs)
        else:
            raw_response = await run_in_threadpool_safe(handler, *args, **kwargs)

        if isinstance(raw_response, BaseElement):
            return LudicResponse(raw_response, status_code=status_code)
        return raw_response

    return wrapped_endpoint


class LudicRoute(APIRoute):
    """Custom Route class for FastAPI that integrates Ludic framework response handling.

    This class ensures that endpoints returning `BaseElement` instances are properly
    wrapped in `LudicResponse`. If a response model is not explicitly provided, it
    infers the return type annotation from the endpoint function.

    Args:
        path (str): The API route path.
        endpoint (Callable[..., Any]): The FastAPI endpoint function.
        response_model (Any, optional): The response model for OpenAPI documentation.
            Defaults to None.
        name (str | None, optional): The route name. Defaults to None.
        status_code (int | None, optional): The HTTP status code. Defaults to None.
        **kwargs (Any): Additional parameters for APIRoute.
    """

    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = Default(None),  # noqa
        name: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        if isinstance(response_model, DefaultPlaceholder):
            return_annotation = get_typed_return_annotation(endpoint)
            if is_base_element(return_annotation) or lenient_issubclass(
                return_annotation, Response
            ):
                response_model = None
            else:
                response_model = return_annotation

        name = get_name(endpoint) if name is None else name
        wrapped_route = endpoint

        if inspect.isfunction(endpoint) or inspect.ismethod(endpoint):
            wrapped_route = function_wrapper(endpoint, status_code=status_code or 200)
        if getattr(endpoint, "route", None) is None:
            endpoint.route = self  # type: ignore

        super().__init__(
            path, wrapped_route, response_model=response_model, name=name, **kwargs
        )

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = LudicRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler
