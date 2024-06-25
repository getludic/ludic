from collections.abc import Mapping, MutableMapping
from typing import Any

from ludic.base import BaseElement

from .themes import Theme, get_default_theme
from .types import CSSProperties, GlobalStyles

GLOBAL_STYLES_CACHE: MutableMapping[str, GlobalStyles] = {}


def format_styles(styles: GlobalStyles, separator: str = "\n") -> str:
    """Format styles from all registered elements.

    Args:
        styles (GlobalStyles): Styles to format.
    """
    result: list[str] = []
    nodes_to_parse: list[
        tuple[list[str], str | Mapping[str | tuple[str, ...], Any]]
    ] = [([], styles)]

    while nodes_to_parse:
        parents, node = nodes_to_parse.pop(0)

        content = []
        if isinstance(node, str):
            content.append(node)
        else:
            for key, value in node.items():
                if isinstance(value, str | int | float):
                    content.append(f"{key}: {value};")
                elif isinstance(value, Mapping):
                    keys = (key,) if isinstance(key, str | int | float) else key
                    for key in keys:
                        if key.startswith("@"):
                            value = format_styles(value, separator=" ")
                        nodes_to_parse.append(([*parents, key], value))

        if content:
            result.append(f"{" ".join(parents)} {{ {" ".join(content)} }}")

    return separator.join(result)


def from_components(
    *components: type["BaseElement"], theme: Theme | None = None
) -> GlobalStyles:
    """Global styles collector from given components.

    Example usage:

        class Page(Component[AnyChildren, NoAttrs]):

            @override
            def render(self) -> html:
                return html(
                    head(
                        title("An example Example"),
                        styles(collect_from_components()),
                    ),
                    body(
                        *self.children,
                    ),
                )

    This would render an HTML page containing the ``<style>`` element
    with the styles the given components.
    """
    theme = theme or get_default_theme()
    all_styles: dict[str | tuple[str, ...], CSSProperties | GlobalStyles] = {}

    for component in components:
        styles = getattr(component, "styles", {})

        if not isinstance(styles, Mapping):
            continue
        elif hasattr(styles, "context"):
            styles.context["theme"] = theme

        for key, value in styles.items():
            if isinstance(value, Mapping):
                all_styles[key] = value

    return all_styles


def from_loaded(cache: bool = False, theme: Theme | None = None) -> GlobalStyles:
    """Global styles collector from loaded components.

    Args:
        cache (bool): Whether to cache the result Default is False.

    Returns:
        GlobalStyles: Collected styles from loaded components.
    """
    from ludic.components import COMPONENT_REGISTRY

    global GLOBAL_STYLES_CACHE
    theme = theme or get_default_theme()

    if cache and GLOBAL_STYLES_CACHE.get(theme.name):
        return GLOBAL_STYLES_CACHE[theme.name]

    loaded = (
        element for elements in COMPONENT_REGISTRY.values() for element in elements
    )
    result = from_components(*loaded, theme=theme)
    if cache:
        GLOBAL_STYLES_CACHE[theme.name] = result
    return result
