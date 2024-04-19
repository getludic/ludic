def attr_to_camel(name: str) -> str:
    """Convert an attribute name to camel case.

    Args:
        name (str): The attribute name.

    Returns:
        str: The attribute name in camel case.
    """
    return " ".join(value.title() for value in name.split("_"))


def text_to_kebab(name: str) -> str:
    """Convert a text to kebab case.

    Args:
        name (str): The text.

    Returns:
        str: The text in kebab case.
    """
    return "-".join(value.lower() for value in name.split())
