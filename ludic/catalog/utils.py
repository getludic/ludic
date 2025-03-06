from collections.abc import Callable


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


def remove_whitespaces(text: str) -> str:
    """Remove leading whitespaces from a text.

    Args:
        text (str): The text.

    Returns:
        str: The text without leading whitespaces.
    """
    if not text:
        return text

    by_line = text.splitlines()
    min_whitespaces = min(len(line) - len(line.lstrip()) for line in by_line if line)
    return "\n".join(line[min_whitespaces:].rstrip() for line in by_line).strip()


def add_line_numbers(text: str, apply_fun: Callable[[str], str] = str) -> str:
    """Add line number at the beginning of each line.

    Args:
        text (str): Content to append line number.
        apply_fun (Callable[[int], str]): Call this function on each number.

    Returns:
        str: Text with number appended to each line.
    """
    lines = text.splitlines()
    max_digits = len(str(len(lines)))

    return "\n".join(
        f"{apply_fun(f'{number + 1:>{max_digits}}   ')}{line}"
        for number, line in enumerate(lines)
    )
