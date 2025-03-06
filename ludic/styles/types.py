from abc import ABCMeta, abstractmethod
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Literal,
    LiteralString,
    Self,
    SupportsIndex,
    TypedDict,
)

from typing_extensions import TypeVar

from .utils import (
    clamp,
    darken_color,
    hex_to_rgb,
    lighten_color,
    pick_readable_color_for,
)

if TYPE_CHECKING:
    from .themes import Theme

TTheme = TypeVar("TTheme", bound="Theme", default="Theme")
SizeUnit = Literal["px", "ex", "em", "ch", "rem", "vw", "vh", "vmin", "vmax", "%"]


def format_unit(value: float, unit: SizeUnit = "rem") -> str:
    match unit:
        case "px" | "ch":
            formatted = f"{value:.0f}{unit}"
        case _:
            formatted = f"{value:.2f}".rstrip("0").rstrip(".")
            if not formatted or formatted == "0":
                formatted = f"0{unit}"
            else:
                formatted = f"{formatted}{unit}"
    return formatted


class Color(str):
    """Color class."""

    @property
    def rgb(self) -> tuple[int, int, int]:
        """RGB color."""
        return hex_to_rgb(self)

    def darken(self, shift: int = 1) -> Self:
        """Pick darker color from the range by given shift.

        Args:
            shift (int, optional): Darkening shift. Defaults to 1.

        Returns:
            str: Darkened color.
        """
        return type(self)(darken_color(self, shift / 20))

    def lighten(self, shift: int = 1) -> Self:
        """Pick lighter color from the range by given shift.

        Args:
            shift (int, optional): Lightening shift. Defaults to 1.

        Returns:
            str: Lightened color.
        """
        return type(self)(lighten_color(self, shift / 20))

    def readable(self) -> Self:
        """Get lighter or darker variant of the given color depending on the luminance.

        Args:
            color (str): Color to find the readable opposite for.

        Returns:
            str: Readable opposite of the given color.
        """
        return type(self)(pick_readable_color_for(self))


class ColorRange(Color):
    """Color class."""

    variants: list[str]
    position: int

    def __new__(
        cls, variants: list[str] | str, position: int | None = None
    ) -> "ColorRange":
        if isinstance(variants, str):
            variants = [variants]

        if position is None:
            position = len(variants) // 2

        self = super().__new__(cls, variants[position])
        self.variants = variants
        self.position = position
        return self

    def darken(self, shift: int = 1) -> Self:
        """Pick darker color from the range by given shift.

        Args:
            shift (int, optional): Darkening shift. Defaults to 1.

        Returns:
            str: Darkened color.
        """
        if 0 <= self.position - shift < len(self.variants):
            return type(self)(self.variants, self.position - shift)
        else:
            return type(self)(self.variants, 0)

    def lighten(self, shift: int = 1) -> Self:
        """Pick lighter color from the range by given shift.

        Args:
            shift (int, optional): Lightening shift. Defaults to 1.

        Returns:
            str: Lightened color.
        """
        if 0 <= self.position + shift < len(self.variants):
            return type(self)(self.variants, self.position + shift)
        else:
            return type(self)(self.variants, len(self.variants) - 1)


class BaseSize(str, metaclass=ABCMeta):
    """Base size class."""

    @abstractmethod
    def __mul__(self, factor: float | int | LiteralString | SupportsIndex) -> Self:
        pass

    @abstractmethod
    def __add__(self, value: float | int | LiteralString | SupportsIndex) -> Self:
        pass

    @abstractmethod
    def __sub__(self, value: float | int | LiteralString | SupportsIndex) -> Self:
        pass


