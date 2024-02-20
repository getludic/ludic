from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from typing import Any, Generic, get_args, get_type_hints, override

from starlette.datastructures import FormData
from typeguard import TypeCheckError, check_type

from ludic.types import TAttrs
from ludic.utils import get_annotations_metadata_of_type

from .exceptions import BadRequestError

Parsers = dict[str, Callable[[Any], Any]]


class ValidationError(BadRequestError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail=detail)


class BaseParser(Generic[TAttrs], metaclass=ABCMeta):
    _form_data: FormData
    _parsers: Parsers
    _attrs_type: type[dict]

    def __init__(self, data: FormData) -> None:
        self._form_data = data

    def _load_parsers(self) -> None:
        # This method cannot be part of __init__ as the __orig_class__
        # is not present at that time.
        if (orig_class := getattr(self, "__orig_class__", None)) and (
            bases := get_args(orig_class)
        ):
            self._attrs_type = bases[0]
            hints = get_type_hints(self._attrs_type, include_extras=True)

            self._parsers = get_annotations_metadata_of_type(
                hints,
                Callable,  # type: ignore
                default=str,
            )
        else:
            raise TypeError(
                f"Could not collect type information from {self.__class__!r}"
            )

    def _validate(self, attrs: dict[str, Any], attrs_type: type[dict]) -> TAttrs:
        try:
            return check_type(attrs, attrs_type)
        except TypeCheckError as err:
            raise ValidationError(f"Invalid attributes for {attrs_type!r}: {err}.")

    @abstractmethod
    def parse(self) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def validate(self) -> Any:
        raise NotImplementedError()


class Parser(BaseParser[TAttrs]):
    """A class for form data parsing and validation.

    Usage:

        @api.post("/entities")
        def create_entity(data: Validator[EntityAttrs]) -> form:
            attrs = data.validate()
            return form(...)

    Args:
        data (FormData): Form data to be parsed and validated.

    Raises:
        TypeError: The class can raise a TypeError when it was not passible
            to collect type information from generic class.
        ValidationError: The class can raise a ValidationError when parsing
            form data was not successful due to a validation error.
    """

    @override
    def parse(self) -> dict[str, Any]:
        """Parse the attributes and return them.

        The parsers used are defined in the ``Validator._parsers`` dictionary.
        Key is name of the attribute and value is the parser.

        Returns:
            dict[str, Any]: The parsed attributes.
        """
        return {
            key: self._parsers[key](value)
            for key, value in self._form_data.items()
            if key in self._parsers
        }

    @override
    def validate(self) -> TAttrs:
        """Parse, validate and return attributes.

        Returns:
            TAttrs: The validated attributes.

        Raises:
            ValidationError: If the attributes are invalid.
        """
        attrs = self.parse()
        return self._validate(attrs, self._attrs_type)


class ListParser(BaseParser[TAttrs]):
    @override
    def parse(self) -> list[dict[str, Any]]:
        """Parse a list of attributes and return them.

        The parsers used are defined in the ``Validator._parsers`` dictionary.
        Key is name of the attribute and value is the parser.

        Returns:
            list[dict[str, Any]]: The parsed attributes.
        """
        result: dict[str, dict[str, Any]] = {}
        for compound_key, value in self._form_data.items():
            try:
                key, id_name, id_value = compound_key.split(":", 2)
            except ValueError:
                raise ValidationError(
                    "All keys in a list must contain a unique identifier."
                )
            if key not in self._parsers:
                continue

            result.setdefault(
                id_value, {id_name: self._parsers.get(id_name, str)(id_value)}
            )
            result[id_value][key] = self._parsers[key](value)
        return list(result.values())

    @override
    def validate(self) -> list[TAttrs]:
        """Parse, validate and return attributes in a list.

        Returns:
            list[TAttrs]: The validated attributes.

        Raises:
            ValidationError: If the attributes are invalid.
        """
        attrs_list = self.parse()
        result = []
        for attrs in attrs_list:
            result.append(self._validate(attrs, self._attrs_type))
        return result
