from typing import Generic, Unpack, cast

from .attrs import NoAttrs
from .base import BaseElement
from .types import TAttrs, TChildren, TChildrenArgs


class Element(Generic[TChildren, TAttrs], BaseElement):
    """Base class for Ludic elements.

    Args:
        *children (TChild): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[TChildren, ...]
    attrs: TAttrs

    def __init__(
        self,
        *children: TChildren,
        # FIXME: https://github.com/python/typing/issues/1399
        **attributes: Unpack[TAttrs],  # type: ignore
    ) -> None:
        super().__init__()
        self.attrs = cast(TAttrs, attributes)
        self.children = tuple(self.formatter.extract(*children))


class ElementStrict(Generic[*TChildrenArgs, TAttrs], BaseElement):
    """Base class for strict elements (elements with concrete types of children).

    Args:
        *children (*TChildTuple): The children of the element.
        **attrs (Unpack[TAttrs]): The attributes of the element.
    """

    children: tuple[*TChildrenArgs]
    attrs: TAttrs

    def __init__(
        self,
        *children: *TChildrenArgs,
        # FIXME: https://github.com/python/typing/issues/1399
        **attrs: Unpack[TAttrs],  # type: ignore
    ) -> None:
        super().__init__()
        self.attrs = cast(TAttrs, attrs)
        self.children = tuple(self.formatter.extract(*children))


class Blank(Element[TChildren, NoAttrs]):
    """Element representing no element at all, just children.

    The purpose of this element is to be able to return only children
    when rendering a component.
    """

    def __init__(self, *children: TChildren) -> None:
        super().__init__(*self.formatter.extract(*children))

    def to_html(self) -> str:
        return "".join(map(str, self.children))
