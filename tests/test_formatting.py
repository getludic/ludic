from ludic.catalog.typography import Link, Paragraph
from ludic.html import p, strong


def test_component_with_f_string():
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


def test_escaping_works():
    link = '<a href="https://example.com">test</a>'
    dom = p(f"Hello, how <b>are you</b>? Click {link}.")
    assert dom.to_html() == (
        "<p>Hello, how &lt;b&gt;are you&lt;/b&gt;? "
        "Click &lt;a href=&quot;https://example.com&quot;&gt;test&lt;/a&gt;.</p>"
    )
