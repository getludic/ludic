from ludic.utils import format_attr_value


def test_format_attr_value():
    assert format_attr_value("foo", "bar") == "bar"
    assert format_attr_value("foo", "bar", is_html=True) == "bar"

    assert format_attr_value("foo", 1) == "1"
    assert format_attr_value("foo", 1, is_html=True) == "1"

    assert format_attr_value("foo", True) == "true"
    assert format_attr_value("foo", True, is_html=True) == "foo"

    assert format_attr_value("foo", False) == "false"
    assert format_attr_value("foo", False, is_html=True) == ""

    assert format_attr_value("hx-confirm", True) == "true"
    assert format_attr_value("hx-confirm", True, is_html=True) == "true"

    assert format_attr_value("hx-confirm", False) == "false"
    assert format_attr_value("hx-confirm", False, is_html=True) == "false"

    assert (
        format_attr_value("style", {"color": "red", "background": "blue"})
        == "color:red;background:blue"
    )
