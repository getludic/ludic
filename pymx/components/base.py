from abc import abstractmethod

from ..elements import Element
from ..elements.base import Attributes, TElements


class Component(Element[*TElements], Attributes):
    html_name = "div"

    @abstractmethod
    def render(self) -> Element:
        ...
