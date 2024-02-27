from typing import Any

from ludic.base import _ELEMENT_REGISTRY
from ludic.html import style
from ludic.types import BaseElement, GlobalStyles, Safe


def format_styles(styles: GlobalStyles) -> str:
    """Format styles from all registered elements."""
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
    """Global styles collector from all elements."""

    _styles: GlobalStyles

    def __init__(self, extra_styles: GlobalStyles | None = None) -> None:
        self._styles = extra_styles or {}
        self.collect()

    @property
    def children(self) -> tuple:
        return ()

    @property
    def attrs(self) -> GlobalStyles:
        return self._styles

    def collect(self) -> None:
        """Collect all styles from all registered elements."""
        for elements in _ELEMENT_REGISTRY.values():
            for element in elements:
                if not element.styles:
                    continue

                for key, value in element.styles.items():
                    if isinstance(value, dict):
                        self._styles[key] = value

    def render(self) -> style:
        return style(Safe(format_styles(self._styles)))
