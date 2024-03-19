from collections.abc import Mapping
from typing import Any

from ludic.base import ELEMENT_REGISTRY
from ludic.css import CSSProperties
from ludic.types import BaseElement, GlobalStyles

GLOBAL_STYLES_CACHE: GlobalStyles = {}


def format_styles(styles: GlobalStyles, separator: str = "\n") -> str:
    """Format styles from all registered elements.

    Args:
        styles (GlobalStyles): Styles to format.
    """
    result: list[str] = []
    nodes_to_parse: list[tuple[list[str], str | Mapping[str, Any]]] = [([], styles)]

    while nodes_to_parse:
        parents, node = nodes_to_parse.pop(0)

        content = []
        if isinstance(node, str):
            content.append(node)
        else:
            for key, value in node.items():
                if isinstance(value, str):
                    content.append(f"{key}: {value};")
                elif isinstance(value, Mapping):
                    if key.startswith("@"):
                        value = format_styles(value, separator=" ")
                    nodes_to_parse.append(([*parents, key], value))

        if content:
            result.append(f"{" ".join(parents)} {{ {" ".join(content)} }}")

    return separator.join(result)


def collect_from_components(*components: type[BaseElement]) -> GlobalStyles:
    """Global styles collector from given components.

    Example usage:

        class Page(Component[AnyChildren, NoAttrs]):

            @override
            def render(self) -> BaseElement:
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
    styles: dict[str, CSSProperties | GlobalStyles] = {}
    for component in components:
        if not component.styles:
            continue

        for key, value in component.styles.items():
            if isinstance(value, Mapping):
                styles[key] = value
    return styles


def collect_from_loaded(cache: bool = False) -> GlobalStyles:
    """Global styles collector from loaded components.

    Args:
        cache (bool): Whether to cache the result Default is False.

    Returns:
        GlobalStyles: Collected styles from loaded components.
    """
    global GLOBAL_STYLES_CACHE

    if cache and GLOBAL_STYLES_CACHE:
        return GLOBAL_STYLES_CACHE

    loaded = (
        element
        for elements in ELEMENT_REGISTRY.values()
        for element in elements
        if element.styles
    )
    result = collect_from_components(*loaded)
    if cache:
        GLOBAL_STYLES_CACHE = result
    return result
