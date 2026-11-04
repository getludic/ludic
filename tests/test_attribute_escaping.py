"""Regression tests for attribute-value quote escaping.

An attribute value must never be able to terminate its own quotes. Previously
``_format_attributes`` switched to single-quote wrapping whenever a value
contained a double quote; an apostrophe in that same value then closed the
attribute early, truncating the value and allowing extra attributes (e.g.
event handlers) to be injected.
"""

from html.parser import HTMLParser

from ludic.html import div, p


class _AttrCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.attrs: list[tuple[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.attrs.extend(attrs)


def parse_attrs(html_text: str) -> dict[str, str | None]:
    parser = _AttrCollector()
    parser.feed(html_text)
    return dict(parser.attrs)


def test_value_with_both_quote_kinds_round_trips() -> None:
    """Ordinary prose, no payload: the value must survive a full HTML round trip."""
    value = 'He said "it\'s fine"'
    out = div("hello", title=value).to_html()
    assert out == '<div title="He said &quot;it\'s fine&quot;">hello</div>'
    assert parse_attrs(out) == {"title": value}


def test_value_cannot_inject_new_attributes() -> None:
    """A crafted value must not add event-handler attributes."""
    value = "\"' onmouseover=alert(1) a='"
    out = div("hello", title=value).to_html()
    attrs = parse_attrs(out)
    assert set(attrs) == {"title"}
    assert attrs["title"] == value


def test_double_quote_only_value_is_escaped() -> None:
    assert div("hello", title='say "hi"').to_html() == (
        '<div title="say &quot;hi&quot;">hello</div>'
    )
    assert parse_attrs(div("hello", title='say "hi"').to_html()) == {
        "title": 'say "hi"'
    }


def test_single_quote_value_keeps_existing_output() -> None:
    """Existing HTMX-style values contain apostrophes and must stay unchanged."""
    assert div("x", hx_on__before_request="alert('Making a request!')").to_html() == (
        '<div hx-on--before-request="alert(\'Making a request!\')">x</div>'
    )


def test_ampersand_is_not_double_escaped() -> None:
    """Escaping quotes here must not re-escape entities produced upstream."""
    assert div("x", title='a & b "c"').to_html() == (
        '<div title="a &amp; b &quot;c&quot;">x</div>'
    )


def test_text_content_quotes_are_still_not_escaped() -> None:
    """Text escaping deliberately leaves quotes alone; keep that contract."""
    assert p("It's alive <3.").to_html() == "<p>It's alive &lt;3.</p>"


def test_plain_attributes_are_unchanged() -> None:
    assert div("test", id="div").to_html() == '<div id="div">test</div>'
    assert div("content", data_foo="1").to_html() == (
        '<div data-foo="1">content</div>'
    )
