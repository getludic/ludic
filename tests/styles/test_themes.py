from typing import override

from ludic.attrs import GlobalAttrs
from ludic.html import a, b, div, style
from ludic.styles.themes import (
    Colors,
    Fonts,
    get_default_theme,
    set_default_theme,
)
from ludic.styles.types import Color, Size
from ludic.types import Component

from . import BarTheme, FooTheme


def test_theme_colors() -> None:
    theme = FooTheme(
        colors=Colors(
            primary=Color("#c2e7fd"),
            white=Color("#fff"),
            light=Color("#eee"),
            dark=Color("#333"),
            black=Color("#000"),
        )
    )

    assert theme.colors.primary.rgb == (194, 231, 253)
    assert theme.colors.white.rgb == (255, 255, 255)
    assert theme.colors.light.rgb == (238, 238, 238)
    assert theme.colors.dark.rgb == (51, 51, 51)
    assert theme.colors.black.rgb == (0, 0, 0)

    assert theme.colors.white.darken(0.5).rgb == (127, 127, 127)
    assert theme.colors.white.darken(1).rgb == (1, 1, 1)
    assert theme.colors.black.lighten(0.5).rgb == (127, 127, 127)
    assert theme.colors.black.lighten(1).rgb == (255, 255, 255)

    assert theme.colors.light.darken(0.5).rgb == (119, 119, 119)
    assert theme.colors.dark.lighten(0.5).rgb == (153, 153, 153)

    assert theme.colors.primary.darken(0.5).rgb == (97, 115, 126)


def test_theme_font_sizes() -> None:
    theme = FooTheme(fonts=Fonts(size=Size(10, "px")))

    assert theme.fonts.size == "10px"
    assert theme.fonts.plain == "sans-serif"


def test_themes_switching() -> None:
    foo, bar = FooTheme(), BarTheme()

    set_default_theme(foo)
    assert get_default_theme() == foo
    set_default_theme(bar)
    assert get_default_theme() == bar


def test_element_theme_switching() -> None:
    foo = FooTheme()
    bar = BarTheme()

    set_default_theme(bar)

    class C1(Component[str, GlobalAttrs]):
        styles = style.use(
            lambda theme: {
                "#c1 a": {"color": theme.colors.warning},
            }
        )

        @override
        def render(self) -> div:
            return div(
                b("Hello, ", style={"color": self.theme.colors.secondary}),
                a(*self.children, href="https://example.com"),
                id="c1",
            )

    class C2(Component[str, GlobalAttrs]):
        styles = style.use(
            lambda theme: {
                "#c2 a": {"color": theme.colors.danger},
            }
        )

        @override
        def render(self) -> div:
            return div(
                foo.use(C1(*self.children)),
                id="c2",
                style={"background-color": self.theme.colors.primary},
            )

    assert C2("World").to_html() == (
        f'<div id="c2" style="background-color:{bar.colors.primary}">'
          '<div id="c1">'
            f'<b style="color:{foo.colors.secondary}">Hello, </b>'
            '<a href="https://example.com">World</a>'
          "</div>"
        "</div>"
    )  # fmt: skip
    assert style.from_components(C1, C2).to_html() == (
        '<style type="text/css">\n'
          f"#c1 a {{ color: {bar.colors.warning}; }}\n"
          f"#c2 a {{ color: {bar.colors.danger}; }}\n"
        "</style>"
    )  # fmt: skip

    set_default_theme(foo)

    assert style.from_components(C1, C2).to_html() == (
        '<style type="text/css">\n'
          f"#c1 a {{ color: {foo.colors.warning}; }}\n"
          f"#c2 a {{ color: {foo.colors.danger}; }}\n"
        "</style>"
    )  # fmt: skip
