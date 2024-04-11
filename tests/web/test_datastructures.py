from ludic.web.datastructures import Headers


def test_headers() -> None:
    headers = Headers({"foo": "bar", "bar": {"foo": "baz"}})

    assert headers["foo"] == "bar"
    assert headers["bar"] == '{"foo": "baz"}'
