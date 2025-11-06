from ludic.catalog.typography import Link, Paragraph
from ludic.format import format_attr_value, format_attrs
from ludic.html import b, div, i, p, strong


def test_format_attr_value() -> None:
    assert format_attr_value("foo", "bar") == "bar"
    assert format_attr_value("foo", "bar", is_html=True) == "bar"

    assert format_attr_value("foo", 1) == "1"
    assert format_attr_value("foo", 1, is_html=True) == "1"

    assert format_attr_value("foo", True) == "true"
    assert format_attr_value("foo", True, is_html=True) == "foo"

    assert format_attr_value("foo", False) == "false"
    assert format_attr_value("foo", False, is_html=True) == ""

    assert format_attr_value("hx-confirm", True) == "true"
    assert format_attr_value("hx-confirm", True, is_html=True) == "true"

    assert format_attr_value("hx-confirm", False) == "false"
    assert format_attr_value("hx-confirm", False, is_html=True) == "false"

    assert (
        format_attr_value("style", {"color": "red", "background": "blue"})
        == "color:red;background:blue"
    )


def test_template_processing() -> None:
    # With Python 3.14+, t-strings are processed into tuples of parts
    # Example: t"test {b("foo")} {i("bar")}" becomes ("test ", b("foo"), " ", i("bar"))
    assert div(t"test {b('foo')} {i('bar')}") == div("test ", b("foo"), " ", i("bar"))


def test_tstring_in_elements() -> None:
    # Simple t-string with elements
    text = t"test {b('baz')} {i('foo')}"
    assert div(text) == div("test ", b("baz"), " ", i("foo"))

    # Nested t-strings
    assert div(t"test {div(t'foo {b("nested")}, {i("nested2")}')}") == div(
        "test ",
        div("foo ", b("nested"), ", ", i("nested2")),
    )


def test_component_with_tstring() -> None:
    paragraph = Paragraph(
        t"Hello, how {strong('are you')}? Click {Link('here', to='https://example.com')}.",
    )
    assert len(paragraph.children) == 5
    assert isinstance(paragraph.children[3], Link)
    assert paragraph.children[3].attrs["to"] == "https://example.com"
    assert paragraph.to_string(pretty=False) == (
        "<Paragraph>"
          'Hello, how <strong>are you</strong>? '
          'Click <Link to="https://example.com">here</Link>.'
        "</Paragraph>"
    )  # fmt: skip
    assert paragraph.to_html() == (
        "<p>"
        "Hello, how <strong>are you</strong>? Click "
        '<a href="https://example.com" target="_blank">here</a>.'
        "</p>"
    )


def test_escaping_works() -> None:
    """Test that HTML escaping works correctly with t-strings."""
    link = '<a href="https://example.com">test</a>'
    dom = p(t"Hello, how <b>are you</b>? Click {link}.")
    assert dom.to_html() == (
        "<p>Hello, how &lt;b&gt;are you&lt;/b&gt;? "
        'Click &lt;a href="https://example.com"&gt;test&lt;/a&gt;.</p>'
    )


def test_quotes_not_escaped() -> None:
    dom = p("It's alive <3.")
    assert dom.to_html() == "<p>It's alive &lt;3.</p>"


def test_attributes() -> None:
    assert format_attrs({"checked": False}, is_html=True) == {}
    assert format_attrs({"checked": True}, is_html=True) == {"checked": "checked"}

    assert format_attrs({"on_click": "test"}) == {"onclick": "test"}
    assert format_attrs({"hx_boost": True}) == {"hx-boost": "true"}
    assert format_attrs({"for_": "value"}) == {"for": "value"}
    assert format_attrs({"class_": "a b c"}) == {"class": "a b c"}
    assert format_attrs({"class_": "a b c", "classes": ["more", "classes"]}) == {
        "class": "a b c more classes"
    }

    assert format_attrs(
        {
            "hx_on_htmx_before_request": "alert('test')",
            "hx_on__after_request": "alert('test2')",
        }
    ) == {
        "hx-on-htmx-before-request": "alert('test')",
        "hx-on--after-request": "alert('test2')",
    }
    assert format_attrs(
        {"hx-on:htmx:before-request": "alert('Making a request!')"}
    ) == {"hx-on:htmx:before-request": "alert('Making a request!')"}


def test_raw_attrs() -> None:
    """Test that raw attrs are not converted (for libraries like Datastar)."""
    # Basic raw attrs without conversion
    assert format_attrs({"attrs": {"data_store": "value"}}) == {"data_store": "value"}
    assert format_attrs({"attrs": {"data-store_foo": "bar"}}) == {
        "data-store_foo": "bar"
    }

    # Combination of regular and raw attrs
    assert format_attrs({"class_": "test", "attrs": {"data_store": "value"}}) == {
        "class": "test",
        "data_store": "value",
    }

    # Multiple raw attrs
    assert format_attrs(
        {"attrs": {"data_store": "value", "data-signal_test": "signal"}}
    ) == {"data_store": "value", "data-signal_test": "signal"}

    # Raw attrs with dataset attrs
    assert format_attrs(
        {"dataset": {"foo": "bar"}, "attrs": {"data_store": "value"}}
    ) == {"data-foo": "bar", "data_store": "value"}

    # Raw attrs should still format boolean values
    assert format_attrs({"attrs": {"data_store": True}}) == {"data_store": "true"}
    assert format_attrs({"attrs": {"data_store": True}}, is_html=True) == {
        "data_store": "data_store"
    }

    # Raw attrs should handle different value types
    assert format_attrs({"attrs": {"data_count": 42}}) == {"data_count": "42"}
    assert format_attrs({"attrs": {"data_items": ["a", "b", "c"]}}) == {
        "data_items": "a b c"
    }
