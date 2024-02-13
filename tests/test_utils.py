import pytest

from ludic.utils import parse_elements


def test_empty_string():
    string = ""
    parsed = parse_elements(string)
    assert parsed == []


def test_text_only():
    string = "Some text here"
    parsed = parse_elements(string)
    assert parsed == ["Some text here"]


def test_single_self_closing_element():
    string = "<element />"
    parsed = parse_elements(string)
    assert parsed == [{"tag": "element", "attrs": {}, "children": []}]


def test_single_element_with_attributes():
    string = 'before <element attribute="value">content</element> after'
    parsed = parse_elements(string)
    assert parsed == [
        "before ",
        {
            "tag": "element",
            "attrs": {"attribute": "value"},
            "children": ["content"],
        },
        " after",
    ]


def test_single_element_with_nested_text():
    string = "<element>content</element>"
    parsed = parse_elements(string)
    assert parsed == [{"tag": "element", "attrs": {}, "children": ["content"]}]


def test_single_element_with_nested_element():
    string = "<parent><child/></parent>"
    with pytest.raises(TypeError):
        parse_elements(string)


def test_multiple_elements():
    string = "<first />Some text<second attribute='value' />More text"
    parsed = parse_elements(string)
    assert parsed == [
        {"tag": "first", "attrs": {}, "children": []},
        "Some text",
        {"tag": "second", "attrs": {"attribute": "value"}, "children": []},
        "More text",
    ]


def test_multiple_pair_elements():
    string = (
        '<first />Some text<second attribute="value">Another text</second>More text'
    )
    parsed = parse_elements(string)
    assert parsed == [
        {"tag": "first", "attrs": {}, "children": []},
        "Some text",
        {
            "tag": "second",
            "attrs": {"attribute": "value"},
            "children": ["Another text"],
        },
        "More text",
    ]


def test_nested_elements():
    with pytest.raises(TypeError):
        parse_elements("<parent><child>content</child></parent>")
    with pytest.raises(TypeError):
        parse_elements("<parent><child attribute='value'>content</child></parent>")
    with pytest.raises(TypeError):
        parse_elements("<parent><child attribute='value' /></parent>")
