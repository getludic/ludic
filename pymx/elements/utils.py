# pyright: reportMissingTypeStubs=false
# pyright: reportUnknownVariableType=false
# pyright: reportGeneralTypeIssues=false

import random
import string
from typing import Any, TypedDict
from xml.etree.ElementTree import XMLParser

from typeguard import TypeCheckError, check_type
from typing_inspect import get_args, get_generic_bases, get_origin, is_union_type


class ParsedElement(TypedDict):
    tag: str
    children: list[str]
    attrs: dict[str, str]


def random_string(n: int) -> str:
    """Generate a random string of length N using uppercase letters and digits.

    :param n: The length of the random string to be generated
    :return: A random string of length N
    """
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


class _PyMXHandler:
    """Parse HTML elements from a string and collects them as ParsedElement's."""

    elements: list[ParsedElement | str]
    current_element: ParsedElement

    def __init__(self) -> None:
        self.elements = []
        self.current_element = ParsedElement(tag="", children=[], attrs={})

    def start(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "ROOT":
            return
        if self.current_element["tag"]:
            raise TypeError("You cannot use nested elements when using f-strings.")
        self.current_element["tag"] = tag
        self.current_element["attrs"] = dict(attrs)

    def end(self, tag: str) -> None:
        if tag == "ROOT":
            return
        self.elements.append(ParsedElement(**self.current_element))
        self.current_element = ParsedElement(tag="", children=[], attrs={})

    def data(self, data: str) -> None:
        if self.current_element["tag"]:
            self.current_element["children"].append(data)
        else:
            if self.elements and isinstance(self.elements[-1], str):
                self.elements[-1] += data
            else:
                self.elements.append(data)

    def close(self) -> list[ParsedElement | str]:
        return self.elements


def parse_elements(string: str) -> list[ParsedElement | str]:
    """Parse HTML elements from a string.

    Args:
        string (str): The string to parse.

    Returns:
        list[ParsedElement | str]: A list of parsed elements and text.
    """
    parser = XMLParser(target=_PyMXHandler())  # noqa
    parser.feed(f"<ROOT>{string}</ROOT>")
    return parser.close()


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
