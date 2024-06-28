import os

from django.http import HttpRequest

from ludic.base import BaseElement
from ludic.contrib.django import LudicMiddleware, LudicResponse
from ludic.html import p

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.contrib")


def test_django_response() -> None:
    assert LudicResponse(p("test")).content == b"<p>test</p>"


def test_django_middleware() -> None:
    get_response_called = False

    def get_response(_: HttpRequest) -> LudicResponse:
        nonlocal get_response_called
        get_response_called = True

        assert len(BaseElement.formatter.get()) == 0
        response = LudicResponse(f"{p("does not clean up cache")}")
        assert len(BaseElement.formatter.get()) == 1
        return response

    middleware = LudicMiddleware(get_response)
    middleware(HttpRequest())

    assert get_response_called
    assert len(BaseElement.formatter.get()) == 0
