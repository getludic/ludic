import html
import re
from typing import (
    Annotated,
    Any,
    Final,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

_T = TypeVar("_T", covariant=True)

EXTRACT_NUMBER_RE: Final[re.Pattern] = re.compile(r"\{(\d+):id\}")


def extract_identifiers(text: str) -> list[str | int]:
    """Extract numbers from a string.

    Args:
        text (str): The string to extract numbers from.

    Returns:
        Iterable[int]: The extracted numbers.
    """
    return [
        int(match) if str(match).isdigit() else match
        for match in EXTRACT_NUMBER_RE.split(text)
        if match
    ]


def get_element_generic_args(cls_or_obj: Any) -> tuple[type, ...] | None:
    """Get the generic arguments of the element class.

    Args:
        cls_or_obj (Any): The element to get the generic arguments of.

    Returns:
        dict[str, Any] | None: The generic arguments or :obj:`None`.
    """
    from ludic.base import BaseElement

    for base in getattr(cls_or_obj, "__orig_bases__", []):
        if issubclass(get_origin(base), BaseElement):
            return get_args(base)
    return None


def get_element_attrs_annotations(
    cls_or_obj: Any, include_extras: bool = False
) -> dict[str, Any]:
    """Get the annotations of the element.

    Args:
        cls_or_obj (type[Any]): The element to get the annotations of.
        include_extras (bool): Whether to include extra annotation info.

    Returns:
        dict[str, Any]: The attributes' annotations of the element.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        return get_type_hints(args[-1], include_extras=include_extras)
    return {}


def get_annotations_metadata_of_type(
    annotations: dict[str, Any],
    expected_type: type[_T],
    default: _T | None = None,
) -> dict[str, _T]:
    """Get the metadata of the annotations with the given type.

    Args:
        annotations (dict[str, Any]): The annotations.
        expected_type (Any): The expected type.
        default (Any, optional): The default type.

    Returns:
        dict[str, Any]: The metadata.
    """
    result: dict[str, _T] = {}
    for name, annotation in annotations.items():
        if get_origin(annotation) is not Annotated:
            continue
        for metadata in annotation.__metadata__:
            if isinstance(metadata, expected_type):
                result[name] = metadata
                break
        else:
            if default is not None:
                result[name] = default
    return result


def _format_attr_value(key: str, value: Any, is_html: bool = False) -> str:
    """Format an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        str: The formatted HTML attribute.
    """
    if isinstance(value, dict):
        value = ";".join(
            f"{dict_key}:{html.escape(dict_value)}"
            for dict_key, dict_value in value.items()
        )
    elif isinstance(value, bool):
        if is_html:
            value = html.escape(key) if value else ""
        else:
            value = "true" if value else "false"
    elif getattr(value, "escape", True):
        value = html.escape(value)
    return value


def format_attrs(
    attrs_type: Any, attrs: dict[str, Any], is_html: bool = False
) -> dict[str, Any]:
    """Format the given attributes according to the element's attributes.

    Here is an example of TypedDict definition:

        class PersonAttrs(TypedDict):
            name: str
            class_: Annotated[str, "class"]
            is_adult: bool

    And here is the attrs that will be formatted:

        attrs = {"name": "John", "class_": "person", "is_adult": True}

    The result will be:

        >>> format_attrs(PersonAttrs, attrs)
        >>> {"name": "John", "class": "person"}

    Args:
        attrs_type (Any): The element.
        attrs (dict[str, Any]): The attributes to format.

    Returns:
        dict[str, Any]: The formatted attributes.
    """
    hints = get_element_attrs_annotations(attrs_type, include_extras=True)

    def _get_key(key: str) -> str:
        if get_origin(hints[key]) is Annotated:
            args = get_args(hints[key])
            if len(args) > 1 and isinstance(args[1], str):
                return args[1]
        return key

    result = {}
    for key, value in attrs.items():
        if formatted_value := _format_attr_value(key, value, is_html=is_html):
            result[_get_key(key)] = formatted_value
    return result


def format_element(child: Any) -> str:
    """Default HTML formatter.

    Args:
        child (AnyChild): The HTML element or text to format.
    """
    if isinstance(child, str) and getattr(child, "escape", True):
        return html.escape(child)
    elif hasattr(child, "to_html"):
        return child.to_html()
    else:
        return str(child)
