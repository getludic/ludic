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
    _spec: type[TAttrs]

    @property
    def form_data(self) -> FormData:
        return self._form_data

    @property
    def parsers(self) -> Parsers:
        if not hasattr(self, "_parsers"):
            self._load_meta()
        return self._parsers

    @property
    def spec(self) -> type[TAttrs]:
        if not hasattr(self, "_spec"):
            self._load_meta()
        return self._spec

    def __init__(self, data: FormData, spec: type[TAttrs] | None = None) -> None:
        self._form_data = data
        if spec is not None:
            self._spec = spec

    def _load_meta(self) -> None:
        # This method cannot be part of __init__ as the __orig_class__
        # is not present at that time.
        if (
            not hasattr(self, "_spec")
            and (orig_class := getattr(self, "__orig_class__", None))
            and (bases := get_args(orig_class))
        ):
            self._spec = bases[0]
        else:
            raise TypeError(
                f"Could not collect type information from {self.__class__!r}"
            )

        hints = get_type_hints(self._spec, include_extras=True)
        self._parsers = get_annotations_metadata_of_type(
            hints,
            Callable,  # type: ignore
            default=str,
        )

    def _validate(self, attrs: dict[str, Any]) -> TAttrs:
        try:
            return check_type(attrs, self.spec)
        except TypeCheckError as err:
            raise ValidationError(f"Invalid attributes for {self.spec!r}: {err}.")

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
        result = {}
        for key, value in self.form_data.items():
            if key in self.parsers:
                try:
                    result[key] = self.parsers[key](value)
                except Exception as e:
                    raise ValidationError(
                        f"Could not parse value {value!r} with parser "
                        f"{self.parsers[key]!r}."
                    ) from e
        return result

    @override
    def validate(self) -> TAttrs:
        """Parse, validate and return attributes.

        Returns:
            TAttrs: The validated attributes.

        Raises:
            ValidationError: If the attributes are invalid.
        """
        attrs = self.parse()
        return self._validate(attrs)


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
        for compound_key, value in self.form_data.items():
            try:
                key, id_name, id_value = compound_key.split(":", 2)
            except ValueError:
                raise ValidationError(
                    "All keys in a list must contain a unique identifier."
                )
            if key not in self.parsers:
                continue

            result.setdefault(
                id_value,
                {id_name: self.parsers.get(id_name, str)(id_value)}
                if not id_name.startswith("_")
                else {},
            )
            try:
                result[id_value][key] = self.parsers[key](value)
            except Exception as e:
                raise ValidationError(
                    f"Could not parse value {value!r} with parser "
                    f"{self.parsers[key]!r}."
                ) from e
        return list(result.values())

    @override
    def validate(self) -> list[TAttrs]:
        """Parse, validate and return attributes in a list.

        Returns:
            list[TAttrs]: The validated attributes.

        Raises:
            ValidationError: If the attributes are invalid.
        """
        result = []
        for attrs in self.parse():
            result.append(self._validate(attrs))
        return result
