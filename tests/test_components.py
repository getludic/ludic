from typing import Any, override

import pytest

from ludic.attrs import Attrs, NoAttrs
from ludic.components import Component
from ludic.html import div, span
from ludic.types import AnyChildren, NoChildren


class ClassesComponentAttrs(Attrs):
    class_: str


class ClassesComponent(Component[AnyChildren, ClassesComponentAttrs]):
    classes = ["class-a"]

    @override
    def render(self) -> div:
        return div(*self.children, classes=["class-b"], **self.attrs)


def test_component_classes() -> None:
    assert ClassesComponent(
        div("content", class_="class-f"), class_="class-c class-d"
    ).to_html() == (
        '<div class="class-b class-a class-c class-d">'
            '<div class="class-f">content</div>'
        '</div>'
    )  # fmt: skip


class Broken(Component[NoChildren, NoAttrs]):
    @override
    def render(self) -> div:
        raise ValueError("broken component")


class BrokenWithNote(Component[NoChildren, NoAttrs]):
    @override
    def render(self) -> div:
        error = ValueError("broken component")
        error.add_note("a note from the application")
        raise error


class Wrapper(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> div:
        return div(*self.children)


class Layout(Component[AnyChildren, NoAttrs]):
    @override
    def render(self) -> Wrapper:
        return Wrapper(span(*self.children))


def test_render_error_notes_component_path() -> None:
    with pytest.raises(ValueError, match="broken component") as exc_info:
        Layout(Broken()).to_html()

    assert exc_info.value.__notes__ == ["While rendering: Layout > Wrapper > Broken"]


def test_render_error_keeps_other_notes() -> None:
    with pytest.raises(ValueError) as exc_info:
        Wrapper(BrokenWithNote()).to_html()

    assert exc_info.value.__notes__ == [
        "a note from the application",
        "While rendering: Wrapper > BrokenWithNote",
    ]


def test_render_error_in_element_notes_component_path() -> None:
    invalid: Any = {"on click": "x"}

    with pytest.raises(ValueError, match="attribute name") as exc_info:
        Wrapper(div("content", attrs=invalid)).to_html()

    assert exc_info.value.__notes__ == ["While rendering: Wrapper"]


def test_render_without_error_adds_no_note() -> None:
    assert Layout("content").to_html() == "<div><span>content</span></div>"
