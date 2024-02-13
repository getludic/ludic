def attr_to_camel(name: str) -> str:
    """Convert an attribute name to camel case.

    Args:
        name (str): The attribute name.

    Returns:
        str: The attribute name in camel case.
    """
    return " ".join(value.title() for value in name.split("_"))
