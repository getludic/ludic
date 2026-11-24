import hashlib
from typing import override

from ludic import html
from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import div, style
from ludic.types import AnyChildren


class TabAttrs(GlobalAttrs):
    label: str


class Tab(Component[AnyChildren, TabAttrs]):
    """One tab of :class:`Tabs`: a label and the content shown when it is selected.

    Example usage:

        Tab(CodeBlock("pip install ludic"), label="pip")
    """

    classes = ["tab-panel"]

    @override
    def render(self) -> div:
        return div(*self.children, **self.attrs_for(div))


class TabsAttrs(GlobalAttrs, total=False):
    name: str


class Tabs(Component[Tab, TabsAttrs]):
    """Tabs showing the content of one :class:`Tab` at a time.

    The tabs work without JavaScript. Each label belongs to a hidden radio
    button, so a click or the arrow keys select a tab, and CSS shows the
    content of the selected one. The first tab is selected.

    The radio buttons of one ``Tabs`` share a name, which is the ``name`` or
    the ``id`` attribute, or a name derived from the labels. Give two ``Tabs``
    with the same labels on one page different names.

    Example usage:

        Tabs(
            Tab(CodeBlock("pip install ludic"), label="pip"),
            Tab(CodeBlock("uv add ludic"), label="uv"),
        )
    """

    classes = ["tabs"]
    styles = style.use(
        lambda theme: {
            ".tabs": {
                "display": "flex",
                "flex-wrap": "wrap",
                "align-items": "flex-end",
                "column-gap": theme.sizes.xxs,
            },
            ".tabs > .tab-input": {
                "position": "absolute",
                "opacity": "0",
                "width": "1px",
                "height": "1px",
                "pointer-events": "none",
            },
            ".tabs > .tab-label": {
                "padding": f"{theme.sizes.xxxs} {theme.sizes.xs}",
                "border-block-end": f"{theme.borders.normal} solid transparent",
                "color": theme.colors.dark.lighten(1),
                "font-weight": "500",
                "cursor": "pointer",
                "user-select": "none",
            },
            ".tabs > .tab-label:hover": {
                "color": theme.colors.dark,
            },
            ".tabs > .tab-input:checked + .tab-label": {
                "color": theme.colors.dark,
                "border-block-end-color": theme.colors.primary,
            },
            ".tabs > .tab-input:focus-visible + .tab-label": {
                "outline": f"{theme.borders.normal} solid {theme.colors.primary}",
                "outline-offset": theme.borders.normal,
                "border-radius": theme.rounding.less,
            },
            ".tabs > .tab-panel": {
                "display": "none",
                "order": "1",
                "flex-basis": "100%",
                "min-inline-size": "0",
                "padding-block-start": theme.sizes.s,
                "border-block-start": (
                    f"{theme.borders.thin} solid {theme.colors.light.darken(1)}"
                ),
            },
            ".tabs > .tab-input:checked + .tab-label + .tab-panel": {
                "display": "block",
            },
        }
    )

    @override
    def render(self) -> div:
        name = self.attrs.get("name") or self.attrs.get("id") or self._default_name()
        parts: list[AnyChildren] = []
        for index, tab in enumerate(self.children):
            input_id = f"{name}-{index}"
            parts.append(
                html.input(
                    type="radio",
                    name=name,
                    id=input_id,
                    checked=index == 0,
                    classes=["tab-input"],
                )
            )
            parts.append(
                html.label(tab.attrs["label"], for_=input_id, classes=["tab-label"])
            )
            parts.append(tab)
        return div(*parts, **self.attrs_for(div))

    def _default_name(self) -> str:
        labels = "\x00".join(tab.attrs["label"] for tab in self.children)
        return f"tabs-{hashlib.sha256(labels.encode()).hexdigest()[:8]}"
