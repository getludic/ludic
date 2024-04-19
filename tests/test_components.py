from ludic.catalog.forms import Form, InputField, TextAreaField
from ludic.catalog.items import Key, Pairs, Value
from ludic.catalog.navigation import Navigation, NavItem
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.catalog.typography import Link, Paragraph
from ludic.html import b


def test_link() -> None:
    link = Link("A link!", to="https://example.com")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'


def test_paragraph() -> None:
    paragraph = Paragraph(
        "Hello, how ",
        b("are you"),
        "? Click ",
        Link("here", to="https://example.com"),
        ".",
    )
    assert isinstance(paragraph.children[3], Link)
    assert paragraph.children[3].attrs["to"] == "https://example.com"
    assert paragraph.to_string(pretty=False) == (
        "<Paragraph>"
          'Hello, how <b>are you</b>? Click <Link to="https://example.com">here</Link>.'
        "</Paragraph>"
    )  # fmt: skip
    assert paragraph.to_html() == (
        '<p>'
            'Hello, how <b>are you</b>? '
            'Click <a href="https://example.com">here</a>.'
        '</p>'
    )  # fmt: skip


def test_navigation() -> None:
    navigation = Navigation(
        NavItem("Home", to="/"),
        NavItem("About", to="/about"),
        id="nav",
    )
    assert navigation.to_html() == (
        '<nav id="nav">'
            "<ul>"
                '<li id="home"><a href="/">Home</a></li>'
                '<li id="about"><a href="/about">About</a></li>'
            "</ul>"
        "</nav>"
    )  # fmt: skip


def test_pairs() -> None:
    pairs = Pairs(
        Key("Name"),
        Value("John"),
        Key("Age"),
        Value(42),
    )
    assert pairs.to_html() == (
        '<dl class="stack stack-small">'
            '<dt>Name</dt>'
            '<dd>John</dd>'
            '<dt>Age</dt>'
            '<dd>42</dd>'
        "</dl>"
    )  # fmt: skip


def test_tables() -> None:
    table = Table(
        TableHead("Name", "Age"),
        TableRow("John", 42),
        TableRow("Jane", 43),
    )

    assert table.header == ("Name", "Age")
    assert table.getlist("Name") == ["John", "Jane"]
    assert table.getlist("Age") == [42, 43]
    assert table.getlist("NOT_FOUND") == []

    assert len(table.children) > 2
    assert table.children[2].get_value(123) is None

    assert table.to_html() == (
        '<table class="table">'
            "<thead>"
                '<tr><th>Name</th><th>Age</th></tr>'
            "</thead>"
            "<tbody>"
                '<tr><td>John</td><td>42</td></tr>'
                '<tr><td>Jane</td><td>43</td></tr>'
            "</tbody>"
        "</table>"
    )  # fmt: skip


def test_form_fields() -> None:
    form = Form(
        InputField(value="Name", name="name"),
        TextAreaField("Description", name="description"),
    )

    assert form.to_html() == (
        '<form class="form stack">'
            '<div class="form-field">'
                '<input value="Name" name="name" id="name" />'
            "</div>"
            '<div class="form-field">'
                '<textarea name="description" id="description">Description</textarea>'
            "</div>"
        "</form>"
    )  # fmt: skip

    form = Form(
        InputField(value="Name", name="name", label="Foo"),
        TextAreaField("Description", name="description", label="Bar"),
    )

    assert form.to_html() == (
        '<form class="form stack">'
            '<div class="form-field">'
                '<label for="name">Foo</label>'
                '<input value="Name" name="name" id="name" />'
            "</div>"
            '<div class="form-field">'
                '<label for="description">Bar</label>'
                '<textarea name="description" id="description">Description</textarea>'
            "</div>"
        "</form>"
    )  # fmt: skip
