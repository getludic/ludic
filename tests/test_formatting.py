from typing import Any, override

import pytest

from ludic import Blank, Component, NoAttrs
from ludic.base import BaseElement
from ludic.catalog.typography import Link, Paragraph
from ludic.format import FormatContext, format_attr_value, format_attrs
from ludic.html import b, div, i, p, strong, style
from ludic.styles.themes import DarkTheme
from ludic.types import NoChildren, Safe


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


def test_format_context() -> None:
    with FormatContext("test_context") as ctx:
        first = ctx.append("foo")
        second = ctx.append({"bar": "baz"})
        extracts = ctx.extract(f"test {first} {second}")

    assert extracts == ("test ", "foo", " ", {"bar": "baz"})


def test_format_context_in_elements() -> None:
    context = BaseElement.formatter
    assert context.get() == {}

    with context:
        f"test {b("foo")} {i("bar")}"
        assert list(context.get().values()) == [b("foo"), i("bar")]

    assert context.get() == {}

    with context:
        text = f"test {b("baz")} {i("foo")}"
        assert div(text) == div("test ", b("baz"), " ", i("foo"))
        assert div(f"test {div(f"foo {b("nested")}, {i("nested2")}")}") == div(
            "test ",
            div("foo ", b("nested"), ", ", i("nested2")),
        )

    assert context.get() == {}


