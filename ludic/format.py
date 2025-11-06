import html
import inspect
import itertools
from collections.abc import Mapping
from functools import lru_cache
from string.templatelib import Interpolation
from string.templatelib import Template as Template
from typing import Any, TypeVar, get_type_hints

T = TypeVar("T")


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


def extract_dataset_attrs(attrs: Mapping[str, Any]) -> Mapping[str, Any]:
    """Converts "dataset" attributes to "data-*" attributes names.

    Args:
        attrs (Mapping[str, Any]): A dictionary containing HTML attributes.

    Returns:
        Mapping[str, Any]: A dictionary containing extracted data-* attributes.

    Raises:
        TypeError: If the 'dataset' parameter is not a dict.
    """
    extracted_attrs = {}
    if dataset_attrs := attrs.get("dataset"):
        if not isinstance(dataset_attrs, dict):
            raise TypeError(
                f"The 'dataset' parameter must be a dict, "
                f"got {type(dataset_attrs).__name__}"
            )
        for key, value in dataset_attrs.items():
            extracted_attrs[f"data-{key}"] = value
    return extracted_attrs


def extract_raw_attrs(attrs: Mapping[str, Any]) -> Mapping[str, Any]:
    """Extracts raw attributes that bypass underscore-to-dash conversion.

    This is useful for libraries like Datastar that use underscores in their DSL.

    Args:
        attrs (Mapping[str, Any]): A dictionary containing HTML attributes.

    Returns:
        Mapping[str, Any]: A dictionary containing raw attributes with keys as-is.

    Raises:
        TypeError: If the 'attrs' parameter is not a dict.
    """
    extracted_attrs = {}
    if raw_attrs := attrs.get("attrs"):
        if not isinstance(raw_attrs, dict):
            raise TypeError(
                f"The 'attrs' parameter must be a dict, got {type(raw_attrs).__name__}"
            )
        extracted_attrs.update(raw_attrs)
    return extracted_attrs


def format_attrs(attrs: Mapping[str, Any], is_html: bool = False) -> dict[str, Any]:
    """Format the given attributes.

        attrs = {"name": "John", "class_": "person", "is_adult": True}

    The result will be:

        >>> format_attrs(attrs)
        >>> {"name": "John", "class": "person"}

    Args:
        attrs (Mapping[str, Any]): The attributes to format.

    Returns:
        Mapping[str, Any]: The formatted attributes.
    """
    aliases = _load_attrs_aliases()
    result: dict[str, str] = {}
    dataset_attrs = extract_dataset_attrs(attrs)
    raw_attrs = extract_raw_attrs(attrs)

    for key, value in itertools.chain(attrs.items(), dataset_attrs.items()):
        if key in ("dataset", "attrs"):
            continue
        if formatted_value := format_attr_value(key, value, is_html=is_html):
            if key in aliases:
                alias = aliases[key]
            else:
                alias = key.strip("_").replace("_", "-")

            if alias in result:
                result[alias] += " " + formatted_value
            else:
                result[alias] = formatted_value

    # Add raw attributes without underscore-to-dash conversion
    for key, value in raw_attrs.items():
        if formatted_value := format_attr_value(key, value, is_html=is_html):
            if key in result:
                result[key] += " " + formatted_value
            else:
                result[key] = formatted_value

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


def process_template(template: Any, wrap_in: type | None = None) -> tuple[Any, ...]:
    """Process a t-string template into a tuple of children.

    This function processes Python 3.14 t-string Template objects, extracting
    both static string parts and dynamic interpolated values. This replaces the
    old FormatContext system.

    Example usage:

        dom = div(t"test {b('foo')} {i('bar')}")
        # Internally processes to: div("test ", b('foo'), " ", i('bar'))

    Args:
        template: The Template object from a t-string literal.
        wrap_in: Optional element type to wrap the processed parts in.

    Returns:
        tuple[Any, ...]: A tuple of children elements and strings.
    """
    # Template objects are iterable, yielding str or Interpolation objects
    parts: list[Any] = []
    for part in template:
        if isinstance(part, str):
            # Static string part
            if part:  # Only add non-empty strings
                parts.append(part)
        elif isinstance(part, Interpolation):
            # Dynamic interpolated value
            value = part.value
            parts.append(value)
        else:
            # Fallback for unexpected types
            parts.append(part)

    if wrap_in is not None:
        return (wrap_in(*parts),)

    return tuple(parts)
