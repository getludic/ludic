from pymx.elements import Button, Div, Label


def test_button_get():
    div = Div(hx_target="this", hx_swap="outerHTML")(
        Div(Label("First Name"), ": Joe"),
        Div(Label("Last Name"), ": Blow"),
        Div(Label("Email"), ": joe@blow.com"),
        Button(hx_get="/contact/1/edit", class_="btn btn-primary")("Click To Edit"),
    )

    assert div[3].hx_get == "/contact/1/edit"
    assert div.hx_target == "this"
    assert div.as_html() == (
        '<div hx-target="this" hx-swap="outerHTML">'
            "<div><label>First Name</label>: Joe</div>"
            "<div><label>Last Name</label>: Blow</div>"
            "<div><label>Email</label>: joe@blow.com</div>"
            '<button hx-get="/contact/1/edit" class="btn btn-primary">'
                "Click To Edit"
            "</button>"
        "</div>"
    )  # fmt: skip
