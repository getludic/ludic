from typing import NotRequired, override

from ludic.attrs import GlobalAttrs
from ludic.html import div
from ludic.types import AnyChildren, Component


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
        return div(
            self.attrs.get("placeholder", "Loading ..."),
            hx_get=self.attrs["load_url"],
            hx_trigger="load",
        )
