from collections.abc import Mapping, Sequence
from typing import Any

class Element:
    html_header: str | None
    html_name: str | None
    void_element: bool

    children: Sequence[Any]
    attrs: Mapping[str, Any]
    context: Mapping[str, Any]

    def __str__(self) -> str: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    @property
    def text(self) -> str:
        """Get the text content of the element."""

    def is_simple(self) -> bool: ...
    def has_attributes(self) -> bool: ...
    def to_html(self) -> str: ...
