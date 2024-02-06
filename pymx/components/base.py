from abc import ABCMeta, abstractmethod

from ..elements.base import AnyElement, Attributes, Element


class Component[*Te, Ta: Attributes](Element[*Te, Ta], metaclass=ABCMeta):
    """Base class for components."""

    @abstractmethod
    def render(self) -> AnyElement:
        """Render the component as an instance of :class:`Element`."""
