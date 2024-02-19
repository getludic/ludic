from collections.abc import Callable
from typing import Any, Generic, get_args, get_type_hints

from starlette.datastructures import FormData
from typeguard import TypeCheckError, check_type

from ludic.types import TAttrs
from ludic.utils import get_annotations_metadata_of_type


class Parser(Generic[TAttrs]):
    _dict_class: type[dict]

    data: FormData
    parsers: dict[str, Callable[[Any], Any]]

    def __init__(self, data: FormData) -> None:
        self.data = data

    def __post_init__(self) -> None:
        if (orig_class := getattr(self, "__orig_class__", None)) and (
            bases := get_args(orig_class)
        ):
            self._dict_class = bases[0]

            hints = get_type_hints(self._dict_class, include_extras=True)
            self.parsers = get_annotations_metadata_of_type(
                hints,
                Callable,  # type: ignore
                default=str,
            )
        else:
            raise TypeError(
                f"Could not collect type information from {self.__class__!r}"
            )

    def validate(self, attrs: dict[str, Any]) -> TAttrs:
        """Validate the given attributes.

        Args:
            obj (Parser): The parser instance.
            attrs (dict[str, Any]): The attributes to validate.

        Returns:
            TAttrs: The validated attributes.
        """
        try:
            return check_type(attrs, self._dict_class)
        except TypeCheckError as err:
            raise TypeError(f"Invalid attributes for {self._dict_class!r}: {err}.")

    def parse(self) -> TAttrs:
        """Parse the data.

        Returns:
            TAttrs: The parsed data.
        """
        attrs = {
            key: self.parsers.get(key, str)(value)
            for key, value in self.data.items()
            if key in self.parsers
        }
        return self.validate(attrs)
