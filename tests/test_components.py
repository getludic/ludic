from pymx.components import Link, Navigation, NavItem


def test_link():
    link = Link("A link!", to="https://example.com")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'


def test_navigation():
    navigation = Navigation(
        NavItem("Home", to="/"),
        NavItem("About", to="/about"),
    )
    assert navigation.to_html() == (
        '<ul class="navigation">'
            '<li id="home"><a href="/">Home</a></li>'
            '<li id="about"><a href="/about">About</a></li>'
        "</ul>"
    )  # fmt: skip
