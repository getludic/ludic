from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar

from .types import Color, Size, Spacing

if TYPE_CHECKING:
    from ludic.types import BaseElement

_T = TypeVar("_T", bound="BaseElement")


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

    small: Size = Size(14)
    medium: Size = Size(18)
    large: Size = Size(24)


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
    spacing: Spacing = field(default_factory=Spacing)

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
        element.context["theme"] = self
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
