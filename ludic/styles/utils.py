import colorsys


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB.

    Args:
        hex_color (str): Hex color to convert.

    Returns:
        tuple[int, int, int]: RGB color.
    """
    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    if len(hex_color) == 3:
        hex_color = (
            f"{hex_color[0]}{hex_color[0]}"
            f"{hex_color[1]}{hex_color[1]}"
            f"{hex_color[2]}{hex_color[2]}"
        )

    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")

    return int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    """Convert RGB color to hex.

    Args:
        rgb (tuple[float, float, float]): RGB color to convert.

    Returns:
        str: Hex color.
    """
    return f"#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}"


def pick_readable_color_for(color: str) -> str:
    """Get lighter or darker color variant of the given one depending on the luminance.

    Args:
        color (str): Color to find the readable opposite for.

    Returns:
        str: Readable opposite of the given color.
    """
    rgb = color if isinstance(color, tuple) else hex_to_rgb(color)
    return "#000" if sum(rgb) > 400 else "#fff"


def scale_color(color: str, factor: float = 0.5) -> str:
    """Scale a color by a given factor.

    Args:
        color (str): Color to scale.
        factor (float, optional): Scaling factor. Defaults to 0.5.

    Returns:
        str: Scaled color.
    """
    rgb = color if isinstance(color, tuple) else hex_to_rgb(color)
    hue, luminance, saturation = colorsys.rgb_to_hls(*rgb)

    if factor < 1:
        new_luminance = luminance * factor
    else:
        new_luminance = luminance + (255 - luminance) * (factor - 1)

    result = colorsys.hls_to_rgb(hue, min(255, max(1, new_luminance)), saturation)
    return rgb_to_hex(result)


def darken_color(color: str, factor: float = 0.5) -> str:
    """Darken a color by a given factor.

    Args:
        color (str): Color to darken.
        factor (float, optional): Darkening factor. Defaults to 0.5.

    Returns:
        : Darkened color.
    """
    return scale_color(color, min(1, max(0, 1 - factor)))


def lighten_color(color: str, factor: float = 0.5) -> str:
    """Lighten a color by a given factor.

    Args:
        color (str): Color to lighten.
        factor (float, optional): Lightening factor. Defaults to 0.5.

    Returns:
        : Lightened color.
    """
    return scale_color(color, max(1, min(2, 1 + factor)))


def first_not_none(*values: float | int | None) -> float | int:
    return next((value for value in values if value is not None), 0)


def clamp(min: str, val: str, max: str) -> str:
    return f"clamp({min}, {val}, {max})"
