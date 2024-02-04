from pymx.components import Link, Navigation, Page
from pymx.elements import header, link, meta


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


def test_page():
    page = Page(
        title="My Page",
        metadata=[meta(name="description", content="My page description")],
        links=[link(rel="canonical", href="https://example.com")],
    )(
        header("Header"),
        Link(to="https://example.com")("A link!"),
    )
    assert page.to_html() == (
        "<html>"
            "<head>"
                "<title>My Page</title>"
                '<meta name="description" content="My page description" />'
                '<link rel="canonical" href="https://example.com" />'
            "</head>"
            "<body>"
                "<header>Header</header>"
                '<a href="https://example.com">A link!</a>'
            "</body>"
        "</html>"
    )  # fmt: skip
