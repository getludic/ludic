from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypeVar

from .types import Color, Size

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

    plain: str = "Helvetica Neue, Helvetica, Arial, sans-serif"
    serif: str = "Georgia, serif"
    mono: str = "Space Mono, Roboto Mono, monospace"

    size: Size = Size(1.02, "em")


@dataclass
class Sizes:
    """Size for a theme."""

    xxxxs: Size = Size(0.39)
    xxxs: Size = Size(0.47)
    xxs: Size = Size(0.57)
    xs: Size = Size(0.69)
    s: Size = Size(0.84)
    m: Size = Size(1)
    l: Size = Size(1.19)  # noqa
    xl: Size = Size(1.39)
    xxl: Size = Size(1.61)
    xxxl: Size = Size(1.83)
    xxxxl: Size = Size(2.04)


@dataclass
class Borders:
    """Border sizes for a theme."""

    thin: Size = Size(0.1)
    normal: Size = Size(0.23)
    thick: Size = Size(0.42)


@dataclass
class Rounding:
    """Border rounding for a theme."""

    less: Size = Size(0.20)
    normal: Size = Size(0.25)
    more: Size = Size(0.35)


@dataclass
class Sidebar:
    """Sidebar layout config for a theme."""

    # The width of the sidebar (empty means not set; defaults to the content width)
    side_width: Size | None = None

    # The narrowest the content element can be before wrapping. Should be a percentage.
    content_min_width: str = "60%"


@dataclass
class Switcher:
    """Switcher layout config for a theme."""

    # The container width at which the component switches between a horizontal and
    # vertical layout
    threshold: Size = Size(40, "rem")

    # The maximum number of elements allowed to appear in the horizontal configuration
    limit: int = 4


@dataclass
class Layouts:
    """Layout configuration for a theme."""

    sidebar: Sidebar = field(default_factory=Sidebar)
    switcher: Switcher = field(default_factory=Switcher)


@dataclass
class Theme(metaclass=ABCMeta):
    """An abstract base class for theme configuration."""

    measure: Size = Size(110, "ch")
    line_height: float = 1.4

    fonts: Fonts = field(default_factory=Fonts)
    colors: Colors = field(default_factory=Colors)
    sizes: Sizes = field(default_factory=Sizes)

    borders: Borders = field(default_factory=Borders)
    rounding: Rounding = field(default_factory=Rounding)
    headers: Headers = field(default_factory=Headers)

    layouts: Layouts = field(default_factory=Layouts)

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
