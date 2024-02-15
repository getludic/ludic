import pytest

from ludic.base import Safe
from ludic.catalog.typography import Link, Paragraph
from ludic.html import a, b, br, div, p, span, th
from ludic.parsing import parse_element


def test_element_empty():
    assert parse_element("<div></div>") == div()


def test_element_text_only():
    assert parse_element("<span>Some text here</span>") == span("Some text here")


def test_self_closing_element():
    assert parse_element("<div />") == div()


def test_invalid_nesting_of_elements():
    with pytest.raises(TypeError):
        parse_element("<span><div>test</span><div />")


def test_element_with_attributes():
    string = '<div>before <span class="value">content</span> after</div>'
    assert parse_element(string) == div(
        "before ", span("content", class_="value"), " after"
    )


def test_multiple_elements():
    string = "<div><span />Some text<div class='value' />More text</div>"
    assert parse_element(string) == div(
        span(), "Some text", div(class_="value"), "More text"
    )


def test_multiple_pair_elements():
    string = '<div><p />Some text<span id="value">Another text</span>More text</div>'
    assert parse_element(string) == div(
        p(), "Some text", span("Another text", id="value"), "More text"
    )


def test_boolean_attribute():
    assert parse_element('<span popover="">Hello, World!</span>') == span(
        "Hello, World!", popover=True
    )


def test_integer_attribute():
    assert parse_element('<th colspan="2">Hello, World!</th>') == th(
        "Hello, World!", colspan=2
    )


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


def test_parse_nested():
    assert Safe.parse("<div><p>Hello, <b>World!</b></p></div>") == div(
        p("Hello, ", b("World!"))
    )
    assert Safe.parse(
        "<div><p>Hello, <b>World!</b></p><p><b>How are you?</b></p><br />I'm good</div>"
    ) == div(p("Hello, ", b("World!")), p(b("How are you?")), br(), "I'm good")
