from ludic.attrs import Attrs
from ludic.components import Component
from ludic.html import style
from ludic.types import AnyChildren

from . import FooTheme


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


def test_styles_nested_formatting() -> None:
    assert (
        style(
            {
                "p.message": {
                    "color": "black",  # type: ignore[dict-item]
                    "background": "yellow",  # type: ignore[dict-item]
                    "padding": "10px",  # type: ignore[dict-item]
                    "a": {
                        "color": "red",
                        "text-decoration": "none",
                    },
                    "a:hover": {
                        "text-decoration": "underline",
                    },
                },
            }
        ).to_html()
        == (
            "<style>\n"
            "p.message { color: black; background: yellow; padding: 10px; }\n"
            "p.message a { color: red; text-decoration: none; }\n"
            "p.message a:hover { text-decoration: underline; }\n"
            "</style>"
        )
    )


def test_styles_with_at_rule() -> None:
    assert (
        style(
            {
                ".htmx-settling": {
                    "opacity": "100",
                },
                "@keyframes lds-ellipsis1": {
                    "0%": {
                        "transform": "scale(0)",
                        "color": "red",
                    }
                },
                "@layer state": {
                    ".alert": {
                        "background-color": "brown",
                    },
                    "p": {
                        "padding": "10px",
                    },
                },
            }
        ).to_html()
    ) == (
        "<style>\n"
        ".htmx-settling { opacity: 100; }\n"
        "@keyframes lds-ellipsis1 { 0% { transform: scale(0); color: red; } }\n"
        "@layer state { .alert { background-color: brown; } p { padding: 10px; } }\n"
        "</style>"
    )


def test_styles_collection() -> None:
    assert style.from_components(A, B, theme=FooTheme()).to_html() == (
        '<style type="text/css">\n'
        "a { color: red; }\n"
        ".content { background: #ffe; padding: 10px; }\n"
        ".content > p { color: blue; font-size: 20px; }\n"
        "a.test { color: blue; }\n"
        "</style>"
    )