class Size(BaseSize):
    """Size class."""

    value: float
    unit: SizeUnit = "rem"

    def __new__(cls, value: float, unit: SizeUnit = "rem") -> "Size":
        self = super().__new__(cls, format_unit(value, unit))
        self.value = value
        self.unit = unit
        return self

    def __mul__(self, factor: float | int | LiteralString | SupportsIndex) -> Self:
        """Scale size by a given factor.

        Args:
            factor (float): Scaling factor.

        Returns:
            str: Scaled size.
        """
        if isinstance(factor, float | int):
            return type(self)(self.value * factor, self.unit)
        else:
            return self

    def __add__(self, value: float | int | LiteralString | SupportsIndex) -> Self:
        """Increment size by a given factor.

        Args:
            value (float, optional): Increment value.

        Returns:
            str: Incremented size.
        """
        if isinstance(value, float | int):
            return type(self)(self.value + value, self.unit)
        else:
            return self

    def __sub__(self, value: float | int | LiteralString | SupportsIndex) -> Self:
        """Decrement size by a given factor.

        Args:
            value (float, optional): Decrement value.

        Returns:
            str: Decremented size.
        """
        if isinstance(value, float | int):
            return type(self)(self.value - value, self.unit)
        else:
            return self


class SizeClamp(BaseSize):
    """Size clamp class."""

    minimum: float
    value: float
    maximum: float
    base_unit: SizeUnit = "rem"
    viewport_unit: SizeUnit = "vw"

    def __new__(
        cls,
        minimum: float,
        value: float,
        maximum: float,
        base_unit: SizeUnit = "rem",
        viewport_unit: SizeUnit = "vw",
    ) -> "SizeClamp":
        self = super().__new__(
            cls,
            clamp(
                format_unit(minimum, base_unit),
                (
                    f"{format_unit(minimum, base_unit)} + "
                    f"{format_unit(value, viewport_unit)}"
                ),
                format_unit(maximum, base_unit),
            ),
        )

        self.minimum = minimum
        self.value = value
        self.maximum = maximum
        self.base_unit = base_unit
        self.viewport_unit = viewport_unit
        return self

    def __mul__(self, factor: float | int | LiteralString | SupportsIndex) -> Self:
        """Scale size by a given factor.

        Args:
            factor (float): Scaling factor.

        Returns:
            str: Scaled size.
        """
        if isinstance(factor, float | int):
            return type(self)(
                self.minimum * factor, self.value * factor, self.maximum * factor
            )
        else:
            return self

    def __add__(self, value: float | int | LiteralString | SupportsIndex) -> Self:
        """Increment size by a given factor.

        Args:
            value (float, optional): Increment value.

        Returns:
            str: Incremented size.
        """
        if isinstance(value, float | int):
            return type(self)(
                self.minimum + value, self.value + value, self.maximum + value
            )
        else:
            return self

    def __sub__(self, value: float | int | LiteralString | SupportsIndex) -> Self:
        """Decrement size by a given factor.

        Args:
            value (float, optional): Decrement value.

        Returns:
            str: Decremented size.
        """
        if isinstance(value, float | int):
            return type(self)(
                self.minimum - value, self.value - value, self.maximum - value
            )
        else:
            return self


