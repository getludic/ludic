from datetime import datetime

from ludic import html
from ludicrous import div, span

now = datetime.now()
data = html.div(
    *(html.span("test", id="https://example.com") for _ in range(1000000)),
    style={"text-shadow": "2"},
)
print("ludic", datetime.now() - now)

now = datetime.now()
data2 = div(
    *(span("test", id="https://example.com") for _ in range(1000000)),
    style={"text-shadow": "2"},
)
print("ludicrous", datetime.now() - now)

now = datetime.now()
val1 = data.to_html()
print("ludic to_html", datetime.now() - now)

now = datetime.now()
val2 = data2.to_html()
print("ludicrous to_html", datetime.now() - now)

print(val1 == val2)
