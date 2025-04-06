import builtins
import sys
from typing import Annotated, Any, Literal, TypedDict

import pytest
from starlette.datastructures import FormData

from ludic.catalog.forms import FieldMeta
from ludic.web.parsers import ListParser, Parser, ValidationError


def parse_bool(value: Literal["on", "off"]) -> bool:
    return True if value == "on" else False


class Example(TypedDict):
    sample_str: Annotated[str, FieldMeta()]
    sample_int: Annotated[int, FieldMeta(parser=int)]
    sample_bool: Annotated[bool, FieldMeta(parser=parse_bool)]


class ExampleOptional(TypedDict, total=False):
    sample_optional: Annotated[str, FieldMeta()]


class InvalidExample(TypedDict):
    sample_invalid: Annotated[int, FieldMeta()]  # missing parser=int


def test_parse_form_data() -> None:
    data = FormData({"sample_str": "test", "sample_int": "10", "sample_bool": "on"})
    assert Parser[Example](data).validate() == Example(
        sample_str="test",
        sample_int=10,
        sample_bool=True,
    )


def test_parse_invalid_form_data() -> None:
    data = FormData({"sample_str": "test", "sample_int": "10a", "sample_bool": "on"})
    with pytest.raises(ValidationError):
        _ = Parser[Example](data).validate()


def test_parse_invalid_example() -> None:
    data = FormData({"sample_invalid": "10"})
    with pytest.raises(ValidationError):
        _ = Parser[InvalidExample](data).validate()


def test_parse_empty_valid() -> None:
    data = FormData({})
    assert Parser[ExampleOptional](data).validate() == {}


def test_parse_list_form_data() -> None:
    data = FormData(
        {
            "sample_str:_index:0": "test2",
            "sample_int:_index:0": "90",
            "sample_bool:_index:0": "off",
            "sample_str:_index:1": "test1",
            "sample_int:_index:1": "10",
            "sample_bool:_index:1": "on",
        }
    )
    assert ListParser[Example](data).validate() == [
        Example(
            sample_str="test2",
            sample_int=90,
            sample_bool=False,
        ),
        Example(
            sample_str="test1",
            sample_int=10,
            sample_bool=True,
        ),
    ]


def test_parse_list_invalid_form_data() -> None:
    data = FormData(
        {
            "sample_str:_index:0": "test2",
            "sample_int:_index:0": "90abc",
            "sample_bool:_index:0": "off",
        }
    )
    with pytest.raises(ValidationError):
        _ = ListParser[Example](data).validate()


def test_parse_list_invalid_example() -> None:
    data = FormData({"sample_invalid:_intex:0": "10"})
    with pytest.raises(ValidationError):
        _ = ListParser[InvalidExample](data).validate()


def test_parse_list_empty_invalid() -> None:
    data = FormData({"sample_str": "10"})
    with pytest.raises(ValidationError):
        _ = ListParser[Example](data).validate()


def test_parse_list_empty_valid() -> None:
    data = FormData({})
    assert ListParser[ExampleOptional](data).validate() == []


def test_module_can_be_imported_without_typeguard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_import(name: str, *args: Any, **kwargs: Any) -> Any:
        if name == "typeguard":
            raise ImportError("No module named 'some_module'")
        return real_import(name, *args, **kwargs)

    real_import = builtins.__import__
    monkeypatch.setattr(builtins, "__import__", fake_import)
    sys.modules.pop("typeguard")
    sys.modules.pop("ludic.web.parsers")

    from ludic.web.parsers import check_type

    result = check_type(1, int)
    assert result == 1
