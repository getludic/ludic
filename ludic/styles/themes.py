from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar

from .types import Color, Size
from .utils import clamp

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
class Header:
    """Header for a theme."""

    size: Size = Size(1.5, "em")
    anchor: bool = True


@dataclass
class Headers:
    """Headers for a theme."""

    h1: Header = field(default_factory=lambda: Header(size=Size(3, "em"), anchor=False))
    h2: Header = field(
        default_factory=lambda: Header(size=Size(2.5, "em"), anchor=True)
    )
    h3: Header = field(default_factory=lambda: Header(size=Size(2, "em"), anchor=False))
    h4: Header = field(
        default_factory=lambda: Header(size=Size(1.5, "em"), anchor=False)
    )
    h5: Header = field(
        default_factory=lambda: Header(size=Size(1.25, "em"), anchor=False)
    )
    h6: Header = field(default_factory=lambda: Header(size=Size(1, "em"), anchor=False))


@dataclass
class Fonts:
    """Font sizes for a theme."""

    plain: str = "sans-serif"
    serif: str = "serif"
    mono: str = "monospace"

    size: Size = Size(1.02, "em")


@dataclass
class Sizes:
    """Size for a theme."""

    xxxxs: str = clamp(Size(0.33), Size(0.39), Size(0.18))
    xxxs: str = clamp(Size(0.41), Size(0.47), Size(0.25))
    xxs: str = clamp(Size(0.51), Size(0.57), Size(0.35))
    xs: str = clamp(Size(0.64), Size(0.69), Size(0.5))
    s: str = clamp(Size(0.8), Size(0.84), Size(0.71))
    m: str = clamp(Size(1), Size(1), Size(1))
    l: str = clamp(Size(1.25), Size(1.19), Size(1.41))  # noqa
    xl: str = clamp(Size(1.56), Size(1.39), Size(2))
    xxl: str = clamp(Size(1.95), Size(1.61), Size(2.83))
    xxxl: str = clamp(Size(2.44), Size(1.83), Size(4))
    xxxxl: str = clamp(Size(3.05), Size(2.04), Size(5.65))


@dataclass
class Borders:
    """Border sizes for a theme."""

    thin: str = clamp(Size(0.1), Size(0.18), Size(0.05))
    normal: str = clamp(Size(0.2), Size(0.25), Size(0.1))
    thick: str = clamp(Size(0.3), Size(0.4), Size(0.2))


@dataclass
class Rounding:
    """Border rounding for a theme."""

    less: str = clamp(Size(0.15), Size(0.20), Size(0.08))
    normal: str = clamp(Size(0.2), Size(0.25), Size(0.12))
    more: str = clamp(Size(0.25), Size(0.35), Size(0.18))


@dataclass
class Theme(metaclass=ABCMeta):
    """An abstract base class for theme classes."""

    measure: Size = Size(80, "ch")
    line_height: float = 1.4

    borders: Borders = field(default_factory=Borders)
    rounding: Rounding = field(default_factory=Rounding)
    fonts: Fonts = field(default_factory=Fonts)
    colors: Colors = field(default_factory=Colors)
    sizes: Sizes = field(default_factory=Sizes)
    headers: Headers = field(default_factory=Headers)

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
