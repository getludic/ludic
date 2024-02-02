import random
import string
from typing import Any


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
