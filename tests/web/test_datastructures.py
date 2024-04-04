from ludic.web.datastructures import Headers, URLPath


def test_headers() -> None:
    headers = Headers({"foo": "bar", "bar": {"foo": "baz"}})

    assert headers["foo"] == "bar"
    assert headers["bar"] == '{"foo": "baz"}'


def test_url_path() -> None:
    path = URLPath("https://example.com/some/path")
    assert str(path.query(foo="bar")) == "https://example.com/some/path?foo=bar"
