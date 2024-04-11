from ludic.web.requests import join_mounts


def test_join_mounts() -> None:
    assert join_mounts("", "") == ""
    assert join_mounts("a", "b") == "a:b"
    assert join_mounts("a:b", "c") == "a:b:c"
    assert join_mounts("foo:bar", "bar:Baz") == "foo:bar:Baz"
    assert join_mounts("foo:bar:Baz", "bar:Baz:foo") == "foo:bar:Baz:foo"
