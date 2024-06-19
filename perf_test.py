from ludic.html import a, div

data = div(
    *(a("test", href="https://example.com") for _ in range(1000000)),
    style={"text-shadow": "2"},
)

# ludicrous.to_html(data)
