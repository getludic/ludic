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
from ludic.catalog.quotes import Quote
from ludic.catalog.tables import Table, TableHead, TableRow
from ludic.catalog.typography import Code, Link, Paragraph
from ludic.html import b
from ludic.styles import themes
from ludic.types import Safe


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

    assert TableRow(b("John"), 42).get_value(0) == "John"

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


def test_headers_with_t_strings() -> None:
    assert H1(t"The {Code('style')} Attribute").to_html() == (
        '<h1>The <code class="code">style</code> Attribute</h1>'
    )
    assert H4(t"{Code('ludic.types')}").to_html() == (
        '<h4><code class="code">ludic.types</code></h4>'
    )

    theme = themes.LightTheme(headers=themes.Headers(h3=themes.Header(anchor=True)))
    assert theme.use(H3(t"The {Code('style')} Attribute")).to_html() == (
        '<div class="with-anchor">'
            '<h3 id="the-style-attribute">'
                'The <code class="code">style</code> Attribute'
            '</h3>'
            '<a href="#the-style-attribute" class="anchor">#</a>'
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
    assert List(t"Test {b("yes")}", "D").to_html() == (
        "<ul>"
          "<li>Test <b>yes</b></li>"
          "<li>D</li>"
        "</ul>"
    )  # fmt: skip
    assert NumberedList(
        Item(t"Test {b("ol")}"),
        Item("E"),
    ).to_html() == (
        "<ol>"
          "<li>Test <b>ol</b></li>"
          "<li>E</li>"
        "</ol>"
    )  # fmt: skip


def test_quote_with_tstring() -> None:
    quote = Quote(
        t"One {Code('select')} depends on another.",
        source_url="https://htmx.org/examples/value-select/",
    )
    assert quote.to_html() == (
        '<div class="quote">'
          "<blockquote>"
            '<p>One <code class="code">select</code> depends on another.</p>'
          "</blockquote>"
          "<footer>"
            "Source: "
            '<a href="https://htmx.org/examples/value-select/">'
              "https://htmx.org/examples/value-select/"
            "</a>"
          "</footer>"
        "</div>"
    )  # fmt: skip


def test_quote_paragraphs() -> None:
    assert Quote("First.\n\nSecond.").to_html() == (
        '<div class="quote">'
          "<blockquote><p>First.</p><p>Second.</p></blockquote>"
        "</div>"
    )  # fmt: skip
    assert Quote(t"One {Code('a')}.\n\nTwo {Code('b')}.").to_html() == (
        '<div class="quote">'
          "<blockquote>"
            '<p>One <code class="code">a</code>.</p>'
            '<p>Two <code class="code">b</code>.</p>'
          "</blockquote>"
        "</div>"
    )  # fmt: skip
    assert Quote(t"{Code('a')}\n\n{Code('b')}").to_html() == (
        '<div class="quote">'
          "<blockquote>"
            '<p><code class="code">a</code></p>'
            '<p><code class="code">b</code></p>'
          "</blockquote>"
        "</div>"
    )  # fmt: skip
    assert Quote(Safe("<i>a</i>\n\n<i>b</i>")).to_html() == (
        '<div class="quote">'
          "<blockquote><p><i>a</i></p><p><i>b</i></p></blockquote>"
        "</div>"
    )  # fmt: skip


def test_head_with_dark_theme() -> None:
    from ludic.catalog.pages import DARK_STYLES_ID, Head

    head = Head(
        title="Dark",
        theme=themes.LightTheme(),
        dark_theme=themes.DarkTheme(),
    ).to_html()

    assert head.count("<style") == 2
    assert '<style type="text/css">' in head
    assert (
        f'<style media="(prefers-color-scheme: dark)" id="{DARK_STYLES_ID}" '
        'type="text/css">'
    ) in head
    assert "html { color-scheme: light; }" in head
    assert "html { color-scheme: dark; }" in head
    assert 'localStorage.getItem("ludic-color-scheme")' in head
    # The script restoring the scheme must run after the dark styles exist.
    assert head.index("localStorage") > head.index(DARK_STYLES_ID)


def test_head_without_dark_theme() -> None:
    from ludic.catalog.pages import Head

    head = Head(title="Light").to_html()
    assert head.count("<style") == 1
    assert "localStorage" not in head


def test_color_scheme_toggle() -> None:
    from ludic.catalog.pages import ColorSchemeToggle

    toggle = ColorSchemeToggle().to_html()
    assert toggle.startswith('<button type="button" onclick="')
    assert 'aria-label="Switch between light and dark theme"' in toggle
    assert 'class="color-scheme-toggle"' in toggle
    assert '<span class="when-light"><svg' in toggle
    assert '<span class="when-dark"><svg' in toggle
    assert "&quot;ludic-dark-styles&quot;" in toggle

    custom = ColorSchemeToggle("Theme", aria_label="Theme").to_html()
    assert ">Theme</button>" in custom


def test_tabs() -> None:
    from ludic.catalog.tabs import Tab, Tabs

    tabs = Tabs(
        Tab("pip install ludic", label="pip"),
        Tab(b("uv add ludic"), label="uv"),
        id="install",
    )
    assert tabs.to_html() == (
        '<div id="install" class="tabs">'
            '<input type="radio" name="install" id="install-0" checked="checked" '
                'class="tab-input">'
            '<label for="install-0" class="tab-label">pip</label>'
            '<div class="tab-panel">pip install ludic</div>'
            '<input type="radio" name="install" id="install-1" class="tab-input">'
            '<label for="install-1" class="tab-label">uv</label>'
            '<div class="tab-panel"><b>uv add ludic</b></div>'
        "</div>"
    )  # fmt: skip


def test_tabs_default_name_is_stable() -> None:
    from ludic.catalog.tabs import Tab, Tabs

    first = Tabs(Tab("a", label="A"), Tab("b", label="B")).to_html()
    second = Tabs(Tab("a", label="A"), Tab("b", label="B")).to_html()
    other = Tabs(Tab("a", label="A"), Tab("c", label="C")).to_html()
    assert first == second
    assert 'name="tabs-' in first
    assert first.split('name="')[1][:14] != other.split('name="')[1][:14]


def test_code_block_with_copy_button() -> None:
    from ludic.catalog.typography import CodeBlock

    plain = CodeBlock("print(1)").to_html()
    assert plain == '<pre class="code-block">print(1)</pre>'

    block = CodeBlock("print(1)", copy_button=True, id="example").to_html()
    assert block.startswith('<div id="example" class="code-block"><pre>print(1)</pre>')
    assert '<button type="button" class="copy-button" aria-label="Copy code"' in block
    assert "navigator.clipboard.writeText" in block
    assert block.endswith(">Copy</button></div>")


def test_code_block_line_numbers_are_marked() -> None:
    from ludic.catalog.typography import CodeBlock

    block = CodeBlock("a = 1\nb = 2", language="python", line_numbers=True).to_html()
    assert block.count('class="line-number"') == 2


def test_code_block_with_label() -> None:
    from ludic.catalog.typography import CodeBlock

    assert CodeBlock("print(1)", label="app.py").to_html() == (
        '<div class="code-block">'
        '<div class="code-block-label">app.py</div>'
        "<pre>print(1)</pre>"
        "</div>"
    )


def test_table_of_contents() -> None:
    from ludic.catalog.headers import H1, H2, H3
    from ludic.catalog.navigation import TableOfContents
    from ludic.html import h2

    content = [
        H1("Guide"),
        H2("Getting Started", anchor=True),
        Paragraph("Text"),
        H3("Install It", anchor=True),
        h2("Usage", id="how-to-use"),
        H2("Example", anchor=False),
        h2("Plain"),
    ]
    assert TableOfContents(*content, label="On this page").to_html() == (
        '<nav aria-label="On this page" class="table-of-contents">'
            '<p class="toc-title">On this page</p>'
            "<ul>"
                '<li class="level-2">'
                    '<a href="#getting-started">Getting Started</a>'
                "</li>"
                '<li class="level-2"><a href="#how-to-use">Usage</a></li>'
            "</ul>"
        "</nav>"
    )  # fmt: skip
    deeper = TableOfContents(*content, max_level=3).to_html()
    assert '<li class="level-3"><a href="#install-it">Install It</a></li>' in deeper
    assert 'aria-label="Table of contents"' in deeper


def test_table_of_contents_links_match_header_anchors() -> None:
    from ludic.catalog.headers import H2
    from ludic.catalog.navigation import TableOfContents

    header = H2("Error Handlers", anchor=True)
    toc = TableOfContents(header).to_html()
    assert 'id="error-handlers"' in header.to_html()
    assert 'href="#error-handlers"' in toc

    # The default theme renders H2 without an anchor, so it has no id to link to.
    assert "<li" not in TableOfContents(H2("Error Handlers")).to_html()


def test_navbar() -> None:
    from ludic.catalog.navigation import NavBar

    assert NavBar(Link("App", to="/"), Link("Docs", to="/docs")).to_html() == (
        '<header class="navbar">'
            '<div class="navbar-content">'
                '<a href="/">App</a><a href="/docs">Docs</a>'
            "</div>"
        "</header>"
    )  # fmt: skip


def test_card() -> None:
    from ludic.catalog.cards import Card
    from ludic.html import h3

    assert Card(h3("Typed"), Paragraph("Checked by mypy.")).to_html() == (
        '<div class="card"><h3>Typed</h3><p>Checked by mypy.</p></div>'
    )
    assert Card(h3("Docs"), to="/docs", id="docs").to_html() == (
        '<a href="/docs" id="docs" class="card"><h3>Docs</h3></a>'
    )


def test_code_block_wrapper_styles() -> None:
    from ludic.catalog.typography import CodeBlock
    from ludic.html import style

    css = style.from_components(CodeBlock, theme=themes.LightTheme()).to_html()
    assert "div.code-block > pre { padding-block:" in css
    assert "color: inherit;" in css
    assert "div.code-block:has(> .copy-button) > pre {" in css


def test_code_block_is_not_limited_by_the_measure() -> None:
    from ludic.catalog.typography import CodeBlock
    from ludic.html import style

    css = style.from_components(CodeBlock, theme=themes.LightTheme()).to_html()
    rules = {line.split(" {")[0]: line for line in css.splitlines() if " {" in line}
    assert "max-inline-size: none;" in rules[".code-block"]
    assert "max-inline-size: none;" in rules["div.code-block > pre"]
