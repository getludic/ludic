from abc import ABCMeta, abstractmethod

from ..elements import Element
from ..elements.base import AnyElement, TAttributes, TElements


class Component(Element[*TElements, TAttributes], metaclass=ABCMeta):
    """Base class for components."""

    @abstractmethod
    def render(self) -> AnyElement:
        """Render the component as an instance of :class:`Element`."""
