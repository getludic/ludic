from pymx.elements import (
    Link,
    Paragraph,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeadCell,
    TableRow,
)


def test_paragraph():
    paragraph = Paragraph("Hello, World!")
    assert paragraph.as_html() == "<p>Hello, World!</p>"


def test_link():
    link = Link(href="https://example.com")("A link!")
    assert link.as_html() == '<a href="https://example.com">A link!</a>'


def test_table():
    table = Table(
        TableHead(
            TableRow(
                TableHeadCell("Header 1"),
                TableHeadCell("Header 2"),
                TableHeadCell("Header 3"),
            )
        ),
        TableBody(
            TableRow(
                TableCell(style={"color": "red", "height": "100px"})("Cell 1"),
                TableCell("Cell 2"),
                TableCell("Cell 3"),
            ),
        ),
    )

    assert table.as_html() == (
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
