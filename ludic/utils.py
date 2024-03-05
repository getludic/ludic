from typing import (
    Annotated,
    Any,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

_T = TypeVar("_T", covariant=True)


def get_element_generic_args(cls_or_obj: Any) -> tuple[type, ...] | None:
    """Get the generic arguments of the element class.

    Args:
        cls_or_obj (Any): The element to get the generic arguments of.

    Returns:
        dict[str, Any] | None: The generic arguments or :obj:`None`.
    """
    from ludic.base import BaseElement

    for base in getattr(cls_or_obj, "__orig_bases__", []):
        if issubclass(get_origin(base), BaseElement):
            return get_args(base)
    return None


def get_element_attrs_annotations(
    cls_or_obj: Any, include_extras: bool = False
) -> dict[str, Any]:
    """Get the annotations of the element.

    Args:
        cls_or_obj (type[Any]): The element to get the annotations of.
        include_extras (bool): Whether to include extra annotation info.

    Returns:
        dict[str, Any]: The attributes' annotations of the element.
    """
    if (args := get_element_generic_args(cls_or_obj)) is not None:
        return get_type_hints(args[-1], include_extras=include_extras)
    return {}


def get_annotations_metadata_of_type(
    annotations: dict[str, Any],
    expected_type: type[_T],
    default: _T | None = None,
) -> dict[str, _T]:
    """Get the metadata of the annotations with the given type.

    Args:
        annotations (dict[str, Any]): The annotations.
        expected_type (Any): The expected type.
        default (Any, optional): The default type.

    Returns:
        dict[str, Any]: The metadata.
    """
    result: dict[str, _T] = {}
    for name, annotation in annotations.items():
        if get_origin(annotation) is not Annotated:
            continue
        for metadata in annotation.__metadata__:
            if isinstance(metadata, expected_type):
                result[name] = metadata
                break
        else:
            if default is not None:
                result[name] = default
    return result
