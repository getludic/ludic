"""A collection of PyMX components.

This module is meant as a collection of components that could be useful
for building PyMX applications. Any contributor is welcome to add new ones.

It also serves as showcase of possible implementations.
"""

from .navigation import Navigation, NavItem
from .typography import Link, Paragraph

__all__ = (
    "Navigation",
    "NavItem",
    "Link",
    "Paragraph",
)
