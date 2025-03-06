from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import TypeVar

from ludic.base import BaseElement

from .types import BaseSize, Color, ColorRange, Size, SizeClamp

highlight_light: str | type = "default"
highlight_dark: str | type = "default"
try:
    from .highlight import LudicDark, LudicLight

    highlight_light = LudicLight
    highlight_dark = LudicDark
except ImportError:
    pass

_T = TypeVar("_T", bound="BaseElement")


@dataclass
class Colors:
    """Colors for a theme."""

    primary: Color = ColorRange(["#276662", "#4ecdc4", "#dbf5f3"])
    secondary: Color = ColorRange(["#212529", "#414549", "#616569"])
    success: Color = ColorRange(["#637a32", "#c7f464", "#eefbd0"])
    info: Color = ColorRange(["#978801", "#fce303", "#fef9cc"])
    warning: Color = ColorRange(["#7e4801", "#fc9003", "#fee8cc"])
    danger: Color = ColorRange(["#711414", "#e32929", "#f9d4d4"])

    light: Color = Color("#f2f2f2")
    dark: Color = Color("#414549")

    white: Color = Color("#fff")
    black: Color = Color("#222")


@dataclass
class Header:
    """Header for a theme."""

    size: BaseSize = SizeClamp(1.5, 2, 2.5)
    anchor: bool = False


@dataclass
class Headers:
    """Headers for a theme."""

    h1: Header = field(
        default_factory=lambda: Header(size=SizeClamp(2, 1.5, 3.3), anchor=False)
    )
    h2: Header = field(
        default_factory=lambda: Header(size=SizeClamp(1.5, 1.3, 2.8), anchor=False)
    )
    h3: Header = field(
        default_factory=lambda: Header(size=SizeClamp(1.2, 0.8, 2.2), anchor=False)
    )
    h4: Header = field(
        default_factory=lambda: Header(size=SizeClamp(1, 0.6, 1.8), anchor=False)
    )
    h5: Header = field(
        default_factory=lambda: Header(size=SizeClamp(0.7, 0.5, 1.3), anchor=False)
    )
    h6: Header = field(
        default_factory=lambda: Header(size=SizeClamp(0.5, 0.4, 1.1), anchor=False)
    )


@dataclass
class Fonts:
    """Font sizes for a theme."""

    primary: str = "Helvetica Neue, Helvetica, Arial, sans-serif"
    secondary: str = "Georgia, serif"
    monospace: str = "Space Mono, Roboto Mono, monospace"

    size: BaseSize = Size(1, "em")


@dataclass
class Sizes:
    """Size for a theme."""

    xxxxs: BaseSize = SizeClamp(0.39, 0, 0.47)
    xxxs: BaseSize = SizeClamp(0.47, 0.1, 0.69)
    xxs: BaseSize = SizeClamp(0.57, 0.15, 0.69)
    xs: BaseSize = SizeClamp(0.69, 0.2, 0.84)
    s: BaseSize = SizeClamp(0.84, 0.25, 1)
    m: BaseSize = SizeClamp(1, 0.3, 1.16)
    l: BaseSize = SizeClamp(1.16, 0.35, 1.4)  # noqa
    xl: BaseSize = SizeClamp(1.4, 0.4, 1.68)
    xxl: BaseSize = SizeClamp(1.68, 0.45, 2.01)
    xxxl: BaseSize = SizeClamp(2.01, 0.5, 2.41)
    xxxxl: BaseSize = SizeClamp(2.41, 0.55, 2.88)


@dataclass
class Borders:
    """Border sizes for a theme."""

    thin: BaseSize = Size(0.1)
    normal: BaseSize = Size(0.23)
    thick: BaseSize = Size(0.42)


@dataclass
class Rounding:
    """Border rounding for a theme."""

    less: BaseSize = Size(0.20)
    normal: BaseSize = Size(0.25)
    more: BaseSize = Size(0.35)


@dataclass
class Sidebar:
    """Sidebar layout config for a theme."""

    # The width of the sidebar (empty means not set; defaults to the content width)
    side_width: str | None = None

    # The narrowest the content element can be before wrapping. Should be a percentage.
    content_min_width: str = "60%"


@dataclass
class Switcher:
    """Switcher layout config for a theme."""

    # The container width at which the component switches between a horizontal and
    # vertical layout
    threshold: BaseSize = Size(40, "rem")

    # The maximum number of elements allowed to appear in the horizontal configuration
    limit: int = 4


@dataclass
class Cover:
    """Cover layout config for a theme."""

    # The minimum height of the cover
    min_height: BaseSize = Size(100, "vh")

    # The minimum space between and around the child elements
    element: str = "h1"


@dataclass
class Grid:
    """Grid layout config for a theme."""

    # The size of the grid cells
    cell_size: BaseSize = Size(250, "px")


@dataclass
class Frame:
    """Frame layout config for a theme."""

    # The width of the frame as fraction
    numerator: int = 16

    # The height of the frame as fraction
    denominator: int = 9


@dataclass
class Layouts:
    """Layout configuration for a theme."""

    sidebar: Sidebar = field(default_factory=Sidebar)
    switcher: Switcher = field(default_factory=Switcher)
    cover: Cover = field(default_factory=Cover)
    grid: Grid = field(default_factory=Grid)
    frame: Frame = field(default_factory=Frame)


@dataclass
class CodeBlock:
    """Code block config for a theme."""

    color: Color = Color("#414549")
    background_color: Color = Color("#f2f2f2")
    line_number_color: Color = Color("#c2c2c2")
    line_numbers: bool = True
    font_size: BaseSize = Size(0.9)
    style: str | type = highlight_light


@dataclass
class Theme(metaclass=ABCMeta):
    """An abstract base class for theme configuration."""

    measure: BaseSize = Size(70, "ch")
    line_height: float = 1.5

    fonts: Fonts = field(default_factory=Fonts)
    colors: Colors = field(default_factory=Colors)
    sizes: Sizes = field(default_factory=Sizes)

    borders: Borders = field(default_factory=Borders)
    rounding: Rounding = field(default_factory=Rounding)
    headers: Headers = field(default_factory=Headers)

    layouts: Layouts = field(default_factory=Layouts)
    code: CodeBlock = field(default_factory=CodeBlock)

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
            primary=ColorRange(["#de946f", "#bd7b5b", "#9e674c"]),
            secondary=Color("#a79272"),
            success=Color("#56A677"),
            info=Color("#518eb5"),
            warning=Color("#d09d3c"),
            danger=Color("#e15c4d"),
            light=ColorRange(["#665949", "#52473a", "#302a22"]),
            dark=ColorRange(["#cfc5b6", "#cab8a5", "#a69685"]),
            white=ColorRange(["#302a22", "#231f1a", "#12100e"]),
            black=ColorRange(["#f2ebe1", "#ebe4da", "#cfc5b6"]),
        ),
    )
    code: CodeBlock = field(
        default_factory=lambda: CodeBlock(
            color=ColorRange(["#ebe4da", "#cfc5b6", "#cab8a5"]),
            background_color=ColorRange(["#52473a", "#302a22", "#231f1a"]),
            line_number_color=Color("#a69685"),
            style=highlight_dark,
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
