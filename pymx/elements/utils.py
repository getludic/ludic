import random
import string
import warnings
from typing import Any

from typeguard import TypeCheckError, check_type
from typing_inspect import (  # type: ignore
    get_args,
    get_generic_bases,
    get_origin,
)


def random_string(n: int) -> str:
    """Generate a random string of length N using uppercase letters and digits.

    :param n: The length of the random string to be generated
    :return: A random string of length N
    """
    return "".join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )


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
        if issubclass(get_origin(base), Element):
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
        element_types = args[:-1]
        has_infinite_children = get_args(args[0]) and get_args(args[0])[-1] is Ellipsis

        try:
            if not has_infinite_children:
                for idx, element in enumerate(elements):
                    check_type(element, element_types[idx])
            else:
                with warnings.catch_warnings(action="ignore"):
                    check_type(elements, element_types)
        except TypeCheckError as err:
            raise TypeError(f"Invalid children for {cls_or_obj}.") from err