def test_component_with_f_string() -> None:
    paragraph = Paragraph(
        f"Hello, how {strong("are you")}? Click {Link("here", to="https://example.com")}.",
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
    link = '<a href="https://example.com">test</a>'
    dom = p(f"Hello, how <b>are you</b>? Click {link}.")
    assert dom.to_html() == (
        "<p>Hello, how &lt;b&gt;are you&lt;/b&gt;? "
        'Click &lt;a href="https://example.com"&gt;test&lt;/a&gt;.</p>'
    )


def test_quotes_not_escaped() -> None:
    dom = p("It's alive <3.")
    assert dom.to_html() == "<p>It's alive &lt;3.</p>"


class Markup:
    """An object that is not a string and renders as HTML markup."""

    def __str__(self) -> str:
        return "<b>&</b>"


def test_non_string_children_are_escaped() -> None:
    child: Any = Markup()
    assert div(child).to_html() == "<div>&lt;b&gt;&amp;&lt;/b&gt;</div>"
    assert p(f"Error: {child}").to_html() == ("<p>Error: &lt;b&gt;&amp;&lt;/b&gt;</p>")

    error: Any = ValueError("invalid value '<script>alert(1)</script>'")
    assert p(error).to_html() == (
        "<p>invalid value '&lt;script&gt;alert(1)&lt;/script&gt;'</p>"
    )

    assert div(1, " ", 2.5, " ", True).to_html() == "<div>1 2.5 True</div>"
    assert div(Safe("<b>&</b>")).to_html() == "<div><b>&</b></div>"


def test_blank_children_are_escaped() -> None:
    payload = "<script>alert(1)</script>"
    escaped = "&lt;script&gt;alert(1)&lt;/script&gt;"

    assert Blank(payload).to_html() == escaped
    assert div(Blank(payload)).to_html() == f"<div>{escaped}</div>"
    assert Blank(f"Hi {payload} {b('there')}").to_html() == (
        f"Hi {escaped} <b>there</b>"
    )
    assert Blank(Safe("<b>&</b>"), 1, b("x")).to_html() == "<b>&</b>1<b>x</b>"


class ThemeName(Component[NoChildren, NoAttrs]):
    @override
    def render(self) -> i:
        return i(self.theme.name)


def test_blank_passes_theme_to_children() -> None:
    dom = DarkTheme().use(Blank(ThemeName()))
    assert dom.to_html() == "<i>dark</i>"


def test_non_string_attribute_values_are_escaped() -> None:
    escaped = "&lt;b&gt;&amp;&lt;/b&gt;"
    assert format_attr_value("title", Markup(), is_html=True) == escaped
    assert format_attr_value("title", Markup()) == "<b>&</b>"
    assert format_attr_value("title", Safe("<b>&</b>"), is_html=True) == "<b>&</b>"
    assert format_attr_value("tabindex", 0, is_html=True) == "0"
    assert format_attr_value("title", "", is_html=True) == ""


class TrustedMarkup:
    """An object that is not a string and implements the ``__html__`` protocol."""

    def __html__(self) -> str:
        return "<b>&amp;</b>"


class TrustedString(str):
    """A string implementing ``__html__`` the way ``markupsafe.Markup`` does."""

    def __html__(self) -> str:
        return str(self)


def test_html_protocol_children_are_not_escaped() -> None:
    child: Any = TrustedMarkup()
    assert div(child).to_html() == "<div><b>&amp;</b></div>"
    assert div(TrustedString("<i>x</i>")).to_html() == "<div><i>x</i></div>"

    # an f-string turns the value into plain text, the same way it does with Safe
    assert p(f"Total: {TrustedString('<i>x</i>')}").to_html() == (
        "<p>Total: &lt;i&gt;x&lt;/i&gt;</p>"
    )
    assert p(f"Total: {Safe('<i>x</i>')}").to_html() == (
        "<p>Total: &lt;i&gt;x&lt;/i&gt;</p>"
    )


def test_safe_implements_html_protocol() -> None:
    assert Safe("<b>&</b>").__html__() == "<b>&</b>"


def test_escape_flag_without_html_protocol() -> None:
    class Raw:
        escape = False

        def __str__(self) -> str:
            return "<b>&</b>"

    child: Any = Raw()
    assert div(child).to_html() == "<div><b>&</b></div>"


def test_html_protocol_does_not_apply_to_attribute_values() -> None:
    value = TrustedString("<b>&</b>")
    assert format_attr_value("title", value, is_html=True) == (
        "&lt;b&gt;&amp;&lt;/b&gt;"
    )
    assert div("x", title=value).to_html() == (
        '<div title="&lt;b&gt;&amp;&lt;/b&gt;">x</div>'
    )


def test_attribute_value_cannot_break_out_of_quotes() -> None:
    payload = "x\" ' autofocus onfocus=alert(1) y='"
    escaped = "x&quot; ' autofocus onfocus=alert(1) y='"

    assert div("x", title=payload).to_html() == f'<div title="{escaped}">x</div>'
    assert div("x", classes=[payload]).to_html() == f'<div class="{escaped}">x</div>'
    assert div("x", style={"color": payload}).to_html() == (
        f'<div style="color:{escaped}">x</div>'
    )
    assert div("x", dataset={"key": payload}).to_html() == (
        f'<div data-key="{escaped}">x</div>'
    )
    assert div("x", attrs={"data_key": payload}).to_html() == (
        f'<div data_key="{escaped}">x</div>'
    )
    assert div("x", title=Safe(payload)).to_html() == (
        f'<div title="{escaped}">x</div>'
    )
    assert style("a{}", media=payload).to_html() == (
        f'<style media="{escaped}">\na{{}}\n</style>'
    )


def test_attribute_value_with_double_quotes() -> None:
    dom = div("x", hx_vals='{"name": "O\'Brien"}')
    assert dom.to_html() == (
        '<div hx-vals="{&quot;name&quot;: &quot;O\'Brien&quot;}">x</div>'
    )
    assert dom.to_string(pretty=False) == dom.to_html()


def test_invalid_attribute_name_is_rejected() -> None:
    names = [
        "x onclick",
        "x\tonclick",
        "x\nonclick",
        'x"',
        "x'",
        "x>",
        "x<",
        "x/",
        "x=y",
    ]
    error = "Invalid character .* in attribute name"

    for name in names:
        for attrs in ({name: "v"}, {"attrs": {name: "v"}}, {"dataset": {name: "v"}}):
            with pytest.raises(ValueError, match=error):
                div("x", **attrs).to_html()


def test_special_attribute_names_are_allowed() -> None:
    dom = div(
        "x",
        attrs={
            "@click": "a",
            ":class": "b",
            "x-on:click.prevent": "c",
            "data-on-click__debounce.500ms": "d",
            "_": "e",
        },
    )
    assert dom.to_html() == (
        '<div @click="a" :class="b" x-on:click.prevent="c" '
        'data-on-click__debounce.500ms="d" _="e">x</div>'
    )


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

    # Raw attrs with same key as converted regular attr (concatenation)
    assert format_attrs({"class_": "btn", "attrs": {"class": "extra"}}) == {
        "class": "btn extra"
    }


def test_raw_attrs_validation() -> None:
    """Test that attrs parameter validates type correctly."""
    import pytest

    # Should raise TypeError if attrs is not a dict
    with pytest.raises(
        TypeError, match="The 'attrs' parameter must be a dict, got str"
    ):
        format_attrs({"attrs": "not a dict"})

    with pytest.raises(
        TypeError, match="The 'attrs' parameter must be a dict, got list"
    ):
        format_attrs({"attrs": ["foo", "bar"]})

    with pytest.raises(
        TypeError, match="The 'attrs' parameter must be a dict, got int"
    ):
        format_attrs({"attrs": 123})

    # None should be treated as no attrs (not raise an error)
    # This is handled by the walrus operator check
    assert format_attrs({"attrs": None}) == {}


def test_dataset_attrs_validation() -> None:
    """Test that dataset parameter validates type correctly."""
    import pytest

    # Should raise TypeError if dataset is not a dict
    with pytest.raises(
        TypeError, match="The 'dataset' parameter must be a dict, got str"
    ):
        format_attrs({"dataset": "not a dict"})

    with pytest.raises(
        TypeError, match="The 'dataset' parameter must be a dict, got list"
    ):
        format_attrs({"dataset": ["foo", "bar"]})

    with pytest.raises(
        TypeError, match="The 'dataset' parameter must be a dict, got int"
    ):
        format_attrs({"dataset": 123})

    # None should be treated as no dataset (not raise an error)
    assert format_attrs({"dataset": None}) == {}
