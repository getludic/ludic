from ludic.css import CSSProperties
from ludic.html import (
    a,
    b,
    button,
    div,
    i,
    label,
    p,
    script,
    span,
    table,
    tbody,
    td,
    th,
    thead,
    tr,
)


def test_empty_element() -> None:
    dom = div()
    assert dom.to_html() == "<div />"
    assert dom.to_string() == "<div />"

    dom2 = p("")
    assert dom2.to_html() == "<p></p>"
    assert dom2.to_string() == "<p></p>"

    dom3 = script()
    assert dom3.to_html() == "<script></script>"
    assert dom3.to_string() == "<script />"


def test_html_paragraph() -> None:
    paragraph = p(f"Hello, World! {b("Something bold")} and {i("Something italic")}")
    assert paragraph.to_html() == (
        "<p>Hello, World! <b>Something bold</b> and <i>Something italic</i></p>"
    )
    assert paragraph.to_string() == (
        "<p>\n"
        "  Hello, World! \n"
        "  <b>Something bold</b>\n"
        "   and \n"
        "  <i>Something italic</i>\n"
        "</p>"
    )  # fmt: skip


def test_html_link() -> None:
    link = a("A link!", href="https://example.com")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'
    assert link.to_string() == (
        '<a href="https://example.com">\n'
        "  A link!\n"
        "</a>"
    )  # fmt: skip


def test_html_table() -> None:
    dom = table(
        thead(
            tr(
                th("Header 1"),
                th("Header 2"),
                th("Header 3"),
            )
        ),
        tbody(
            tr(
                td("Cell 1", style=CSSProperties(color="red", height="100px")),
                td("Cell 2"),
                td("Cell 3"),
            ),
        ),
    )

    assert dom.to_html() == (
        "<table>"
            "<thead>"
                "<tr>"
                    "<th>Header 1</th>"
                    "<th>Header 2</th>"
                    "<th>Header 3</th>"
                "</tr>"
            "</thead>"
            "<tbody>"
                "<tr>"
                    '<td style="color:red;height:100px">Cell 1</td>'
                    "<td>Cell 2</td>"
                    "<td>Cell 3</td>"
                "</tr>"
            "</tbody>"
        "</table>"
    )  # fmt: skip


def test_button_get() -> None:
    dom = div(
        div(label("First Name"), ": Joe"),
        div(label("Last Name"), ": Blow"),
        div(label("Email"), ": joe@blow.com"),
        button(
            "Click To Edit",
            class_="btn btn-primary",
            hx_get="/contact/1/edit",
        ),
        hx_target="this",
        hx_swap="outerHTML",
    )

    assert isinstance(dom.children[3], button)
    assert dom.children[3].attrs.get("hx_get") == "/contact/1/edit"
    assert dom.children[3].children[0] == "Click To Edit"
    assert dom.attrs.get("hx_target") == "this"
    assert dom.to_html() == (
        '<div hx-target="this" hx-swap="outerHTML">'
            "<div><label>First Name</label>: Joe</div>"
            "<div><label>Last Name</label>: Blow</div>"
            "<div><label>Email</label>: joe@blow.com</div>"
            '<button class="btn btn-primary" hx-get="/contact/1/edit">'
                "Click To Edit"
            "</button>"
        "</div>"
    )  # fmt: skip
    assert dom.to_string() == (
        '<div hx-target="this" hx-swap="outerHTML">\n'
        "  <div>\n"
        "    <label>First Name</label>\n"
        "    : Joe\n"
        "  </div>\n"
        "  <div>\n"
        "    <label>Last Name</label>\n"
        "    : Blow\n"
        "  </div>\n"
        "  <div>\n"
        "    <label>Email</label>\n"
        "    : joe@blow.com\n"
        "  </div>\n"
        '  <button class="btn btn-primary" hx-get="/contact/1/edit">\n'
        "    Click To Edit\n"
        "  </button>\n"
        "</div>"
    )


def test_expand_nested() -> None:
    div_dom = div(p(1), p(2), p(3))
    span_dom = span(*div_dom)

    assert div_dom.text == span_dom.text == "123"
    assert span_dom.to_html() == "<span><p>1</p><p>2</p><p>3</p></span>"


def test_repr_and_str() -> None:
    dom = div(p(1), p(2), p(3), id="test")
    assert repr(dom) == '<div id="test"><p>1</p><p>2</p><p>3</p></div>'
    assert str(dom) == (
        '<div id="test">\n'
        "  <p>1</p>\n"
        "  <p>2</p>\n"
        "  <p>3</p>\n"
        "</div>"
    )  # fmt: skip
