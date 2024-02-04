from typing import Literal, TypedDict

Styles = TypedDict(
    "Styles",
    {
        "color": str,
        "direction": Literal["row", "column"],
        "height": str,
        "justify-content": Literal["start", "end", "center", "equally-spaced"],
        "width": str,
    },
    total=False,
)
