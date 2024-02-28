from typing import Any

from ludic.base import _ELEMENT_REGISTRY
from ludic.html import style
from ludic.types import BaseElement, GlobalStyles, Safe


def format_styles(styles: GlobalStyles) -> str:
    """Format styles from all registered elements.

    Args:
        styles (GlobalStyles): Styles to format.
    """
    result: list[str] = ["\n"]
    nodes_to_parse: list[tuple[list[str], dict[str, Any]]] = [([], styles)]

    while nodes_to_parse:
        parents, node = nodes_to_parse.pop(0)

        content = []
        for key, value in node.items():
            if isinstance(value, str):
                content.append(f"  {key}: {value};")
            elif isinstance(value, dict):
                nodes_to_parse.append(([*parents, key], value))

        if content:
            result.append(f"{" ".join(parents)} {{\n{"\n".join(content)}\n}}\n")

    return "".join(result)


class ComponentsStyles(BaseElement):
    """Global styles collector from all elements.

    Example usage:

        class Page(Component[AllowAny, NoAttrs]):

            @override
            def render(self) -> BaseElement:
                return html(
                    head(
                        title("An example Example"),
                        ComponentsStyles(),
                    ),
                    body(
                        *self.children,
                    ),
                )

    This components would ren an HTML page containing the ``<style>`` element
    with the styles from all components.
    """

    attrs: GlobalStyles

    def __init__(self, extra_styles: GlobalStyles | None = None) -> None:
        self.attrs = extra_styles or {}
        self.children = ()
        self.collect()

    def collect(self) -> None:
        """Collect all styles from all registered elements."""
        for elements in _ELEMENT_REGISTRY.values():
            for element in elements:
                if not element.styles:
                    continue

                for key, value in element.styles.items():
                    if isinstance(value, dict):
                        self.attrs[key] = value

    def render(self) -> style:
        return style(Safe(format_styles(self.attrs)))
