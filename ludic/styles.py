from typing import Any

from ludic.base import _ELEMENT_REGISTRY
from ludic.types import BaseElement, GlobalStyles


def format_styles(styles: GlobalStyles) -> str:
    """Format styles from all registered elements.

    Args:
        styles (GlobalStyles): Styles to format.
    """
    result: list[str] = []
    nodes_to_parse: list[tuple[list[str], dict[str, Any]]] = [([], styles)]

    while nodes_to_parse:
        parents, node = nodes_to_parse.pop(0)

        content = []
        for key, value in node.items():
            if isinstance(value, str):
                content.append(f"{key}: {value};")
            elif isinstance(value, dict):
                nodes_to_parse.append(([*parents, key], value))

        if content:
            result.append(f"{" ".join(parents)} {{ {" ".join(content)} }}\n")

    return "".join(result).rstrip()


def collect_from_components(*components: type[BaseElement]) -> GlobalStyles:
    """Global styles collector from given components.

    Example usage:

        class Page(Component[AllowAny, NoAttrs]):

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
    styles: GlobalStyles = {}
    for component in components:
        if not component.styles:
            continue

        for key, value in component.styles.items():
            if isinstance(value, dict):
                styles[key] = value
    return styles


def collect_from_loaded() -> GlobalStyles:
    """Global styles collector from loaded components."""
    loaded = (
        element
        for elements in _ELEMENT_REGISTRY.values()
        for element in elements
        if element.styles
    )
    return collect_from_components(*loaded)
