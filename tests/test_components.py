import pytest

from ludic.base import Safe
from ludic.catalog.navigation import Navigation, NavItem
from ludic.catalog.typography import Link, Paragraph
from ludic.html import b, li


def test_link():
    link = Link("A link!", to="https://example.com")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'


def test_invalid_link():
    with pytest.raises(TypeError):
        Link("should not pass")
    with pytest.raises(TypeError):
        Link(to="https://should.not.pass")  # type: ignore


def test_component_with_f_string():
    paragraph = Paragraph(
        Safe(
            f"Hello, how {b("are you")}? Click {Link("here", to="https://example.com")}."
        )
    )
    assert isinstance(paragraph.children[3], Link)
    assert paragraph.children[3].attrs["to"] == "https://example.com"
    assert paragraph.to_string(pretty=False) == (
        "<Paragraph>"
          'Hello, how <b>are you</b>? Click <Link to="https://example.com">here</Link>.'
        "</Paragraph>"
    )  # fmt: skip
    assert paragraph.to_html() == (
        '<p>Hello, how <b>are you</b>? Click <a href="https://example.com">here</a>.</p>'
    )


def test_component_with_invalid_f_string():
    with pytest.raises(TypeError):
        Link(Safe(f"should {b("not pass")}"), to="https://example.com")


def test_navigation():
    navigation = Navigation(
        NavItem("Home", to="/"),
        NavItem("About", to="/about"),
        id="nav",
    )
    assert navigation.to_html() == (
        '<ul class="navigation" id="nav">'
            '<li id="home"><a href="/">Home</a></li>'
            '<li id="about"><a href="/about">About</a></li>'
        "</ul>"
    )  # fmt: skip


def test_invalid_navigation():
    with pytest.raises(TypeError):
        Navigation("should not pass")  # type: ignore
    with pytest.raises(TypeError):
        Navigation(li("Home"), li("About"))  # type: ignore
