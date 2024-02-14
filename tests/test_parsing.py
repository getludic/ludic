from ludic.base import Safe
from ludic.catalog.typography import Link, Paragraph
from ludic.html import a, b


def test_parse_simple():
    assert Safe.parse("Hello, World!") == "Hello, World!"
    assert Safe.parse("<b>Hello, World!</b>") == b("Hello, World!")
    assert Safe.parse("<Paragraph>Hello, World!</Paragraph>") == Paragraph(
        "Hello, World!"
    )
    assert Safe.parse('<Link to="/home">Hello, World!</Link>') == Link(
        "Hello, World!", to="/home"
    )
    assert Safe.parse('<a href="/home" class="link">Hello, World!</a>') == a(
        "Hello, World!", href="/home", class_="link"
    )


def test_parse_multiple():
    assert Safe.parse("<Paragraph>Hello, World!</Paragraph>, <b>How Are you?</b>") == (
        Paragraph("Hello, World!"),
        ", ",
        b("How Are you?"),
    )
