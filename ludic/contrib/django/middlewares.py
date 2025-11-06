from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from ludic.base import BaseElement


class LudicMiddleware:
    """Ludic middleware for Django.

    With Python 3.14+ t-strings, this middleware is now optional as it no longer
    needs to manage the FormatContext cache. It's kept for backward compatibility.

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
        response: HttpResponse = self.get_response(request)
        return response
