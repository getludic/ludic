from ludic import html
from ludic.styles import CSSProperties


def test_str_and_bytes() -> None:
    assert str(html.a("str")) == "<a>str</a>"
    assert bytes(html.p("str")) == b"<p>str</p>"


def test_empty_element() -> None:
    dom = html.div()
    assert dom.to_html() == "<div></div>"
    assert dom.to_string() == "<div />"

    dom2 = html.p()
    assert dom2.to_html() == "<p></p>"
    assert dom2.to_string() == "<p />"

    dom3 = html.script()
    assert dom3.to_html() == "<script></script>"
    assert dom3.to_string() == "<script />"

    dom4 = html.input()
    assert dom4.to_html() == "<input>"
    assert dom4.to_string() == "<input />"


def test_html_paragraph() -> None:
    paragraph = html.p(
        f"Hello, World! {html.b("Something bold")} and {html.i("Something italic")}"
    )
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
    link = html.a("A link!", href="https://example.com")
    assert link.to_html() == '<a href="https://example.com">A link!</a>'
    assert link.to_string() == (
        '<a href="https://example.com">\n'
        "  A link!\n"
        "</a>"
    )  # fmt: skip


def test_html_table() -> None:
    dom = html.table(
        html.thead(
            html.tr(
                html.th("Header 1"),
                html.th("Header 2"),
                html.th("Header 3"),
            )
        ),
        html.tbody(
            html.tr(
                html.td("Cell 1", style=CSSProperties(color="red", height="100px")),
                html.td("Cell 2"),
                html.td("Cell 3"),
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
    dom = html.div(
        html.div(html.label("First Name"), ": Joe"),
        html.div(html.label("Last Name"), ": Blow"),
        html.div(html.label("Email"), ": joe@blow.com"),
        html.button(
            "Click To Edit",
            classes=["btn", "btn-primary"],
            hx_get="/contact/1/edit",
        ),
        hx_target="this",
        hx_swap="outerHTML",
    )

    assert isinstance(dom.children[3], html.button)
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
    div_dom = html.div(html.p(1), html.p(2), html.p(3))
    span_dom = html.span(*div_dom)

    assert div_dom.text == span_dom.text == "123"
    assert span_dom.to_html() == "<span><p>1</p><p>2</p><p>3</p></span>"


def test_repr_and_str_and_to_string() -> None:
    dom = html.div(html.p(1), html.p(2), html.p(3), id="test")
    assert repr(dom) == str(dom) == '<div id="test"><p>1</p><p>2</p><p>3</p></div>'
    assert dom.to_string() == (
        '<div id="test">\n'
        "  <p>1</p>\n"
        "  <p>2</p>\n"
        "  <p>3</p>\n"
        "</div>"
    )  # fmt: skip


def test_data_attributes() -> None:
    dom = html.div("content", data_foo="1", data_bar="test")  # type: ignore[call-arg]

    assert dom.attrs == {"data_foo": "1", "data_bar": "test"}
    assert dom.to_html() == '<div data-foo="1" data-bar="test">content</div>'


def test_htmx_attributes() -> None:
    assert html.button(
        "Get Info!",
        hx_get="/info", hx_on__before_request="alert('Making a request!')",
    ).to_html() == (  # type: ignore[call-arg]
        '<button hx-get="/info" hx-on--before-request="alert(\'Making a request!\')">'
            "Get Info!"
        "</button>"
    )  # fmt: skip


def test_all_elements() -> None:
    assert html.div("test", id="div").to_html() == '<div id="div">test</div>'
    assert html.span("test", id="span").to_html() == '<span id="span">test</span>'
    assert html.main("test", id="main").to_html() == '<main id="main">test</main>'
    assert html.p("test", id="p").to_html() == '<p id="p">test</p>'
    assert html.a("test", id="a").to_html() == '<a id="a">test</a>'
    assert html.br().to_html() == "<br>"
    assert (
        html.button("test", id="button").to_html()
        == '<button id="button">test</button>'
    )
    assert html.label("test", id="label").to_html() == '<label id="label">test</label>'
    assert html.td("test", id="td").to_html() == '<td id="td">test</td>'
    assert html.th("test", id="th").to_html() == '<th id="th">test</th>'
    assert html.tr(id="tr").to_html() == '<tr id="tr"></tr>'
    assert html.thead(id="thead").to_html() == '<thead id="thead"></thead>'
    assert html.tbody(id="tbody").to_html() == '<tbody id="tbody"></tbody>'
    assert html.tfoot(id="tfoot").to_html() == '<tfoot id="tfoot"></tfoot>'
    assert html.table(id="table").to_html() == '<table id="table"></table>'
    assert html.li("test", id="li").to_html() == '<li id="li">test</li>'
    assert html.ul(id="ul").to_html() == '<ul id="ul"></ul>'
    assert html.ol(id="ol").to_html() == '<ol id="ol"></ol>'
    assert html.dt("test", id="dt").to_html() == '<dt id="dt">test</dt>'
    assert html.dd("test", id="dd").to_html() == '<dd id="dd">test</dd>'
    assert html.dl(id="dl").to_html() == '<dl id="dl"></dl>'
    assert (
        html.section("test", id="section").to_html()
        == '<section id="section">test</section>'
    )
    assert html.input(id="input").to_html() == '<input id="input">'
    assert html.output(id="output").to_html() == '<output id="output"></output>'
    assert (
        html.legend("test", id="legend").to_html()
        == '<legend id="legend">test</legend>'
    )
    assert (
        html.option("test", id="option").to_html()
        == '<option id="option">test</option>'
    )
    assert (
        html.optgroup("test", id="optgroup").to_html()
        == '<optgroup id="optgroup">test</optgroup>'
    )
    assert (
        html.select(html.option(), id="select").to_html()
        == '<select id="select"><option></option></select>'
    )
    assert (
        html.textarea("test", id="textarea").to_html()
        == '<textarea id="textarea">test</textarea>'
    )
    assert (
        html.fieldset("test", id="fieldset").to_html()
        == '<fieldset id="fieldset">test</fieldset>'
    )
    assert html.form("test", id="form").to_html() == '<form id="form">test</form>'
    assert html.img(id="img").to_html() == '<img id="img">'
    assert html.svg("test", id="svg").to_html() == '<svg id="svg">test</svg>'
    assert (
        html.circle("test", id="circle").to_html()
        == '<circle id="circle">test</circle>'
    )
    assert html.line("test", id="line").to_html() == '<line id="line">test</line>'
    assert html.path("test", id="path").to_html() == '<path id="path">test</path>'
    assert (
        html.polyline("test", id="polyline").to_html()
        == '<polyline id="polyline">test</polyline>'
    )
    assert html.b("test", id="b").to_html() == '<b id="b">test</b>'
    assert html.i("test", id="i").to_html() == '<i id="i">test</i>'
    assert html.s("test", id="s").to_html() == '<s id="s">test</s>'
    assert html.u("test", id="u").to_html() == '<u id="u">test</u>'
    assert (
        html.strong("test", id="strong").to_html()
        == '<strong id="strong">test</strong>'
    )
    assert html.em("test", id="em").to_html() == '<em id="em">test</em>'
    assert html.mark("test", id="mark").to_html() == '<mark id="mark">test</mark>'
    assert html.del_("test", id="del_").to_html() == '<del id="del_">test</del>'
    assert html.ins("test", id="ins").to_html() == '<ins id="ins">test</ins>'
    assert (
        html.header("test", id="header").to_html()
        == '<header id="header">test</header>'
    )
    assert html.big("test", id="big").to_html() == '<big id="big">test</big>'
    assert html.small("test", id="small").to_html() == '<small id="small">test</small>'
    assert html.code("test", id="code").to_html() == '<code id="code">test</code>'
    assert html.pre("test", id="pre").to_html() == '<pre id="pre">test</pre>'
    assert html.cite("test", id="cite").to_html() == '<cite id="cite">test</cite>'
    assert (
        html.blockquote("test", id="blockquote").to_html()
        == '<blockquote id="blockquote">test</blockquote>'
    )
    assert html.abbr("test", id="abbr").to_html() == '<abbr id="abbr">test</abbr>'
    assert html.h1("test", id="h1").to_html() == '<h1 id="h1">test</h1>'
    assert html.h2("test", id="h2").to_html() == '<h2 id="h2">test</h2>'
    assert html.h3("test", id="h3").to_html() == '<h3 id="h3">test</h3>'
    assert html.h4("test", id="h4").to_html() == '<h4 id="h4">test</h4>'
    assert html.h5("test", id="h5").to_html() == '<h5 id="h5">test</h5>'
    assert html.h6("test", id="h6").to_html() == '<h6 id="h6">test</h6>'
    assert html.title("test").to_html() == "<title>test</title>"
    assert html.link(type="link").to_html() == '<link type="link">'
    assert (
        html.script("test", id="script").to_html()
        == '<script id="script">test</script>'
    )
    assert (
        html.noscript("test", id="noscript").to_html()
        == '<noscript id="noscript">test</noscript>'
    )
    assert html.meta(id="meta").to_html() == '<meta id="meta">'
    assert html.head(html.meta()).to_html() == "<head><meta></head>"
    assert html.body("test", id="body").to_html() == '<body id="body">test</body>'
    assert (
        html.footer("test", id="footer").to_html()
        == '<footer id="footer">test</footer>'
    )
    assert (
        html.html(html.head(), html.body()).to_html()
        == "<!doctype html>\n<html><head></head><body></body></html>"
    )
    assert html.iframe(id="iframe").to_html() == '<iframe id="iframe"></iframe>'
    assert (
        html.article("test", id="article").to_html()
        == '<article id="article">test</article>'
    )
    assert (
        html.address("test", id="address").to_html()
        == '<address id="address">test</address>'
    )
    assert (
        html.caption("test", id="caption").to_html()
        == '<caption id="caption">test</caption>'
    )
    assert html.col(id="col").to_html() == '<col id="col">'
    assert (
        html.colgroup("test", id="colgroup").to_html()
        == '<colgroup id="colgroup">test</colgroup>'
    )
    assert html.area(id="area").to_html() == '<area id="area">'
    assert html.aside("test", id="aside").to_html() == '<aside id="aside">test</aside>'
    assert html.source(id="source").to_html() == '<source id="source">'
    assert html.audio("test", id="audio").to_html() == '<audio id="audio">test</audio>'
    assert html.base(id="base").to_html() == '<base id="base">'
    assert html.bdi("test", id="bdi").to_html() == '<bdi id="bdi">test</bdi>'
    assert html.bdo("test", id="bdo").to_html() == '<bdo id="bdo">test</bdo>'
    assert (
        html.canvas("test", id="canvas").to_html()
        == '<canvas id="canvas">test</canvas>'
    )
    assert html.data("test", id="data").to_html() == '<data id="data">test</data>'
    assert (
        html.datalist("test", id="datalist").to_html()
        == '<datalist id="datalist">test</datalist>'
    )
    assert (
        html.details("test", id="details").to_html()
        == '<details id="details">test</details>'
    )
    assert html.dfn("test", id="dfn").to_html() == '<dfn id="dfn">test</dfn>'
    assert (
        html.dialog("test", id="dialog").to_html()
        == '<dialog id="dialog">test</dialog>'
    )
    assert html.embed(id="embed").to_html() == '<embed id="embed">'
    assert (
        html.figcaption("test", id="figcaption").to_html()
        == '<figcaption id="figcaption">test</figcaption>'
    )
    assert (
        html.figure("test", id="figure").to_html()
        == '<figure id="figure">test</figure>'
    )
    assert (
        html.hrgroup("test", id="hrgroup").to_html()
        == '<hrgroup id="hrgroup">test</hrgroup>'
    )
    assert html.hr(id="hr").to_html() == '<hr id="hr">'
    assert html.kbd("test", id="kbd").to_html() == '<kbd id="kbd">test</kbd>'
    assert html.map("test", id="map").to_html() == '<map id="map">test</map>'
    assert html.menu("test", id="menu").to_html() == '<menu id="menu">test</menu>'
    assert html.meter("test", id="meter").to_html() == '<meter id="meter">test</meter>'
    assert html.nav("test", id="nav").to_html() == '<nav id="nav">test</nav>'
    assert (
        html.object("test", id="object").to_html()
        == '<object id="object">test</object>'
    )
    assert html.param(id="param").to_html() == '<param id="param">'
    assert (
        html.picture("test", id="picture").to_html()
        == '<picture id="picture">test</picture>'
    )
    assert (
        html.progress("test", id="progress").to_html()
        == '<progress id="progress">test</progress>'
    )
    assert html.q("test", id="q").to_html() == '<q id="q">test</q>'
    assert html.rp("test", id="rp").to_html() == '<rp id="rp">test</rp>'
    assert html.rt("test", id="rt").to_html() == '<rt id="rt">test</rt>'
    assert html.ruby("test", id="ruby").to_html() == '<ruby id="ruby">test</ruby>'
    assert html.samp("test", id="samp").to_html() == '<samp id="samp">test</samp>'
    assert (
        html.search("test", id="search").to_html()
        == '<search id="search">test</search>'
    )
    assert html.sub("test", id="sub").to_html() == '<sub id="sub">test</sub>'
    assert (
        html.summary("test", id="summary").to_html()
        == '<summary id="summary">test</summary>'
    )
    assert html.sup("test", id="sup").to_html() == '<sup id="sup">test</sup>'
    assert (
        html.template("test", id="template").to_html()
        == '<template id="template">test</template>'
    )
    assert html.time("test", id="time").to_html() == '<time id="time">test</time>'
    assert html.track(id="track").to_html() == '<track id="track">'
    assert html.var("test", id="var").to_html() == '<var id="var">test</var>'
    assert html.video("test", id="video").to_html() == '<video id="video">test</video>'
    assert html.wbr(id="wbr").to_html() == '<wbr id="wbr">'
