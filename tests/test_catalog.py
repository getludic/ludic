from ludic.catalog.forms import ChoiceField, Form, InputField, TextAreaField
from ludic.catalog.headers import H1, H2, H3, H4, Anchor
from ludic.catalog.items import Key, Pairs, Value
from ludic.catalog.lists import Item, List, NumberedList
from ludic.catalog.messages import (
    Message,
    MessageDanger,
    MessageInfo,
    MessageSuccess,
    MessageWarning,
    Title,
)
from ludic.catalog.navigation import Navigation, NavItem
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.catalog.typography import Link, Paragraph
from ludic.html import b
from ludic.styles import themes


def test_link() -> None:
    link = Link("A link!", to="https://example.com")
    assert link.to_html() == '<a href="https://example.com" target="_blank">A link!</a>'
    link = Link("A link!", to="/home")
    assert link.to_html() == '<a href="/home">A link!</a>'


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
            'Click <a href="https://example.com" target="_blank">here</a>.'
        '</p>'
    )  # fmt: skip


def test_navigation() -> None:
    navigation = Navigation(
        NavItem("Home", to="/"),
        NavItem("About", to="/about"),
        id="nav",
    )
    assert navigation.to_html() == (
        '<nav id="nav" class="navigation">'
            '<ul class="stack small">'
                '<li class="nav-item"><a href="/" class="btn">Home</a></li>'
                '<li class="nav-item">'
                    '<a href="/about" class="btn">About</a>'
                '</li>'
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
        '<dl>'
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
        '<div class="table">'
            "<table>"
                "<thead>"
                    '<tr><th>Name</th><th>Age</th></tr>'
                "</thead>"
                "<tbody>"
                    '<tr><td>John</td><td>42</td></tr>'
                    '<tr><td>Jane</td><td>43</td></tr>'
                "</tbody>"
            "</table>"
        "</div>"
    )  # fmt: skip


def test_form_fields() -> None:
    form = Form(
        InputField(value="Name", name="name"),
        TextAreaField("Description", name="description"),
    )

    assert form.to_html() == (
        '<form class="form stack">'
            '<div class="form-field">'
                '<input value="Name" name="name" id="name">'
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
                '<input value="Name" name="name" id="name">'
            "</div>"
            '<div class="form-field">'
                '<label for="description">Bar</label>'
                '<textarea name="description" id="description">Description</textarea>'
            "</div>"
        "</form>"
    )  # fmt: skip


def test_header_anchor() -> None:
    assert Anchor(target="test").to_html() == '<a href="#test" class="anchor">#</a>'
    assert (
        Anchor("url", target="test").to_html()
        == '<a href="#test" class="anchor">url</a>'
    )


def test_headers() -> None:
    assert H1("Header 1").to_html() == "<h1>Header 1</h1>"
    assert H2("Header 2").to_html() == "<h2>Header 2</h2>"
    assert H3("Header 3").to_html() == "<h3>Header 3</h3>"
    assert H4("Header 4").to_html() == "<h4>Header 4</h4>"

    theme = themes.LightTheme(
        headers=themes.Headers(
            h1=themes.Header(anchor=True),
            h2=themes.Header(anchor=True),
            h3=themes.Header(anchor=True),
            h4=themes.Header(anchor=True),
        )
    )
    assert theme.use(H1("Header 1")).to_html() == (
        '<div class="with-anchor">'
            '<h1 id="header-1">Header 1</h1>'
            '<a href="#header-1" class="anchor">#</a>'
        '</div>'
    )  # fmt: skip
    assert theme.use(H2("Header 2")).to_html() == (
        '<div class="with-anchor">'
            '<h2 id="header-2">Header 2</h2>'
            '<a href="#header-2" class="anchor">#</a>'
        '</div>'
    )  # fmt: skip
    assert theme.use(H3("Header 3")).to_html() == (
        '<div class="with-anchor">'
            '<h3 id="header-3">Header 3</h3>'
            '<a href="#header-3" class="anchor">#</a>'
        '</div>'
    )  # fmt: skip
    assert theme.use(H4("Header 4")).to_html() == (
        '<div class="with-anchor">'
            '<h4 id="header-4">Header 4</h4>'
            '<a href="#header-4" class="anchor">#</a>'
        '</div>'
    )  # fmt: skip


def test_messages() -> None:
    assert Message("test").to_html() == (
        '<div class="message"><div class="content">test</div></div>'
    )
    assert Message(Title("Title"), "Content message").to_html() == (
        '<div class="message">'
        '<div class="title">Title</div>'
        '<div class="content">Content message</div>'
        "</div>"
    )
    assert MessageSuccess("test").to_html() == (
        '<div class="message success"><div class="content">test</div></div>'
    )
    assert MessageInfo("test").to_html() == (
        '<div class="message info"><div class="content">test</div></div>'
    )
    assert MessageWarning("test").to_html() == (
        '<div class="message warning"><div class="content">test</div></div>'
    )
    assert MessageDanger("test").to_html() == (
        '<div class="message danger"><div class="content">test</div></div>'
    )


def test_choice_field() -> None:
    assert ChoiceField(
        choices=[("yes", "Yes"), ("no", "No")],
        selected="yes",
        name="yes_no",
        label="Test",
    ).to_html() == (
        '<div class="form-field">'
            '<p class="form-label">Test</p>'
            '<div class="choice-field">'
                '<input '
                    'id="yes" value="yes" checked="checked" name="yes_no" type="radio"'
                '>'
                '<label for="yes">Yes</label>'
            '</div>'
            '<div class="choice-field">'
                '<input id="no" value="no" name="yes_no" type="radio">'
                '<label for="no">No</label>'
            '</div>'
        '</div>'
    )  # fmt: skip


def test_items() -> None:
    assert List("A", "B", "C").to_html() == "<ul><li>A</li><li>B</li><li>C</li></ul>"
    assert List(f"Test {b("yes")}", "D").to_html() == (
        "<ul>"
          "<li>Test <b>yes</b></li>"
          "<li>D</li>"
        "</ul>"
    )  # fmt: skip
    assert NumberedList(
        Item(f"Test {b("ol")}"),
        Item("E"),
    ).to_html() == (
        "<ol>"
          "<li>Test <b>ol</b></li>"
          "<li>E</li>"
        "</ol>"
    )  # fmt: skip
