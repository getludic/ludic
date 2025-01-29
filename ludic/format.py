import html
import inspect
import random
import re
from collections.abc import Mapping
from contextvars import ContextVar
from functools import lru_cache
from typing import Any, Final, TypeVar, get_type_hints

T = TypeVar("T")

_EXTRACT_NUMBER_RE: Final[re.Pattern[str]] = re.compile(r"\{(\d+:id)\}")


@lru_cache
def _load_attrs_aliases() -> Mapping[str, str]:
    from ludic import attrs

    result = {}
    for name, cls in inspect.getmembers(attrs, inspect.isclass):
        if not name.endswith("Attrs"):
            continue

        hints = get_type_hints(cls, include_extras=True)
        for key, value in hints.items():
            if metadata := getattr(value, "__metadata__", None):
                for meta in metadata:
                    if isinstance(meta, attrs.Alias):
                        result[key] = str(meta)

    return result


def format_attr_value(key: str, value: Any, is_html: bool = False) -> str:
    """Format an HTML attribute with the given key and value.

    Args:
        key (str): The key of the attribute.
        value (Any): The value of the attribute, can be a string or a dictionary.
    Returns:
        str: The formatted HTML attribute.
    """

    def _html_escape(value: Any) -> str:
        if (
            is_html
            and value
            and isinstance(value, str)
            and getattr(value, "escape", True)
        ):
            return html.escape(value, False)  # type: ignore
        return str(value)

    if isinstance(value, dict):
        formatted_value = ";".join(
            f"{dict_key}:{_html_escape(dict_value)}"
            for dict_key, dict_value in value.items()
        )
    elif isinstance(value, list):
        formatted_value = " ".join(map(_html_escape, value))
    elif isinstance(value, bool):
        if is_html and not key.startswith("hx"):
            formatted_value = html.escape(key, False) if value else ""
        else:
            formatted_value = "true" if value else "false"
    else:
        formatted_value = _html_escape(value)

    return formatted_value


def format_attrs(attrs: Mapping[str, Any], is_html: bool = False) -> dict[str, Any]:
    """Format the given attributes.

        attrs = {"name": "John", "class_": "person", "is_adult": True}

    The result will be:

        >>> format_attrs(attrs)
        >>> {"name": "John", "class": "person"}

    Args:
        attrs (dict[str, Any]): The attributes to format.

    Returns:
        dict[str, Any]: The formatted attributes.
    """
    aliases = _load_attrs_aliases()
    result: dict[str, str] = {}

    for key, value in attrs.items():
        if formatted_value := format_attr_value(key, value, is_html=is_html):
            if key in aliases:
                alias = aliases[key]
            else:
                alias = key.strip("_").replace("_", "-")

            if alias in result:
                result[alias] += " " + formatted_value
            else:
                result[alias] = formatted_value
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
    parts = [_extract_match(match) for match in _EXTRACT_NUMBER_RE.split(text) if match]
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

    def extract(self, *args: Any, WrapIn: type | None = None) -> tuple[Any, ...]:
        """Extract identifiers from the given arguments.

        Example:

            with FormatContext() as ctx:
                first = ctx.append("foo")
                second = ctx.append({"bar": "baz"})
                print(ctx.extract(f"test {first} {second}"))

            ["test ", "foo", " ", {"bar": "baz"}]

        Args:
            WrapIn
            args (Any): The arguments to extract identifiers from.

        Returns:
            Any: The extracted arguments.
        """
        arguments: list[Any] = []
        for arg in args:
            if isinstance(arg, str) and (parts := extract_identifiers(arg)):
                cache = self.get()
                extracted_args = (
                    cache.pop(part) if isinstance(part, int) else part
                    for part in parts
                    if not isinstance(part, int) or part in cache
                )
                if WrapIn is not None:
                    arguments.append(WrapIn(*extracted_args))
                else:
                    arguments.extend(extracted_args)
                self._context.set(cache)
            else:
                arguments.append(arg)
        return tuple(arguments)

    def clear(self) -> None:
        """Clear the context memory."""
        self._context.set({})

    def __enter__(self) -> "FormatContext":
        return self

    def __exit__(self, *_: Any) -> None:
        self.clear()
