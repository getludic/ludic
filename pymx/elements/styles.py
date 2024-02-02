from typing import Literal, NotRequired, TypedDict

Styles = TypedDict(
    "Styles",
    {
        "color": NotRequired[str],
        "direction": NotRequired[Literal["row", "column"]],
        "height": NotRequired[str],
        "justify-content": NotRequired[
            Literal["start", "end", "center", "equally-spaced"]
        ],
        "width": NotRequired[str],
    },
)
