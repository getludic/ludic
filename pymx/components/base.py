from abc import abstractmethod

from ..elements import Element
from ..elements.base import TAttributes, TElement


class Component(Element[TElement, TAttributes]):
    @abstractmethod
    def render(self) -> Element:
        ...
