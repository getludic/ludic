from abc import ABCMeta
from collections.abc import Iterator, Mapping, Sequence
from typing import Any, ClassVar

from .format import FormatContext, format_attrs, format_element


class BaseElement(metaclass=ABCMeta):
    html_header: ClassVar[str | None] = None
    html_name: ClassVar[str | None] = None
    void_element: ClassVar[bool] = False

    formatter: ClassVar[FormatContext] = FormatContext("element_formatter")
    formatter_fstring_wrap_in: ClassVar[type["BaseElement"] | None] = None

    children: Sequence[Any]
    attrs: Mapping[str, Any]
    context: dict[str, Any]

    def __init__(self, *children: Any, **attrs: Any) -> None:
        self.context = {}
        self.children = self.formatter.extract(
            *children, WrapIn=self.formatter_fstring_wrap_in
        )
        self.attrs = attrs

    def __str__(self) -> str:
        return self.to_html()

    def __bytes__(self) -> bytes:
        return self.to_html().encode("utf-8")

    def __format__(self, _: str) -> str:
        return self.formatter.append(self)

    def __len__(self) -> int:
        return len(self.children)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.children)

    def __repr__(self) -> str:
        return self.to_string(pretty=False)

    def __eq__(self, other: Any) -> bool:
        return (
            type(self) is type(other)
            and self.children == other.children
            and self.attrs == other.attrs
        )

    def _format_attributes(self, is_html: bool = False) -> str:
        attrs: dict[str, Any] = format_attrs(self.attrs, is_html=is_html)
        return " ".join(
            f'{key}="{value}"' if '"' not in value else f"{key}='{value}'"
            for key, value in attrs.items()
        )

    def _format_children(self) -> str:
        formatted = ""
        for child in self.children:
            if self.context and isinstance(child, BaseElement):
                child.context.update(self.context)
            formatted += format_element(child)
        return formatted

    @property
    def aliased_attrs(self) -> dict[str, Any]:
        """Attributes as a dict with keys renamed to their aliases."""
        return format_attrs(self.attrs)

    @property
    def text(self) -> str:
        """Get the text content of the element."""
        return "".join(
            child.text if isinstance(child, BaseElement) else str(child)
            for child in self.children
        )

    def is_simple(self) -> bool:
        """Check if the element is simple (i.e. contains only one primitive type)."""
        return len(self) == 1 and isinstance(self.children[0], str | int | float | bool)

    def has_attributes(self) -> bool:
        """Check if the element has any attributes."""
        return bool(self.attrs)

    def to_string(self, pretty: bool = True, _level: int = 0) -> str:
        """Convert the element tree to a string representation.

        Args:
            pretty (bool, optional): Whether to indent the string. Defaults to True.

        Returns:
            str: The string representation of the element tree.
        """
        indent = "  " * _level if pretty else ""
        name = self.__class__.__name__
        element = f"<{name}"

        if self.has_attributes():
            element += f" {self._format_attributes()}"

        if self.children:
            prefix, sep, suffix = "", "", ""
            if pretty and (not self.is_simple() or self.has_attributes()):
                prefix, sep, suffix = f"\n{indent}  ", f"\n{indent}  ", f"\n{indent}"

            children_str = sep.join(
                child.to_string(pretty=pretty, _level=_level + 1)
                if isinstance(child, BaseElement)
                else str(child)
                for child in self.children
            )

            element += f">{prefix}{children_str}{suffix}</{name}>"
        else:
            element += " />"

        return element

    def to_html(self) -> str:
        """Convert an element tree to an HTML string."""
        element_tag = f"{self.html_header}\n" if self.html_header else ""
        children_str = self._format_children() if self.children else ""

        element_tag += f"<{self.html_name}"
        if self.has_attributes():
            attributes_str = self._format_attributes(is_html=True)
            element_tag += f" {attributes_str}"

        if not self.void_element:
            element_tag += f">{children_str}</{self.html_name}>"
        else:
            element_tag += ">"

        return element_tag
