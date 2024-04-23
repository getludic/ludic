from typing import NotRequired, override

from ludic.attrs import GlobalAttrs, NoAttrs
from ludic.html import div, style
from ludic.types import AnyChildren, Component


class Loading(Component[AnyChildren, NoAttrs]):
    classes = ["loader"]
    styles = style.use(
        lambda theme: {
            ".loader": {
                "text-align": "center",
            },
            ".lds-ellipsis": {
                "display": "inline-block",
                "position": "relative",
                "width": "80px",
                "height": "80px",
            },
            ".lds-ellipsis div": {
                "position": "absolute",
                "top": "33px",
                "width": "13px",
                "height": "13px",
                "border-radius": "50%",
                "background": theme.colors.dark,
                "animation-timing-function": "cubic-bezier(0, 1, 1, 0)",
            },
            ".lds-ellipsis div:nth-child(1)": {
                "left": "8px",
                "animation": "lds-ellipsis1 0.6s infinite",
            },
            ".lds-ellipsis div:nth-child(2)": {
                "left": "8px",
                "animation": "lds-ellipsis2 0.6s infinite",
            },
            ".lds-ellipsis div:nth-child(3)": {
                "left": "32px",
                "animation": "lds-ellipsis2 0.6s infinite",
            },
            ".lds-ellipsis div:nth-child(4)": {
                "left": "56px",
                "animation": "lds-ellipsis3 0.6s infinite",
            },
            "@keyframes lds-ellipsis1": {
                "0%": {
                    "transform": "scale(0)",
                },
                "100%": {
                    "transform": "scale(1)",
                },
            },
            "@keyframes lds-ellipsis3": {
                "0%": {
                    "transform": "scale(1)",
                },
                "100%": {
                    "transform": "scale(0)",
                },
            },
            "@keyframes lds-ellipsis2": {
                "0%": {
                    "transform": "translate(0, 0)",
                },
                "100%": {
                    "transform": "translate(24px, 0)",
                },
            },
        }
    )

    @override
    def render(self) -> div:
        return div(
            div(div(""), div(""), div(""), div(""), classes=["lds-ellipsis"]),
        )


class LazyLoaderAttrs(GlobalAttrs):
    load_url: str
    placeholder: NotRequired[AnyChildren]


class LazyLoader(Component[AnyChildren, LazyLoaderAttrs]):
    """Lazy loader component using HTMX attributes.

    Usage:

        LazyLoader(
            load_url="https://example.com/svg-file"
        )
    """

    @override
    def render(self) -> div:
        self.attrs.setdefault("hx_trigger", "load")
        self.attrs.setdefault("hx_get", self.attrs["load_url"])
        self.attrs.setdefault("hx_swap", "outerHTML")
        return div(self.attrs.get("placeholder", Loading()), **self.attrs_for(div))
