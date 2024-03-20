import html
import random
import re
from contextvars import ContextVar
from typing import Annotated, Any, Final, TypeVar, get_args, get_origin

from .utils import get_element_attrs_annotations

EXTRACT_NUMBER_RE: Final[re.Pattern[str]] = re.compile(r"\{(\d+:id)\}")

T = TypeVar("T")


def format_attr_value(key: str, value: Any, is_html: bool = False) -> str:
    """Format an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        str: The formatted HTML attribute.
    """
    if isinstance(value, dict):
        value = ";".join(
            f"{dict_key}:{html.escape(dict_value, False)}"
            for dict_key, dict_value in value.items()
        )
    elif isinstance(value, bool):
        if is_html and not key.startswith("hx"):
            value = html.escape(key, False) if value else ""
        else:
            value = "true" if value else "false"
    elif isinstance(value, str) and getattr(value, "escape", True):
        value = html.escape(value, False)
    return str(value)


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
        if formatted_value := format_attr_value(key, value, is_html=is_html):
            result[_get_key(key)] = formatted_value
    return result


def format_element(child: Any) -> str:
    """Default HTML formatter.

    Args:
        child (AnyChild): The HTML element or text to format.
    """
    if isinstance(child, str) and getattr(child, "escape", True):
        return html.escape(child, False)
    elif hasattr(child, "to_html"):
        return child.to_html()  # type: ignore
    else:
        return str(child)


def _extract_match(text: str | Any) -> int | str:
    if text.endswith(":id") and text[:-3].isdigit():
        return int(text[:-3])
    return str(text)


def extract_identifiers(text: str) -> list[str | int]:
    """Extract numbers from a string.

    Args:
        text (str): The string to extract numbers from.

    Returns:
        Iterable[int]: The extracted numbers.
    """
    parts = [_extract_match(match) for match in EXTRACT_NUMBER_RE.split(text) if match]
    if any(isinstance(part, int) for part in parts):
        return parts
    else:
        return []


class FormatContext:
    """Format context helper for using f-strings in elements.

    Facilitates dynamic content formatting within Ludic elements using f-strings.

    This class addresses potential memory leaks when using f-strings directly in
    element generation. Employing the 'with' statement ensures proper cleanup of
    formatting context.

    It is possible to use f-strings in elements without the contextmanager,
    however, the contextmanager clears the context (cache) at the end of the block.
    So without this manager, you can have memory leaks in your app.

    It is recommended to wrap, for example, request context with this manager.

    Example usage:

        with FormatContext():
            dom = div(f"test {b('foo')} {i('bar')}")

        assert dom.to_html() == "<div>test <b>foo</b> <i>bar</i></div>"
    """

    _context: ContextVar[dict[int, Any]]

    def __init__(self, name: str) -> None:
        self._context = ContextVar(name)

    def get(self) -> dict[int, Any]:
        try:
            return self._context.get()
        except LookupError:
            return {}

    def append(self, obj: Any) -> str:
        """Store the given object in context memory and return the identifier.

        Args:
            obj (Any): The object to store in context memory.

        Returns:
            str: The identifier of the stored object.
        """
        random_id = random.getrandbits(256)

        try:
            cache = self._context.get()
            cache[random_id] = obj
            self._context.set(cache)
        except LookupError:
            self._context.set({random_id: obj})

        return f"{{{random_id}:id}}"

    def extract(self, *args: Any) -> list[Any]:
        """Extract identifiers from the given arguments.

        Example:

            with FormatContext() as ctx:
                first = ctx.append("foo")
                second = ctx.append({"bar": "baz"})
                print(ctx.extract(f"test {first} {second}"))

            ["test ", "foo", " ", {"bar": "baz"}]

        Args:
            args (Any): The arguments to extract identifiers from.

        Returns:
            Any: The extracted arguments.
        """
        extracted_args: list[Any] = []
        for arg in args:
            if isinstance(arg, str) and (parts := extract_identifiers(arg)):
                cache = self.get()
                extracted_args.extend(
                    cache.pop(part) if isinstance(part, int) else part
                    for part in parts
                    if not isinstance(part, int) or part in cache
                )
                self._context.set(cache)
            else:
                extracted_args.append(arg)
        return extracted_args

    def clear(self) -> None:
        """Clear the context memory."""
        self._context.set({})

    def __enter__(self) -> "FormatContext":
        return self

    def __exit__(self, *_: Any) -> None:
        self.clear()
