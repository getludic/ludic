from ludic.html import div, script
from ludic.types import JavaScript, Safe


def test_safe() -> None:
    assert (
        div("Hello <b>World!</b>").to_html()
        == "<div>Hello &lt;b&gt;World!&lt;/b&gt;</div>"
    )
    assert (
        div(Safe("Hello <b>World!</b>")).to_html() == "<div>Hello <b>World!</b></div>"
    )


def test_javascript() -> None:
    assert (
        div("document.write('<h2>HTML</h2>');").to_html()
        == "<div>document.write('&lt;h2&gt;HTML&lt;/h2&gt;');</div>"
    )
    assert (
        script(JavaScript("document.write('<h2>HTML</h2>');")).to_html()
        == "<script>document.write('<h2>HTML</h2>');</script>"
    )
