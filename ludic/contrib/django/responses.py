from typing import Any

from django.http import HttpResponse

from ludic.types import AnyChildren


class LudicResponse(HttpResponse):
    """Class representing Ludic response for Django View.

    Usage:

        from django.http import HttpRequest

        from ludic.html import p
        from ludic.contrib.django import LudicResponse

        def index(request: HttpRequest) -> LudicResponse:
            return LudicResponse(p("Hello, World!"))

    """

    def __init__(self, content: AnyChildren = "", *args: Any, **kwargs: Any) -> None:
        super().__init__(str(content), *args, **kwargs)
