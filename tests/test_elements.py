from pymx.elements import (
    a,
    button,
    div,
    label,
    p,
    table,
    tbody,
    td,
    th,
    thead,
    tr,
)


def test_paragraph():
    paragraph = p("Hello, World!")
    assert paragraph.to_html() == "<p>Hello, World!</p>"


def test_link():
    link = a(href="https://example.com")("A link!")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'


def test_table():
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
                td(style={"color": "red", "height": "100px"})("Cell 1"),
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


def test_button_get():
    dom = div(hx_target="this", hx_swap="outerHTML")(
        div(label("First Name"), ": Joe"),
        div(label("Last Name"), ": Blow"),
        div(label("Email"), ": joe@blow.com"),
        button(hx_get="/contact/1/edit", class_="btn btn-primary")("Click To Edit"),
    )

    assert dom[3].hx_get == "/contact/1/edit"  # type: ignore
    assert dom[3][0] == "Click To Edit"  # type: ignore
    assert dom.hx_target == "this"
    assert dom.to_html() == (
        '<div hx-target="this" hx-swap="outerHTML">'
            "<div><label>First Name</label>: Joe</div>"
            "<div><label>Last Name</label>: Blow</div>"
            "<div><label>Email</label>: joe@blow.com</div>"
            '<button hx-get="/contact/1/edit" class="btn btn-primary">'
                "Click To Edit"
            "</button>"
        "</div>"
    )  # fmt: skip
