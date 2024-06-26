from typing import override

from ludic.attrs import Attrs
from ludic.components import Component
from ludic.html import div
from ludic.types import AnyChildren


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
