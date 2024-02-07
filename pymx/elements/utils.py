# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownVariableType=false
# pyright: reportGeneralTypeIssues=false

import html
import random
import re
import string
from typing import Any, TypedDict

from typeguard import TypeCheckError, check_type
from typing_inspect import get_args, get_generic_bases, get_origin, is_union_type

ELEMENTS_REGEX = re.compile(
    r"([^<]*)<(\w+)(\s+[^>]*)?/>([^<]*)|([^<]*)<(\w+)(\s+[^>]*)?>(.*?)</\6>([^<]*)"
)
ATTRIBUTES_REGEX = re.compile(r'(\w+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')')


class ParsedElement(TypedDict):
    tag: str
    children: list[str]
    attributes: dict[str, str]


def random_string(n: int) -> str:
    """Generate a random string of length N using uppercase letters and digits.

    :param n: The length of the random string to be generated
    :return: A random string of length N
    """
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


def parse_elements(string: str) -> list[ParsedElement | str]:
    """Parse HTML elements from a string.

    Args:
        string (str): The string to parse.

    Returns:
        list[ParsedElement | str]: A list of parsed elements and text.
    """
    matches = ELEMENTS_REGEX.findall(string)
    if not matches:
        return [string] if string else []

    elements: list[ParsedElement | str] = []
    for match in matches:
        if match[1]:  # self-closing tag
            tag = match[1]
            raw_attributes = match[2]
            before_text = match[0]
            children = []
            after_text = match[3]
        else:  # tag with content
            tag = match[5]
            raw_attributes = match[6]
            before_text = match[4]
            if ELEMENTS_REGEX.match(match[7]):
                raise TypeError("Nested elements are not allowed.")
            children = [match[7]]
            after_text = match[8]

        attributes = {}
        if raw_attributes:
            attribute_matches = ATTRIBUTES_REGEX.findall(raw_attributes)
            attributes = {
                attr[0]: attr[1] if attr[1] else attr[2] for attr in attribute_matches
            }

        if before_text:
            elements.append(before_text)
        element = ParsedElement(tag=tag, attributes=attributes, children=children)
        elements.append(element)
        if after_text:
            elements.append(after_text)

    return elements


def format_html_attribute(key: str, value: Any) -> str:
    """Format an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        str: The formatted HTML attribute.
    """
    if isinstance(value, dict):
        value = ";".join(f"{dkey}:{dvalue}" for dkey, dvalue in value.items())
    return f'{key.rstrip("_").replace("_", "-")}="{value}"'


def format_attribute(key: str, value: Any) -> str:
    """Format the attribute key and value into a string.

    Args:
        key (str): The attribute key.
        value (Any): The attribute value.

    Returns:
        str: The formatted attribute string.
    """
    return f'{key.rstrip("_").replace("_", "-")}="{value}"'


def get_element_generic_args(cls_or_obj: Any) -> tuple[type, ...] | None:
    """Get the generic arguments of the element class.

    Args:
        cls_or_obj (Any): The element to get the generic arguments of.

    Returns:
        dict[str, Any] | None: The generic arguments or :obj:`None`.
    """
    from pymx.elements import Element

    for base in get_generic_bases(cls_or_obj):
        if issubclass(get_origin(base), Element):  # type: ignore
            return get_args(base)
    return None


def get_element_attributes(cls_or_obj: Any) -> dict[str, Any]:
    """Get the annotations of the element.

    Args:
        cls (type[Any]): The element to get the annotations of.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        return args[-1].__annotations__
    return {}


def validate_attributes(cls_or_obj: Any, values: dict[str, Any]) -> None:
    """Check if the given values are valid for the given class.

    Args:
        cls (type): The expected type of the values.
        values (dict[str, Any]): The values to check.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        try:
            check_type(values, args[-1])
        except TypeCheckError as err:
            raise TypeError(f"Invalid attributes for {cls_or_obj}.") from err


def validate_elements(cls_or_obj: Any, elements: tuple[Any, ...]) -> None:
    """Check if the given elements are valid for the given class.

    Args:
        cls (type): The expected type of the elements.
        elements (tuple[Any, ...]): The elements to check.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        types = args[:-1]
        if len(types) == 0:
            if len(elements) != 0:
                raise TypeError(
                    f"The element {cls_or_obj!r} doesn't expect any elements."
                )
        elif len(types) > 1 or is_union_type(types[0]):
            if len(types) != len(elements):
                raise TypeError(
                    f"The element {cls_or_obj!r} got an invalid number of elements."
                )
            for element, type_ in zip(elements, types, strict=True):
                check_type(element, type_)
        else:
            try:
                check_type(elements, types)
            except TypeCheckError as err:
                raise TypeError(f"Invalid elements for {cls_or_obj!r}.") from err


def default_html_formatter(child: Any) -> str:
    """Default HTML formatter.

    Args:
        child (Any): The HTML element or text to format.
    """
    if isinstance(child, str):
        return html.escape(child)
    else:
        return str(child)
