from .base import _ELEMENT_REGISTRY, AnyElement  # type: ignore
from .utils import parse_element as _base_parse_element


def parse_element(tree: str) -> AnyElement:
    """Parse HTML elements from a string.

    Args:
        tree (str): The string to parse.

    Returns:
        list[AnyElement]: A list of parsed elements and text.
    """
    return _base_parse_element(tree, _ELEMENT_REGISTRY)
