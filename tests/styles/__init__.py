from dataclasses import field

from ludic.styles.themes import Colors, Theme
from ludic.styles.types import Color, GlobalStyles


class FooTheme(Theme):
    name: str = "foo"

    colors: Colors = field(
        default_factory=lambda: Colors(
            primary=Color("#0d6efd"),
            secondary=Color("#6c757d"),
            success=Color("#198754"),
            info=Color("#0dcaf0"),
            warning=Color("#ffc107"),
            danger=Color("#dc3545"),
            light=Color("#414549"),
            dark=Color("#f8f8f8"),
            white=Color("#000"),
            black=Color("#fff"),
        )
    )

    @property
    def styles(self) -> GlobalStyles:
        return {}


class BarTheme(Theme):
    name: str = "bar"

    @property
    def styles(self) -> GlobalStyles:
        return {}
