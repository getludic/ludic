from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Self, TypeVar

from .utils import darken_color, hex_to_rgb, lighten_color

if TYPE_CHECKING:
    from ludic.types import BaseElement

_T = TypeVar("_T", bound="BaseElement")


class Color(str):
    """Color class."""

    @property
    def rgb(self) -> tuple[int, int, int]:
        """RGB color."""
        return hex_to_rgb(self)

    def darken(self, factor: float = 0.5) -> Self:
        """Darken color by a given factor.

        Args:
            factor (float, optional): Darkening factor. Defaults to 0.5.

        Returns:
            str: Darkened color.
        """
        return type(self)(darken_color(self, factor))

    def lighten(self, factor: float = 0.5) -> Self:
        """Lighten color by a given factor.

        Args:
            factor (float, optional): Lightening factor. Defaults to 0.5.

        Returns:
            str: Lightened color.
        """
        return type(self)(lighten_color(self, factor))


class Size(str):
    """Size class."""

    value: int
    unit: Literal["px", "em"] = "px"  # Default unit is pixels

    def __new__(cls, value: int, unit: Literal["px", "em"] = "px") -> "Size":
        self = super().__new__(cls, f"{value}{unit}")
        self.value = value
        self.unit = unit
        return self

    def inc(self, factor: float = 1) -> Self:
        """Increment size by a given factor.

        Args:
            factor (float, optional): Increment factor. Defaults to 1.

        Returns:
            str: Incremented size.
        """
        return type(self)(int(self.value + float(self.value * factor)), self.unit)

    def dec(self, factor: float = 1) -> Self:
        """Decrement size by a given factor.

        Args:
            factor (float, optional): Decrement factor. Defaults to 1.

        Returns:
            str: Decremented size.
        """
        return type(self)(int(self.value - float(self.value * factor)), self.unit)


@dataclass
class Colors:
    """Colors for a theme."""

    primary: Color = Color("#0d6efd")
    secondary: Color = Color("#6c757d")
    success: Color = Color("#198754")
    info: Color = Color("#0dcaf0")
    warning: Color = Color("#ffc107")
    danger: Color = Color("#dc3545")

    dark: Color = Color("#313539")
    light: Color = Color("#f8f9fa")
    white: Color = Color("#fff")
    black: Color = Color("#222")


@dataclass
class FontSizes:
    """Font sizes for a theme."""

    small: Size = Size(12)
    medium: Size = Size(16)
    large: Size = Size(20)


@dataclass
class FontFamilies:
    """Font families for a theme."""

    headers: str = "serif"
    paragraphs: str = "sans-serif"
    monospace: str = "monospace"


@dataclass
class Fonts:
    """Font sizes for a theme."""

    families: FontFamilies = field(default_factory=FontFamilies)
    sizes: FontSizes = field(default_factory=FontSizes)


@dataclass
class Theme(metaclass=ABCMeta):
    """An abstract base class for theme classes."""

    fonts: Fonts = field(default_factory=Fonts)
    colors: Colors = field(default_factory=Colors)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Theme) and self.name == other.name

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the theme."""
        raise NotImplementedError

    def use(self, element: _T) -> _T:
        element.theme = self
        return element


@dataclass
class DarkTheme(Theme):
    """The dark theme."""

    name: str = "dark"


@dataclass
class LightTheme(Theme):
    """Light theme."""

    name: str = "light"

    colors: Colors = field(
        default_factory=lambda: Colors(
            primary=Color("#c2e7fd"),
            secondary=Color("#fefefe"),
            success=Color("#c9ffad"),
            info=Color("#fff080"),
            warning=Color("#ffc280"),
            danger=Color("#ffaca1"),
            light=Color("#f8f8f8"),
            dark=Color("#414549"),
        )
    )


_DEFAULT_THEME: Theme = LightTheme()


def get_default_theme() -> Theme:
    """Get the default theme."""
    return _DEFAULT_THEME


def set_default_theme(theme: Theme) -> None:
    """Set the default theme."""
    global _DEFAULT_THEME
    _DEFAULT_THEME = theme
