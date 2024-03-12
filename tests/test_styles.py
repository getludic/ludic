from ludic.html import style
from ludic.types import AnyChildren, Attrs, Component


class A(Component[AnyChildren, Attrs]):
    styles = {
        "a": {
            "color": "red",
        },
        ".content": {
            "background": "#ffe",
            "padding": "10px",
        },
        ".content > p": {
            "color": "blue",
            "font-size": "20px",
        },
    }


class B(Component[AnyChildren, Attrs]):
    styles = {
        "a.test": {
            "color": "blue",
        },
    }


def test_styles_formatting() -> None:
    assert style(
        {
            "a": {
                "text-decoration": "none",
                "color": "red",
            },
            "a:hover": {
                "color": "blue",
                "text-decoration": "underline",
            },
        }
    ).to_html() == (
        "<style>\n"
        "a { text-decoration: none; color: red; }\n"
        "a:hover { color: blue; text-decoration: underline; }\n"
        "</style>"
    )


def test_styles_collection() -> None:
    assert style.from_components(A, B).to_html() == (
        "<style>\n"
        "a { color: red; }\n"
        ".content { background: #ffe; padding: 10px; }\n"
        ".content > p { color: blue; font-size: 20px; }\n"
        "a.test { color: blue; }\n"
        "</style>"
    )
