import os
from typing import Any

from django.http import HttpRequest
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from ludic.contrib.django import LudicMiddleware, LudicResponse
from ludic.html import p

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.contrib")


def test_django_response() -> None:
    assert LudicResponse(p("test")).content == b"<p>test</p>"


def test_django_does_not_escape_elements() -> None:
    element: Any = p("a & b")
    assert conditional_escape(element) == "<p>a &amp; b</p>"
    assert format_html("<main>{}</main>", p("test")) == "<main><p>test</p></main>"


def test_django_safe_strings_are_not_escaped() -> None:
    assert p(mark_safe("<b>test</b>")).to_html() == "<p><b>test</b></p>"  # noqa: S308
    assert p("<b>test</b>").to_html() == "<p>&lt;b&gt;test&lt;/b&gt;</p>"


def test_django_middleware() -> None:
    get_response_called = False

    def get_response(_: HttpRequest) -> LudicResponse:
        nonlocal get_response_called
        get_response_called = True

        response = LudicResponse(f"{p('does not clean up cache')}")
        return response

    middleware = LudicMiddleware(get_response)
    middleware(HttpRequest())

    assert get_response_called
