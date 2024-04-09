from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Self, TypeVar

from .utils import darken_color, hex_to_rgb, lighten_color, pick_readable_color_for

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

    def readable(self) -> Self:
        """Get lighter or darker variant of the given color depending on the luminance.

        Args:
            color (str): Color to find the readable opposite for.

        Returns:
            str: Readable opposite of the given color.
        """
        return type(self)(pick_readable_color_for(self))


class Size(str):
    """Size class."""

    value: float
    unit: Literal["px", "em"] = "px"  # Default unit is pixels

    def __new__(cls, value: float, unit: Literal["px", "em"] = "px") -> "Size":
        match unit:
            case "em":
                self = super().__new__(cls, f"{value:.1f}{unit}")
            case "px":
                self = super().__new__(cls, f"{value:d}{unit}")
            case _:
                raise ValueError(f"Invalid unit: {unit}")

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
        return type(self)(self.value + float(self.value * factor), self.unit)

    def dec(self, factor: float = 1) -> Self:
        """Decrement size by a given factor.

        Args:
            factor (float, optional): Decrement factor. Defaults to 1.

        Returns:
            str: Decremented size.
        """
        return type(self)(self.value - float(self.value * factor), self.unit)


@dataclass
class Colors:
    """Colors for a theme."""

    primary: Color = Color("#4ecdc4")
    secondary: Color = Color("#fefefe")
    success: Color = Color("#c7f464")
    info: Color = Color("#fce303")
    warning: Color = Color("#fc9003")
    danger: Color = Color("#e32929")

    light: Color = Color("#f8f8f8")
    dark: Color = Color("#414549")

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
        """Apply the theme to an element.

        Args:
            element (_T): Element to apply the theme to.

        Returns:
            _T: The element with the theme applied.
        """
        element.theme = self
        return element


@dataclass
class DarkTheme(Theme):
    """The dark theme."""

    name: str = "dark"

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


@dataclass
class LightTheme(Theme):
    """Light theme."""

    name: str = "light"


_DEFAULT_THEME: Theme = LightTheme()


def get_default_theme() -> Theme:
    """Get the default theme."""
    return _DEFAULT_THEME


def set_default_theme(theme: Theme) -> None:
    """Set the default theme."""
    global _DEFAULT_THEME
    _DEFAULT_THEME = theme