CSSProperties = TypedDict(
    "CSSProperties",
    {
        # A
        "align-content": Literal[
            "center",
            "flex-start",
            "flex-end",
            "space-between",
            "space-around",
            "stretch",
        ],
        "align-items": Literal[
            "stretch", "center", "flex-start", "flex-end", "baseline"
        ],
        "align-self": Literal[
            "auto",
            "stretch",
            "center",
            "flex-start",
            "flex-end",
            "baseline",
            "initial",
            "inherit",
        ],
        "all": str,
        "animation": str,
        "animation-delay": str,
        "animation-direction": Literal[
            "normal", "reverse", "alternate", "alternate-reverse"
        ],
        "animation-duration": str,
        "animation-fill-mode": Literal["none", "forwards", "backwards", "both"],
        "animation-iteration-count": float,
        "animation-name": str,
        "animation-play-state": Literal["paused", "running"],
        "animation-timing-function": str,
        "aspect-ratio": str,
        # B
        "backdrop-filter": str,
        "backface-visibility": Literal["visible", "hidden"],
        "background": str,
        "background-attachment": Literal["scroll", "fixed", "local"],
        "background-blend-mode": str,
        "background-clip": Literal["border-box", "padding-box", "content-box", "text"],
        "background-color": str,
        "background-image": str,
        "background-origin": Literal["padding-box", "border-box", "content-box"],
        "background-position": str,
        "background-repeat": Literal[
            "repeat", "repeat-x", "repeat-y", "no-repeat", "space", "round"
        ],
        "background-size": Literal["auto", "cover", "contain"],
        "block-size": str,
        "border": str,
        "border-block": str,
        "border-block-color": str,
        "border-block-end": str,
        "border-block-end-color": str,
        "border-block-end-style": str,
        "border-block-end-width": str,
        "border-block-start": str,
        "border-block-start-color": str,
        "border-block-start-style": str,
        "border-block-start-width": str,
        "border-block-style": str,
        "border-block-width": str,
        "border-bottom": str,
        "border-bottom-color": str,
        "border-bottom-left-radius": str,
        "border-bottom-right-radius": str,
        "border-bottom-style": str,
        "border-bottom-width": str,
        "border-collapse": Literal["collapse", "separate"],
        "border-color": str,
        "border-image": str,
        "border-image-outset": str,
        "border-image-repeat": Literal["stretch", "repeat", "round"],
        "border-image-slice": str,
        "border-image-source": str,
        "border-image-width": str,
        "border-inline": str,
        "border-inline-color": str,
        "border-inline-end": str,
        "border-inline-end-color": str,
        "border-inline-end-style": str,
        "border-inline-end-width": str,
        "border-inline-start": str,
        "border-inline-start-color": str,
        "border-inline-start-style": str,
        "border-inline-start-width": str,
        "border-inline-style": str,
        "border-inline-width": str,
        "border-left": str,
        "border-left-color": str,
        "border-left-style": str,
        "border-left-width": str,
        "border-radius": str,
        "border-right": str,
        "border-right-color": str,
        "border-right-style": str,
        "border-right-width": str,
        "border-spacing": str,
        "border-style": str,
        "border-top": str,
        "border-top-color": str,
        "border-top-left-radius": str,
        "border-top-right-radius": str,
        "border-top-style": str,
        "border-top-width": str,
        "border-width": str,
        "bottom": str,
        "box-decoration-break": Literal["slice", "clone"],
        "box-shadow": str,
        "box-sizing": Literal["content-box", "border-box"],
        # C
        "caption-side": Literal["top", "bottom"],
        "caret-color": str,
        "clear": Literal["none", "left", "right", "both"],
        "clip": str,
        "clip-path": str,
        "color": str,
        "column-count": str,
        "column-fill": Literal["auto", "balance"],
        "column-gap": str,
        "column-rule": str,
        "column-rule-color": str,
        "column-rule-style": str,
        "column-rule-width": str,
        "column-span": Literal["none", "all"],
        "column-width": str,
        "columns": str,
        "content": str,
        "counter-increment": str,
        "counter-reset": str,
        "cursor": Literal[
            "alias",
            "all-scroll",
            "auto",
            "cell",
            "context-menu",
            "col-resize",
            "copy",
            "crosshair",
            "default",
            "e-resize",
            "ew-resize",
            "grab",
            "grabbing",
            "help",
            "move",
            "n-resize",
            "ne-resize",
            "nesw-resize",
            "ns-resize",
            "nw-resize",
            "nwse-resize",
            "no-drop",
            "none",
            "not-allowed",
            "pointer",
            "progress",
            "row-resize",
            "s-resize",
            "se-resize",
            "sw-resize",
            "text",
            "unset",
            "vertical-text",
            "w-resize",
            "wait",
            "zoom-in",
            "zoom-out",
        ],
        # D
        "direction": Literal["ltr", "rtl"],
        "display": Literal[
            "block",
            "contents",
            "flex",
            "grid",
            "inline",
            "inline-block",
            "inline-flex",
            "inline-grid",
            "inline-table",
            "list-item",
            "run-in",
            "table",
            "table-caption",
            "table-cell",
            "table-column",
            "table-column-group",
            "table-footer-group",
            "table-header-group",
            "table-row",
            "table-row-group",
            "none",
            "unset",
        ],
        "empty-cells": Literal["show", "hide"],
        # F
        "filter": str,
        "flex": str,
        "flex-basis": float | str,
        "flex-direction": Literal["row", "row-reverse", "column", "column-reverse"],
        "flex-flow": str,
        "flex-grow": float | str,
        "flex-shrink": float | str,
        "flex-wrap": Literal["nowrap", "wrap", "wrap-reverse"],
        "float": Literal["left", "right", "none"],
        "font": str,
        "font-family": str,
        "font-feature-settings": str,
        "font-kerning": Literal["auto", "normal", "none"],
        "font-language-override": str,
        "font-size": str,
        "font-size-adjust": str,
        "font-stretch": Literal[
            "normal",
            "ultra-condensed",
            "extra-condensed",
            "condensed",
            "semi-condensed",
            "semi-expanded",
            "expanded",
            "extra-expanded",
            "ultra-expanded",
        ],
        "font-style": Literal["normal", "italic", "oblique"],
        "font-synthesis": Literal["none", "weight", "style"],
        "font-variant": Literal["normal", "small-caps"],
        "font-variant-caps": Literal[
            "normal",
            "small-caps",
            "all-small-caps",
            "petite-caps",
            "all-petite-caps",
            "unicase",
            "titling-caps",
        ],
        "font-variant-east-asian": Literal[
            "normal",
            "ruby",
            "jis78",
            "jis83",
            "jis90",
            "jis04",
            "simplified",
            "traditional",
        ],
        "font-variant-ligatures": Literal[
            "normal",
            "none",
            "common-ligatures",
            "no-common-ligatures",
            "discretionary-ligatures",
            "no-discretionary-ligatures",
            "historical-ligatures",
            "no-historical-ligatures",
            "contextual",
            "no-contextual",
        ],
        "font-variant-numeric": Literal[
            "normal",
            "ordinal",
            "slashed-zero",
            "lining-nums",
            "oldstyle-nums",
            "proportional-nums",
            "tabular-nums",
            "diagonal-fractions",
            "stacked-fractions",
        ],
        "font-variant-position": Literal["normal", "sub", "super"],
        "font-weight": Literal[
            "normal",
            "bold",
            "bolder",
            "lighter",
            "100",
            "200",
            "300",
            "400",
            "500",
            "600",
            "700",
            "800",
            "900",
        ],
        # G
        "gap": str,
        "grid": str,
        "grid-area": str,
        "grid-auto-columns": str,
        "grid-auto-flow": Literal["row", "column", "dense"],
        "grid-auto-rows": str,
        "grid-column": str,
        "grid-column-end": str,
        "grid-column-gap": str,
        "grid-column-start": str,
        "grid-gap": str,
        "grid-row": str,
        "grid-row-end": str,
        "grid-row-gap": str,
        "grid-row-start": str,
        "grid-template": str,
        "grid-template-areas": str,
        "grid-template-columns": str,
        "grid-template-rows": str,
        # H
        "hanging-punctuation": Literal[
            "none", "first", "last", "allow-end", "force-end"
        ],
        "height": str,
        "hyphens": Literal["none", "manual", "auto"],
        # I
        "inset": str | int,
        "inline-size": str,
        # J
        "justify-content": Literal[
            "flex-start",
            "flex-end",
            "center",
            "space-between",
            "space-around",
            "space-evenly",
            "start",
            "end",
            "left",
            "right",
        ],
        # L
        "left": str,
        "letter-spacing": str,
        "line-break": Literal["auto", "loose", "normal", "strict"],
        "line-height": float,
        "list-style": str,
        "list-style-image": str,
        "list-style-position": Literal["inside", "outside"],
        "list-style-type": Literal[
            "disc",
            "circle",
            "square",
            "decimal",
            "decimal-leading-zero",
            "lower-roman",
            "upper-roman",
            "lower-greek",
            "lower-alpha",
            "lower-latin",
            "upper-alpha",
            "upper-latin",
            "hebrew",
            "armenian",
            "georgian",
            "cjk-ideographic",
            "hiragana",
            "katakana",
            "hiragana-iroha",
            "katakana-iroha",
            "none",
        ],
        # M
        "margin": str,
        "margin-block": str,
        "margin-block-end": str,
        "margin-block-start": str,
        "margin-bottom": str,
        "margin-inline": str,
        "margin-inline-end": str,
        "margin-inline-start": str,
        "margin-left": str,
        "margin-right": str,
        "margin-top": str,
        "mask": str,
        "mask-border": str,
        "mask-border-mode": Literal["alpha", "luminance"],
        "mask-border-outset": str,
        "mask-border-repeat": str,
        "mask-border-slice": str,
        "mask-border-source": str,
        "mask-border-width": str,
        "mask-clip": str,
        "mask-composite": str,
        "mask-image": str,
        "mask-mode": str,
        "mask-origin": str,
        "mask-position": str,
        "mask-repeat": str,
        "mask-size": str,
        "mask-type": Literal["alpha", "luminance"],
        "max-block-size": str,
        "max-height": str,
        "max-inline-size": str,
        "max-width": str,
        "min-block-size": str,
        "min-height": str,
        "min-inline-size": str,
        "min-width": str,
        # O
        "object-fit": Literal["fill", "contain", "cover", "none", "scale-down"],
        "object-position": str,
        "offset": str,
        "offset-anchor": str,
        "offset-distance": str,
        "offset-path": str,
        "offset-position": str,
        "offset-rotate": str,
        "opacity": str,
        "order": str,
        "outline": str,
        "outline-color": str,
        "outline-offset": str,
        "outline-style": str,
        "outline-width": str,
        "overflow": Literal["auto", "hidden", "scroll", "visible"],
        "overflow-anchor": Literal["auto", "none"],
        "overflow-block": Literal["auto", "scroll", "visible"],
        "overflow-inline": Literal["auto", "scroll", "visible"],
        "overflow-wrap": Literal["normal", "break-word", "anywhere"],
        "overflow-x": Literal["auto", "hidden", "scroll", "visible"],
        "overflow-y": Literal["auto", "hidden", "scroll", "visible"],
        # P
        "padding": str,
        "padding-block": str,
        "padding-block-end": str,
        "padding-block-start": str,
        "padding-bottom": str,
        "padding-inline": str,
        "padding-inline-end": str,
        "padding-inline-start": str,
        "padding-left": str,
        "padding-right": str,
        "padding-top": str,
        "page-break-after": Literal["auto", "always", "avoid", "left", "right"],
        "page-break-before": Literal["auto", "always", "avoid", "left", "right"],
        "page-break-inside": Literal["auto", "avoid"],
        "paint-order": Literal["normal", "fill", "stroke", "markers"],
        "perspective": str,
        "perspective-origin": str,
        "place-content": str,
        "place-items": str,
        "place-self": str,
        "pointer-events": Literal[
            "auto",
            "none",
            "visiblePainted",
            "visibleFill",
            "visibleStroke",
            "visible",
            "painted",
            "fill",
            "stroke",
            "all",
        ],
        "position": Literal["static", "relative", "absolute", "fixed", "sticky"],
        # Q
        "quotes": str,
        # R
        "resize": Literal["none", "both", "horizontal", "vertical"],
        "right": str,
        # S
        "scroll-behavior": Literal["auto", "smooth"],
        "scroll-margin": str,
        "scroll-margin-block": str,
        "scroll-margin-block-end": str,
        "scroll-margin-block-start": str,
        "scroll-margin-bottom": str,
        "scroll-margin-inline": str,
        "scroll-margin-inline-end": str,
        "scroll-margin-inline-start": str,
        "scroll-margin-left": str,
        "scroll-margin-right": str,
        "scroll-margin-top": str,
        "scroll-padding": str,
        "scroll-padding-block": str,
        "scroll-padding-block-end": str,
        "scroll-padding-block-start": str,
        "scroll-padding-bottom": str,
        "scroll-padding-inline": str,
        "scroll-padding-inline-end": str,
        "scroll-padding-inline-start": str,
        "scroll-padding-left": str,
        "scroll-padding-right": str,
        "scroll-padding-top": str,
        "scroll-snap-align": Literal[
            "none",
            "start",
            "end",
            "center",
            "start end",
            "start center",
            "end center",
            "inherit",
            "initial",
            "unset",
        ],
        "scroll-snap-stop": Literal["normal", "always"],
        "scroll-snap-type": Literal[
            "none",
            "x",
            "y",
            "block",
            "inline",
            "both",
            "start",
            "end",
            "inherit",
            "initial",
            "unset",
        ],
        "shape-image-threshold": str,
        "shape-margin": str,
        "shape-outside": str,
        "tab-size": str,
        "table-layout": Literal["auto", "fixed"],
        "text-align": Literal[
            "left",
            "right",
            "center",
            "justify",
            "start",
            "end",
            "match-parent",
            "justify-all",
        ],
        "text-align-last": Literal["auto", "left", "right", "center", "justify"],
        "text-combine-upright": Literal["none", "all", "digits"],
        "text-decoration": str,
        "text-decoration-color": str,
        "text-decoration-line": Literal[
            "none", "underline", "overline", "line-through"
        ],
        "text-decoration-style": Literal["solid", "double", "dotted", "dashed", "wavy"],
        "text-emphasis": str,
        "text-emphasis-color": str,
        "text-emphasis-position": str,
        "text-emphasis-style": str,
        "text-indent": str,
        "text-justify": Literal[
            "auto",
            "inter-word",
            "inter-character",
            "none",
            "distribute",
            "distribute-all-lines",
            "inter-word",
        ],
        "text-orientation": Literal[
            "mixed", "upright", "sideways", "sideways-right", "use-glyph-orientation"
        ],
        "text-overflow": Literal["clip", "ellipsis"],
        "text-rendering": Literal[
            "auto", "optimizeSpeed", "optimizeLegibility", "geometricPrecision"
        ],
        "text-shadow": str,
        "text-transform": Literal[
            "none", "capitalize", "uppercase", "lowercase", "full-width"
        ],
        "text-underline-offset": str,
        "text-underline-position": str,
        "top": str,
        "transform": str,
        "transform-box": Literal["border-box", "fill-box", "view-box"],
        "transform-origin": str,
        "transform-style": Literal["flat", "preserve-3d"],
        "transition": str,
        "transition-delay": str,
        "transition-duration": str,
        "transition-property": Literal["all", "none"],
        "transition-timing-function": str,
        "translate": str,
        # U
        "unicode-bidi": Literal[
            "normal",
            "embed",
            "bidi-override",
            "isolate",
            "isolate-override",
            "plaintext",
        ],
        "user-select": Literal["auto", "text", "none", "contain", "all"],
        # V
        "vertical-align": Literal[
            "baseline",
            "sub",
            "super",
            "top",
            "text-top",
            "middle",
            "bottom",
            "text-bottom",
            "unset",
        ],
        "view-transition-name": str,
        "visibility": Literal["visible", "hidden", "collapse"],
        # W
        "white-space": Literal["normal", "nowrap", "pre", "pre-line", "pre-wrap"],
        "widows": str,
        "width": str,
        "will-change": str,
        "word-break": Literal["normal", "break-all", "keep-all"],
        "word-spacing": str,
        "word-wrap": Literal["normal", "break-word"],
        "writing-mode": Literal["horizontal-tb", "vertical-rl", "vertical-lr"],
        # Z
        "z-index": str,
    },
    total=False,
)

# FIXME: Currently, it is impossible to properly type nested CSS properties
# defined similar as in SCSS, it will be possible when the following PEP is
# implemented and supported by type checkers: https://peps.python.org/pep-0728/
GlobalStyles = Mapping[str | tuple[str, ...], "CSSProperties | GlobalStyles"]
"""CSS styles for elements or components which are defined by setting the ``styles``
class property.

Example usage:

    class Page(Component[AnyChildren, NoAttrs]):
        styles = {
            "body": {
                "background-color": "red",
            },
        }
"""
