from ludic.html import div, script
from ludic.types import JavaScript, Safe


def test_safe():
    assert (
        div("Hello <b>World!</b>").to_html()
        == "<div>Hello &lt;b&gt;World!&lt;/b&gt;</div>"
    )
    assert (
        div(Safe("Hello <b>World!</b>")).to_html() == "<div>Hello <b>World!</b></div>"
    )


def test_javascript():
    assert (
        div("alert('Hello World!')").to_html()
        == "<div>alert(&#x27;Hello World!&#x27;)</div>"
    )
    assert (
        script(JavaScript("alert('Hello World!')")).to_html()
        == "<script>alert('Hello World!')</script>"
    )
