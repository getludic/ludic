from pymx.components import Link


def test_link():
    link = Link(to="https://example.com")("A link!")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'
