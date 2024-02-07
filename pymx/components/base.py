from abc import ABCMeta, abstractmethod

from ..elements.base import AnyElement, Attributes, Element


class Component[*Te, Ta: Attributes](Element[*Te, Ta], metaclass=ABCMeta):
    """Base class for components.

    A component subclasses an :class:`Element` and represents any element
    that can be rendered in PyMX.

    Example usage:

        class PersonAttributes(Attributes):
            age: NotRequired[int]

        class Person(Component[PersonAttributes]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(self.attrs["name"]),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )

    Now the component can be used in any other component or element:

        >>> div(Person(name="John Doe", age=30), id="person-detail")

    You can also make the component take children:

        class PersonAttributes(Attributes):
            age: NotRequired[int]

        class Person(Component[str, str, PersonAttributes]):
            @override
            def render(self) -> dl:
                return dl(
                    dt("Name"),
                    dd(" ".join(self.children)),
                    dt("Age"),
                    dd(self.attrs.get("age", "N/A")),
                )

    Valid usage would now look like this:

        >>> div(Person("John", "Doe", age=30), id="person-detail")
    """

    @abstractmethod
    def render(self) -> AnyElement:
        """Render the component as an instance of :class:`Element`."""
