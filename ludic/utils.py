import random
import re
import string
from html import escape
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


def random_string(n: int) -> str:
    """Generate a random string of length N using uppercase letters and digits.

    :param n: The length of the random string to be generated
    :return: A random string of length N
    """
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


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


def _format_attr_value(key: str, value: Any, html: bool = False) -> str:
    """Format an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        str: The formatted HTML attribute.
    """
    if isinstance(value, dict):
        value = ";".join(f"{dkey}:{escape(dvalue)}" for dkey, dvalue in value.items())  # type: ignore
    if isinstance(value, bool):
        if html:
            value = escape(key) if value else ""
        else:
            value = "true" if value else "false"
    return value


def _parse_attr_value(value_type: type[Any], value: str, html: bool = False) -> Any:
    """Parse an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        Any: The parsed value.
    """
    if value_type is bool:
        return True if html else value not in ("false", "off", "0")
    elif value_type is int:
        return int(value)
    elif value_type is float:
        return float(value)
    elif value_type is dict:
        return dict(part.split(":", 1) for part in value.split(";"))
    else:
        return value


def format_attrs(
    element_type: Any, attrs: dict[str, Any], html: bool = False
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
        element_type (Any): The element.
        attrs (dict[str, Any]): The attributes to format.

    Returns:
        dict[str, Any]: The formatted attributes.
    """
    hints = get_element_attrs_annotations(element_type, include_extras=True)

    def _get_key(key: str) -> str:
        if get_origin(hints[key]) is Annotated:
            args = get_args(hints[key])
            if len(args) > 1 and isinstance(args[1], str):
                return args[1]
        return key

    result = {}
    for key, value in attrs.items():
        if formatted_value := _format_attr_value(key, value, html=html):
            result[_get_key(key)] = formatted_value
    return result


def parse_attrs(
    element_type: Any, attrs: dict[str, Any], html: bool = False
) -> dict[str, Any]:
    """Parse the given attributes according to the element's attributes.

    Here is an example of TypedDict definition:

        class PersonAttrs(TypedDict):
            name: str
            class_: Annotated[str, "class"]
            is_adult: bool

    And here is the attrs that will be parsed:

        attrs = {"name": "John", "class": "person", "is_adult": "is_adult"}

    The result will be:

        >>> parse_attrs(PersonAttrs, attrs)
        >>> {"name": "John", "class_": "person", "is_adult": True}

    Args:
        element_type (type): The element class.
        attrs (dict[str, Any]): The attributes to parse.

    Returns:
        dict[str, Any]: The parsed attributes.
    """

    def _get_info(annotation: Any, default: str) -> tuple[type[Any], str]:
        if get_origin(annotation) is Annotated:
            args = get_args(annotation)
            if len(args) > 1 and isinstance(args[1], str):
                return args
        return annotation, default

    result: dict[str, Any] = {}
    for key, ann in get_element_attrs_annotations(
        element_type, include_extras=True
    ).items():
        annotation, key_alias = _get_info(ann, key)
        if (value := attrs.get(key_alias)) is not None:
            result[key] = _parse_attr_value(annotation, value, html=html)
    return result


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
