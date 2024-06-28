from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from ludic.base import BaseElement


class LudicMiddleware:
    """Ludic middleware for Django to clean up the cache for f-strings.

    Usage:

        # somewhere in django settings.py

        MIDDLEWARES = [
            "...",
            "ludic.contrib.django.LudicMiddleware",
        ]
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        with BaseElement.formatter:
            response: HttpResponse = self.get_response(request)

        return response
