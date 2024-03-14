from ludic.catalog.typography import Link, Paragraph
from ludic.format import FormatContext, format_attr_value
from ludic.html import b, div, i, p, strong
from ludic.types import BaseElement


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

    assert extracts == ["test ", "foo", " ", {"bar": "baz"}]


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
    assert isinstance(paragraph.children[3], Link)
    assert paragraph.children[3].attrs["to"] == "https://example.com"
    assert paragraph.to_string(pretty=False) == (
        "<Paragraph>"
          'Hello, how <strong>are you</strong>? Click <Link to="https://example.com">here</Link>.'
        "</Paragraph>"
    )  # fmt: skip
    assert paragraph.to_html() == (
        '<p>Hello, how <strong>are you</strong>? Click <a href="https://example.com">here</a>.</p>'
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
