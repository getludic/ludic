from ludic.catalog.navigation import Navigation, NavItem
from ludic.catalog.typography import Link, Paragraph
from ludic.html import b


def test_link() -> None:
    link = Link("A link!", to="https://example.com")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'


def test_paragraph() -> None:
    paragraph = Paragraph(
        "Hello, how ",
        b("are you"),
        "? Click ",
        Link("here", to="https://example.com"),
        ".",
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


def test_navigation() -> None:
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
