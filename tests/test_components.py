from pymx.components import Link, Navigation


def test_link():
    link = Link(to="https://example.com")("A link!")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'


def test_navigation():
    navigation = Navigation(
        class_="nav",
        items={"Home": "https://example.com", "About": "https://example.com/about"},
    )
    assert navigation.to_html() == (
        '<ul class="nav">'
            '<li><a href="https://example.com">Home</a></li>'
            '<li><a href="https://example.com/about">About</a></li>'
        "</ul>"
    )  # fmt: skip
