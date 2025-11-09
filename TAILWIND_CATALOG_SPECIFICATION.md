# Ludic TailwindCSS Catalog Specification

## Overview

This specification defines the `ludic.contrib.tailwind` module, which provides a complete alternative component catalog built with TailwindCSS utilities. The module includes a theme system, component catalog, and integration utilities to enable developers to use TailwindCSS with Ludic's type-safe component architecture.

## Design Principles

1. **No "Tailwind" in Component Names**: Components are named naturally (e.g., `Button`, not `TailwindButton`)
2. **Import Path Clarity**: The module path `ludic.contrib.tailwind.catalog` makes it clear these are Tailwind-based components
3. **API Compatibility**: Where possible, match the native catalog's API for easy switching
4. **Utility-First**: Leverage Tailwind's utility classes rather than custom CSS
5. **Theme Integration**: Provide a TailwindTheme that syncs with Tailwind's configuration
6. **Production-Ready**: Include build tools and optimized CSS generation

## Module Structure

```
ludic/
└── contrib/
    └── tailwind/
        ├── __init__.py
        ├── theme.py              # TailwindTheme and configuration utilities
        ├── pages.py              # Base page components with Tailwind setup
        ├── build.py              # Build utilities for CSS generation
        └── catalog/
            ├── __init__.py
            ├── buttons.py        # Button components
            ├── layouts.py        # Layout components (Stack, Grid, etc.)
            ├── forms.py          # Form components
            ├── cards.py          # Card components
            ├── alerts.py         # Alert/Message components
            ├── badges.py         # Badge components
            ├── navigation.py     # Navigation components
            ├── tables.py         # Table components
            ├── typography.py     # Typography components
            ├── modals.py         # Modal/Dialog components
            ├── dropdowns.py      # Dropdown components
            └── tooltips.py       # Tooltip components
```

## 1. Theme System (`ludic.contrib.tailwind.theme`)

### 1.1 TailwindTheme Class

The `TailwindTheme` class extends Ludic's base `Theme` and provides synchronization with TailwindCSS configuration.

```python
from dataclasses import dataclass
from ludic.styles import Theme
from ludic.styles.themes import LightTheme

@dataclass
class TailwindTheme(Theme):
    """Theme configured for TailwindCSS integration.

    This theme extends Ludic's Theme and provides utilities to:
    - Generate tailwind.config.js from theme values
    - Sync design tokens between Ludic and Tailwind
    - Provide Tailwind-friendly color names and values
    """

    # CSS file path for generated Tailwind styles
    css_path: str = "/static/tailwind.css"

    # Whether to use CDN fallback in development
    use_cdn_fallback: bool = False

    # Tailwind config options
    prefix: str = ""  # Optional prefix for all Tailwind classes
    important: bool = False  # Whether to mark utilities as !important

    def to_tailwind_config(self) -> dict:
        """Convert theme to Tailwind configuration object."""

    def generate_config_file(self, output_path: str = "tailwind.config.js") -> None:
        """Generate tailwind.config.js file from this theme."""

    def get_content_paths(self) -> list[str]:
        """Get content paths for Tailwind to scan for class names."""


# Pre-configured themes
class LightTailwindTheme(TailwindTheme, LightTheme):
    """Light theme configured for TailwindCSS."""
    pass


class DarkTailwindTheme(TailwindTheme):
    """Dark theme configured for TailwindCSS."""
    # Override color values for dark mode
    pass
```

### 1.2 Theme Synchronization

Utilities to keep Ludic theme and Tailwind config in sync:

```python
def theme_to_tailwind_config(theme: TailwindTheme) -> dict:
    """Convert Ludic theme to Tailwind configuration.

    Returns a dictionary that can be serialized to tailwind.config.js.
    Maps:
    - theme.colors -> tailwind.theme.extend.colors
    - theme.fonts -> tailwind.theme.extend.fontFamily
    - theme.sizes -> tailwind.theme.extend.spacing
    - theme.borders -> tailwind.theme.extend.borderWidth
    - theme.rounding -> tailwind.theme.extend.borderRadius
    """

def generate_tailwind_config(
    theme: TailwindTheme,
    output_path: str = "tailwind.config.js",
    include_plugins: list[str] | None = None
) -> None:
    """Generate a complete tailwind.config.js file.

    Args:
        theme: The Ludic TailwindTheme to convert
        output_path: Path to write the config file
        include_plugins: List of Tailwind plugins to include
                        (e.g., ['@tailwindcss/forms', '@tailwindcss/typography'])
    """

def sync_theme_to_css_vars(theme: TailwindTheme) -> str:
    """Generate CSS custom properties from theme.

    Returns CSS defining custom properties that can be used in
    both Tailwind config and regular CSS.
    """
```

### 1.3 Build Utilities (`ludic.contrib.tailwind.build`)

```python
from pathlib import Path

class TailwindBuilder:
    """Utility for building Tailwind CSS during development and production."""

    def __init__(
        self,
        theme: TailwindTheme,
        input_css: str = "styles/tailwind.css",
        output_css: str = "static/tailwind.css",
        config_path: str = "tailwind.config.js"
    ):
        """Initialize the Tailwind builder."""

    def generate_config(self) -> None:
        """Generate tailwind.config.js from theme."""

    def build(self, minify: bool = True) -> None:
        """Build Tailwind CSS (production build)."""

    def watch(self) -> None:
        """Start Tailwind in watch mode (development)."""

    def check_dependencies(self) -> bool:
        """Check if required dependencies (Node.js, Tailwind CLI) are installed."""


# CLI integration
def main():
    """CLI entry point for building Tailwind CSS.

    Usage:
        python -m ludic.contrib.tailwind.build --watch
        python -m ludic.contrib.tailwind.build --build --minify
    """
```

## 2. Base Pages (`ludic.contrib.tailwind.pages`)

Base page components that include Tailwind CSS and provide consistent page structure.

```python
from typing import override
from ludic.catalog.pages import HtmlPage, Head, Body
from ludic.html import link, script, style as style_tag
from ludic.types import AnyChildren

class TailwindPage(HtmlPage):
    """Base page component with TailwindCSS included.

    Automatically includes:
    - Tailwind CSS (from static file or CDN)
    - Tailwind base styles
    - Optional Tailwind plugins (forms, typography, etc.)

    Example:
        class MyPage(TailwindPage):
            def render(self) -> div:
                return div(
                    h1("Welcome"),
                    p("TailwindCSS is ready!"),
                )
    """

    @override
    def head(self) -> Head:
        """Include Tailwind CSS in the page head."""

    @override
    def body(self) -> Body:
        """Optionally include Tailwind UI scripts."""


class TailwindHead(Head):
    """Head component with Tailwind CSS link."""

    def __init__(
        self,
        *children: AnyChildren,
        css_path: str | None = None,
        use_cdn: bool = False,
        **attrs
    ):
        """Initialize head with Tailwind CSS.

        Args:
            css_path: Path to built Tailwind CSS file
            use_cdn: Use Tailwind Play CDN (development only)
        """
```

## 3. Catalog Components

### 3.1 Buttons (`ludic.contrib.tailwind.catalog.buttons`)

```python
from typing import Literal, override
from ludic.attrs import ButtonAttrs
from ludic.components import Component
from ludic.html import button
from ludic.types import PrimitiveChildren

# Type aliases for better autocomplete
ButtonVariant = Literal["primary", "secondary", "success", "danger", "warning", "info", "outline", "ghost", "link"]
ButtonSize = Literal["xs", "sm", "md", "lg", "xl"]


class Button(Component[PrimitiveChildren, ButtonAttrs]):
    """Tailwind-styled button component.

    Example:
        Button("Click me", variant="primary", size="lg")
        Button("Delete", variant="danger", size="sm", disabled=True)

    Attributes:
        variant: Visual style variant
        size: Button size
        full_width: Whether button takes full width
    """

    classes = [
        # Base styles
        "inline-flex", "items-center", "justify-center",
        "font-medium", "rounded-md", "transition-colors",
        "focus:outline-none", "focus:ring-2", "focus:ring-offset-2",
        "disabled:opacity-50", "disabled:cursor-not-allowed"
    ]

    @override
    def render(self) -> button:
        variant = self.attrs.get("variant", "primary")
        size = self.attrs.get("size", "md")
        full_width = self.attrs.get("full_width", False)

        classes = [
            *self.classes,
            *self._get_variant_classes(variant),
            *self._get_size_classes(size),
        ]

        if full_width:
            classes.append("w-full")

        return button(
            self.children[0],
            **self.attrs_for(button),
            classes=classes
        )

    def _get_variant_classes(self, variant: str) -> list[str]:
        """Get Tailwind classes for button variant."""
        variants = {
            "primary": [
                "bg-primary", "text-white",
                "hover:bg-primary-dark", "focus:ring-primary"
            ],
            "secondary": [
                "bg-secondary", "text-white",
                "hover:bg-secondary-dark", "focus:ring-secondary"
            ],
            "success": [
                "bg-success", "text-white",
                "hover:bg-success/90", "focus:ring-success"
            ],
            "danger": [
                "bg-danger", "text-white",
                "hover:bg-danger/90", "focus:ring-danger"
            ],
            "warning": [
                "bg-warning", "text-white",
                "hover:bg-warning/90", "focus:ring-warning"
            ],
            "info": [
                "bg-info", "text-white",
                "hover:bg-info/90", "focus:ring-info"
            ],
            "outline": [
                "border-2", "border-primary", "text-primary", "bg-transparent",
                "hover:bg-primary", "hover:text-white", "focus:ring-primary"
            ],
            "ghost": [
                "text-gray-700", "bg-transparent",
                "hover:bg-gray-100", "focus:ring-gray-300"
            ],
            "link": [
                "text-primary", "bg-transparent", "underline",
                "hover:text-primary-dark", "focus:ring-primary"
            ],
        }
        return variants.get(variant, variants["primary"])

    def _get_size_classes(self, size: str) -> list[str]:
        """Get Tailwind classes for button size."""
        sizes = {
            "xs": ["px-2.5", "py-1.5", "text-xs"],
            "sm": ["px-3", "py-2", "text-sm"],
            "md": ["px-4", "py-2", "text-base"],
            "lg": ["px-5", "py-3", "text-lg"],
            "xl": ["px-6", "py-4", "text-xl"],
        }
        return sizes.get(size, sizes["md"])


class ButtonGroup(Component[AnyChildren, GlobalAttrs]):
    """Group of buttons displayed together.

    Example:
        ButtonGroup(
            Button("Save", variant="primary"),
            Button("Cancel", variant="outline"),
        )
    """

    @override
    def render(self) -> div:
        return div(
            *self.children,
            classes=[
                "inline-flex", "rounded-md", "shadow-sm",
                *self.attrs.get("classes", [])
            ]
        )


class IconButton(Button):
    """Button with icon support (square, icon-only button).

    Example:
        IconButton(
            Icon("trash"),
            variant="danger",
            size="sm",
            aria_label="Delete item"
        )
    """

    @override
    def _get_size_classes(self, size: str) -> list[str]:
        """Icon buttons use equal padding for square shape."""
        sizes = {
            "xs": ["p-1.5", "text-xs"],
            "sm": ["p-2", "text-sm"],
            "md": ["p-2.5", "text-base"],
            "lg": ["p-3", "text-lg"],
            "xl": ["p-4", "text-xl"],
        }
        return sizes.get(size, sizes["md"])
```

### 3.2 Layouts (`ludic.contrib.tailwind.catalog.layouts`)

```python
from typing import Literal, override
from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import div
from ludic.types import AnyChildren


class Stack(Component[AnyChildren, GlobalAttrs]):
    """Vertical stack layout with consistent spacing.

    Example:
        Stack(
            h1("Title"),
            p("Paragraph 1"),
            p("Paragraph 2"),
            spacing="md"
        )

    Attributes:
        spacing: Space between items (xs, sm, md, lg, xl)
    """

    @override
    def render(self) -> div:
        spacing = self.attrs.get("spacing", "md")

        spacing_classes = {
            "xs": "space-y-1",
            "sm": "space-y-2",
            "md": "space-y-4",
            "lg": "space-y-6",
            "xl": "space-y-8",
        }

        return div(
            *self.children,
            classes=[
                "flex", "flex-col",
                spacing_classes.get(spacing, "space-y-4"),
                *self.attrs.get("classes", [])
            ]
        )


class Box(Component[AnyChildren, GlobalAttrs]):
    """Container with padding and optional border/background.

    Example:
        Box(
            h2("Card Title"),
            p("Card content"),
            padding="lg",
            border=True,
            shadow=True
        )

    Attributes:
        padding: Padding size (sm, md, lg, xl)
        border: Whether to show border
        rounded: Border radius (sm, md, lg, full)
        shadow: Whether to show shadow (sm, md, lg)
        bg: Background color variant
    """

    @override
    def render(self) -> div:
        padding = self.attrs.get("padding", "md")
        border = self.attrs.get("border", False)
        rounded = self.attrs.get("rounded", "md")
        shadow = self.attrs.get("shadow", None)
        bg = self.attrs.get("bg", "white")

        classes = []

        # Padding
        padding_map = {
            "sm": "p-3",
            "md": "p-4",
            "lg": "p-6",
            "xl": "p-8",
        }
        classes.append(padding_map.get(padding, "p-4"))

        # Border
        if border:
            classes.extend(["border", "border-gray-200"])

        # Rounded
        rounded_map = {
            "sm": "rounded",
            "md": "rounded-md",
            "lg": "rounded-lg",
            "xl": "rounded-xl",
            "full": "rounded-full",
        }
        classes.append(rounded_map.get(rounded, "rounded-md"))

        # Shadow
        if shadow:
            shadow_map = {
                "sm": "shadow-sm",
                "md": "shadow-md",
                "lg": "shadow-lg",
            }
            if isinstance(shadow, str):
                classes.append(shadow_map.get(shadow, "shadow-md"))
            else:
                classes.append("shadow-md")

        # Background
        bg_map = {
            "white": "bg-white",
            "gray": "bg-gray-50",
            "primary": "bg-primary-50",
            "transparent": "bg-transparent",
        }
        classes.append(bg_map.get(bg, "bg-white"))

        # Custom classes
        classes.extend(self.attrs.get("classes", []))

        return div(*self.children, classes=classes)


class Container(Component[AnyChildren, GlobalAttrs]):
    """Responsive container with max-width and centering.

    Example:
        Container(
            h1("Page Title"),
            p("Content"),
            size="lg"
        )

    Attributes:
        size: Max width (sm, md, lg, xl, full)
        padding: Horizontal padding
    """

    @override
    def render(self) -> div:
        size = self.attrs.get("size", "lg")
        padding = self.attrs.get("padding", True)

        size_classes = {
            "sm": "max-w-screen-sm",
            "md": "max-w-screen-md",
            "lg": "max-w-screen-lg",
            "xl": "max-w-screen-xl",
            "2xl": "max-w-screen-2xl",
            "full": "max-w-full",
        }

        classes = [
            "mx-auto",
            size_classes.get(size, "max-w-screen-lg"),
        ]

        if padding:
            classes.extend(["px-4", "sm:px-6", "lg:px-8"])

        classes.extend(self.attrs.get("classes", []))

        return div(*self.children, classes=classes)


class Grid(Component[AnyChildren, GlobalAttrs]):
    """Responsive grid layout.

    Example:
        Grid(
            Card(...),
            Card(...),
            Card(...),
            cols={"sm": 1, "md": 2, "lg": 3},
            gap="md"
        )

    Attributes:
        cols: Number of columns (int or dict with breakpoints)
        gap: Gap between items (sm, md, lg, xl)
    """

    @override
    def render(self) -> div:
        cols = self.attrs.get("cols", {"md": 2, "lg": 3})
        gap = self.attrs.get("gap", "md")

        classes = ["grid"]

        # Grid columns
        if isinstance(cols, int):
            classes.append(f"grid-cols-{cols}")
        elif isinstance(cols, dict):
            for breakpoint, count in cols.items():
                if breakpoint == "default":
                    classes.append(f"grid-cols-{count}")
                else:
                    classes.append(f"{breakpoint}:grid-cols-{count}")

        # Gap
        gap_classes = {
            "sm": "gap-2",
            "md": "gap-4",
            "lg": "gap-6",
            "xl": "gap-8",
        }
        classes.append(gap_classes.get(gap, "gap-4"))

        classes.extend(self.attrs.get("classes", []))

        return div(*self.children, classes=classes)


class Flex(Component[AnyChildren, GlobalAttrs]):
    """Flexible box layout.

    Example:
        Flex(
            div("Left"),
            div("Right"),
            direction="row",
            justify="between",
            align="center",
            gap="md"
        )

    Attributes:
        direction: Flex direction (row, col, row-reverse, col-reverse)
        justify: Justify content (start, end, center, between, around, evenly)
        align: Align items (start, end, center, baseline, stretch)
        wrap: Whether to wrap (True, False, "reverse")
        gap: Gap between items
    """

    @override
    def render(self) -> div:
        direction = self.attrs.get("direction", "row")
        justify = self.attrs.get("justify", "start")
        align = self.attrs.get("align", "stretch")
        wrap = self.attrs.get("wrap", False)
        gap = self.attrs.get("gap", None)

        classes = ["flex"]

        # Direction
        if direction != "row":
            classes.append(f"flex-{direction}")

        # Justify
        justify_map = {
            "start": "justify-start",
            "end": "justify-end",
            "center": "justify-center",
            "between": "justify-between",
            "around": "justify-around",
            "evenly": "justify-evenly",
        }
        classes.append(justify_map.get(justify, "justify-start"))

        # Align
        align_map = {
            "start": "items-start",
            "end": "items-end",
            "center": "items-center",
            "baseline": "items-baseline",
            "stretch": "items-stretch",
        }
        classes.append(align_map.get(align, "items-stretch"))

        # Wrap
        if wrap is True:
            classes.append("flex-wrap")
        elif wrap == "reverse":
            classes.append("flex-wrap-reverse")

        # Gap
        if gap:
            gap_map = {
                "xs": "gap-1",
                "sm": "gap-2",
                "md": "gap-4",
                "lg": "gap-6",
                "xl": "gap-8",
            }
            classes.append(gap_map.get(gap, "gap-4"))

        classes.extend(self.attrs.get("classes", []))

        return div(*self.children, classes=classes)


class Center(Component[AnyChildren, GlobalAttrs]):
    """Horizontally and vertically centered content.

    Example:
        Center(
            h1("Centered Content"),
            min_height="screen"
        )

    Attributes:
        min_height: Minimum height (screen, 64, 96, etc.)
    """

    @override
    def render(self) -> div:
        min_height = self.attrs.get("min_height", None)

        classes = [
            "flex", "items-center", "justify-center",
        ]

        if min_height == "screen":
            classes.append("min-h-screen")
        elif min_height:
            classes.append(f"min-h-{min_height}")

        classes.extend(self.attrs.get("classes", []))

        return div(*self.children, classes=classes)
```

### 3.3 Cards (`ludic.contrib.tailwind.catalog.cards`)

```python
from typing import override
from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import div
from ludic.types import AnyChildren


class Card(Component[AnyChildren, GlobalAttrs]):
    """Card container with optional hover effects.

    Example:
        Card(
            CardHeader(h2("Title")),
            CardBody(p("Content")),
            CardFooter(Button("Action")),
            variant="bordered",
            hoverable=True
        )

    Attributes:
        variant: Card style (bordered, shadow, elevated)
        hoverable: Whether to show hover effect
    """

    @override
    def render(self) -> div:
        variant = self.attrs.get("variant", "shadow")
        hoverable = self.attrs.get("hoverable", False)

        classes = [
            "bg-white",
            "rounded-lg",
            "overflow-hidden",
        ]

        if variant == "bordered":
            classes.extend(["border", "border-gray-200"])
        elif variant == "shadow":
            classes.append("shadow-md")
        elif variant == "elevated":
            classes.append("shadow-lg")

        if hoverable:
            if "shadow" in variant:
                classes.append("hover:shadow-xl")
            classes.append("transition-shadow")

        classes.extend(self.attrs.get("classes", []))

        return div(*self.children, classes=classes)


class CardHeader(Component[AnyChildren, GlobalAttrs]):
    """Card header section.

    Example:
        CardHeader(
            h3("Card Title"),
            subtitle="Optional subtitle"
        )
    """

    @override
    def render(self) -> div:
        return div(
            *self.children,
            classes=[
                "px-6", "py-4",
                "border-b", "border-gray-200",
                "bg-gray-50",
                *self.attrs.get("classes", [])
            ]
        )


class CardBody(Component[AnyChildren, GlobalAttrs]):
    """Card body section.

    Example:
        CardBody(
            p("Card content goes here"),
            padding="lg"
        )
    """

    @override
    def render(self) -> div:
        padding = self.attrs.get("padding", "md")

        padding_map = {
            "sm": ["px-4", "py-3"],
            "md": ["px-6", "py-4"],
            "lg": ["px-8", "py-6"],
        }

        return div(
            *self.children,
            classes=[
                *padding_map.get(padding, padding_map["md"]),
                *self.attrs.get("classes", [])
            ]
        )


class CardFooter(Component[AnyChildren, GlobalAttrs]):
    """Card footer section.

    Example:
        CardFooter(
            ButtonGroup(
                Button("Save"),
                Button("Cancel", variant="outline"),
            )
        )
    """

    @override
    def render(self) -> div:
        return div(
            *self.children,
            classes=[
                "px-6", "py-4",
                "border-t", "border-gray-200",
                "bg-gray-50",
                *self.attrs.get("classes", [])
            ]
        )
```

### 3.4 Forms (`ludic.contrib.tailwind.catalog.forms`)

```python
from typing import Literal, override
from ludic.attrs import (
    FormAttrs, InputAttrs, SelectAttrs,
    TextAreaAttrs, LabelAttrs
)
from ludic.components import Component
from ludic.html import (
    form, input, label, select, option,
    textarea, div, span
)
from ludic.types import AnyChildren, NoChildren


class Form(Component[AnyChildren, FormAttrs]):
    """Form container with consistent spacing.

    Example:
        Form(
            InputField(label="Email", name="email", type="email"),
            InputField(label="Password", name="password", type="password"),
            Button("Submit", type="submit"),
            spacing="md"
        )
    """

    @override
    def render(self) -> form:
        spacing = self.attrs.get("spacing", "md")

        spacing_classes = {
            "sm": "space-y-3",
            "md": "space-y-4",
            "lg": "space-y-6",
        }

        return form(
            *self.children,
            **self.attrs_for(form),
            classes=[
                spacing_classes.get(spacing, "space-y-4"),
                *self.attrs.get("classes", [])
            ]
        )


class FormField(Component[AnyChildren, GlobalAttrs]):
    """Container for a form field with label and input.

    Handles layout and spacing for form fields automatically.
    """

    @override
    def render(self) -> div:
        return div(
            *self.children,
            classes=[
                "flex", "flex-col", "gap-1.5",
                *self.attrs.get("classes", [])
            ]
        )


class Label(Component[PrimitiveChildren, LabelAttrs]):
    """Form label with consistent styling.

    Example:
        Label("Email Address", for_="email", required=True)
    """

    @override
    def render(self) -> label:
        required = self.attrs.get("required", False)

        classes = [
            "block",
            "text-sm",
            "font-medium",
            "text-gray-700",
            *self.attrs.get("classes", [])
        ]

        content = [self.children[0]]
        if required:
            content.append(
                span("*", classes=["text-danger", "ml-1"])
            )

        return label(
            *content,
            **self.attrs_for(label),
            classes=classes
        )


class Input(Component[NoChildren, InputAttrs]):
    """Styled input field.

    Example:
        Input(
            type="email",
            name="email",
            placeholder="you@example.com",
            size="md",
            error=False
        )

    Attributes:
        size: Input size (sm, md, lg)
        error: Whether to show error state
        full_width: Whether input takes full width
    """

    @override
    def render(self) -> input:
        size = self.attrs.get("size", "md")
        error = self.attrs.get("error", False)
        full_width = self.attrs.get("full_width", True)

        base_classes = [
            "rounded-md",
            "border",
            "transition-colors",
            "focus:outline-none",
            "focus:ring-2",
            "focus:ring-offset-0",
            "disabled:opacity-50",
            "disabled:cursor-not-allowed",
        ]

        # Size variants
        size_classes = {
            "sm": ["px-3", "py-1.5", "text-sm"],
            "md": ["px-4", "py-2", "text-base"],
            "lg": ["px-4", "py-3", "text-lg"],
        }

        # State-based styling
        if error:
            state_classes = [
                "border-danger",
                "focus:ring-danger",
                "focus:border-danger",
            ]
        else:
            state_classes = [
                "border-gray-300",
                "focus:ring-primary",
                "focus:border-primary",
            ]

        classes = [
            *base_classes,
            *size_classes.get(size, size_classes["md"]),
            *state_classes,
        ]

        if full_width:
            classes.append("w-full")

        classes.extend(self.attrs.get("classes", []))

        return input(**self.attrs_for(input), classes=classes)


class InputField(Component[NoChildren, InputAttrs]):
    """Complete input field with label and optional error message.

    Example:
        InputField(
            label="Email",
            name="email",
            type="email",
            placeholder="you@example.com",
            error="Invalid email address",
            help_text="We'll never share your email",
            required=True
        )

    Attributes:
        label: Field label
        error: Error message (shows error state if present)
        help_text: Help text shown below input
        required: Whether field is required
    """

    @override
    def render(self) -> FormField:
        field_label = self.attrs.get("label")
        error_msg = self.attrs.get("error")
        help_text = self.attrs.get("help_text")
        required = self.attrs.get("required", False)

        field_id = self.attrs.get("id") or self.attrs.get("name")

        children = []

        # Label
        if field_label:
            children.append(
                Label(
                    field_label,
                    for_=field_id,
                    required=required
                )
            )

        # Input
        children.append(
            Input(
                **self.attrs_for(Input),
                error=bool(error_msg),
                id=field_id
            )
        )

        # Error message
        if error_msg:
            children.append(
                span(
                    error_msg,
                    classes=["text-sm", "text-danger", "mt-1"]
                )
            )

        # Help text
        if help_text and not error_msg:
            children.append(
                span(
                    help_text,
                    classes=["text-sm", "text-gray-500", "mt-1"]
                )
            )

        return FormField(*children)


class Select(Component[AnyChildren, SelectAttrs]):
    """Styled select dropdown.

    Example:
        Select(
            Option("Option 1", value="1"),
            Option("Option 2", value="2"),
            name="choice",
            size="md"
        )
    """

    @override
    def render(self) -> select:
        size = self.attrs.get("size", "md")
        error = self.attrs.get("error", False)

        base_classes = [
            "rounded-md",
            "border",
            "transition-colors",
            "focus:outline-none",
            "focus:ring-2",
            "focus:ring-offset-0",
            "disabled:opacity-50",
            "disabled:cursor-not-allowed",
            "w-full",
        ]

        size_classes = {
            "sm": ["px-3", "py-1.5", "text-sm"],
            "md": ["px-4", "py-2", "text-base"],
            "lg": ["px-4", "py-3", "text-lg"],
        }

        if error:
            state_classes = [
                "border-danger",
                "focus:ring-danger",
            ]
        else:
            state_classes = [
                "border-gray-300",
                "focus:ring-primary",
            ]

        classes = [
            *base_classes,
            *size_classes.get(size, size_classes["md"]),
            *state_classes,
            *self.attrs.get("classes", [])
        ]

        return select(
            *self.children,
            **self.attrs_for(select),
            classes=classes
        )


class Option(Component[PrimitiveChildren, OptionAttrs]):
    """Select option element."""

    @override
    def render(self) -> option:
        return option(
            self.children[0],
            **self.attrs
        )


class TextArea(Component[NoChildren, TextAreaAttrs]):
    """Styled textarea field.

    Example:
        TextArea(
            name="message",
            rows=4,
            placeholder="Enter your message..."
        )
    """

    @override
    def render(self) -> textarea:
        error = self.attrs.get("error", False)

        base_classes = [
            "rounded-md",
            "border",
            "transition-colors",
            "focus:outline-none",
            "focus:ring-2",
            "focus:ring-offset-0",
            "disabled:opacity-50",
            "disabled:cursor-not-allowed",
            "w-full",
            "px-4", "py-2",
        ]

        if error:
            state_classes = [
                "border-danger",
                "focus:ring-danger",
            ]
        else:
            state_classes = [
                "border-gray-300",
                "focus:ring-primary",
            ]

        classes = [
            *base_classes,
            *state_classes,
            *self.attrs.get("classes", [])
        ]

        return textarea(
            **self.attrs_for(textarea),
            classes=classes
        )


class Checkbox(Component[NoChildren, InputAttrs]):
    """Styled checkbox input.

    Example:
        Checkbox(
            name="accept",
            label="I accept the terms",
            checked=True
        )
    """

    @override
    def render(self) -> div:
        field_label = self.attrs.get("label")
        field_id = self.attrs.get("id") or self.attrs.get("name")

        checkbox = input(
            type="checkbox",
            **self.attrs_for(input),
            id=field_id,
            classes=[
                "rounded",
                "border-gray-300",
                "text-primary",
                "focus:ring-primary",
                "focus:ring-offset-0",
                "h-4", "w-4",
            ]
        )

        if field_label:
            return div(
                div(
                    checkbox,
                    label(
                        field_label,
                        for_=field_id,
                        classes=["ml-2", "text-sm", "text-gray-700"]
                    ),
                    classes=["flex", "items-center"]
                )
            )
        else:
            return checkbox
```

### 3.5 Alerts (`ludic.contrib.tailwind.catalog.alerts`)

```python
from typing import Literal, override
from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import div, span, button
from ludic.types import AnyChildren


AlertVariant = Literal["info", "success", "warning", "danger"]


class Alert(Component[AnyChildren, GlobalAttrs]):
    """Alert/message component with variants.

    Example:
        Alert(
            AlertTitle("Success!"),
            AlertDescription("Your changes have been saved."),
            variant="success",
            dismissible=True
        )

    Attributes:
        variant: Alert style (info, success, warning, danger)
        dismissible: Whether to show close button
        icon: Whether to show icon
    """

    @override
    def render(self) -> div:
        variant = self.attrs.get("variant", "info")
        dismissible = self.attrs.get("dismissible", False)

        variant_classes = {
            "info": {
                "bg": "bg-info-50",
                "border": "border-info-200",
                "text": "text-info-800",
            },
            "success": {
                "bg": "bg-success-50",
                "border": "border-success-200",
                "text": "text-success-800",
            },
            "warning": {
                "bg": "bg-warning-50",
                "border": "border-warning-200",
                "text": "text-warning-800",
            },
            "danger": {
                "bg": "bg-danger-50",
                "border": "border-danger-200",
                "text": "text-danger-800",
            },
        }

        styles = variant_classes.get(variant, variant_classes["info"])

        classes = [
            "rounded-md",
            "border",
            "p-4",
            styles["bg"],
            styles["border"],
            styles["text"],
            *self.attrs.get("classes", [])
        ]

        children = list(self.children)

        if dismissible:
            close_btn = button(
                "×",
                type="button",
                classes=[
                    "ml-auto",
                    "text-xl",
                    "font-bold",
                    "opacity-50",
                    "hover:opacity-100",
                    "transition-opacity",
                ],
                onclick="this.parentElement.remove()"
            )
            children.append(close_btn)

        return div(
            *children,
            classes=classes
        )


class AlertTitle(Component[PrimitiveChildren, GlobalAttrs]):
    """Alert title component."""

    @override
    def render(self) -> div:
        return div(
            self.children[0],
            classes=[
                "font-semibold",
                "mb-1",
                *self.attrs.get("classes", [])
            ]
        )


class AlertDescription(Component[AnyChildren, GlobalAttrs]):
    """Alert description/body component."""

    @override
    def render(self) -> div:
        return div(
            *self.children,
            classes=[
                "text-sm",
                *self.attrs.get("classes", [])
            ]
        )
```

### 3.6 Badges (`ludic.contrib.tailwind.catalog.badges`)

```python
from typing import Literal, override
from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import span
from ludic.types import PrimitiveChildren


BadgeVariant = Literal["primary", "secondary", "success", "danger", "warning", "info", "gray"]
BadgeSize = Literal["sm", "md", "lg"]


class Badge(Component[PrimitiveChildren, GlobalAttrs]):
    """Badge component for status indicators and labels.

    Example:
        Badge("New", variant="success", size="sm")
        Badge("99+", variant="danger", dot=True)

    Attributes:
        variant: Badge color variant
        size: Badge size
        dot: Whether to show a dot indicator
        rounded: Whether to use pill shape
    """

    @override
    def render(self) -> span:
        variant = self.attrs.get("variant", "primary")
        size = self.attrs.get("size", "md")
        dot = self.attrs.get("dot", False)
        rounded = self.attrs.get("rounded", False)

        base_classes = [
            "inline-flex",
            "items-center",
            "font-medium",
        ]

        # Size
        size_classes = {
            "sm": ["px-2", "py-0.5", "text-xs"],
            "md": ["px-2.5", "py-1", "text-sm"],
            "lg": ["px-3", "py-1.5", "text-base"],
        }

        # Variant
        variant_classes = {
            "primary": ["bg-primary", "text-white"],
            "secondary": ["bg-secondary", "text-white"],
            "success": ["bg-success", "text-white"],
            "danger": ["bg-danger", "text-white"],
            "warning": ["bg-warning", "text-white"],
            "info": ["bg-info", "text-white"],
            "gray": ["bg-gray-100", "text-gray-800"],
        }

        classes = [
            *base_classes,
            *size_classes.get(size, size_classes["md"]),
            *variant_classes.get(variant, variant_classes["primary"]),
        ]

        # Rounded
        if rounded:
            classes.append("rounded-full")
        else:
            classes.append("rounded")

        classes.extend(self.attrs.get("classes", []))

        children = []

        # Dot indicator
        if dot:
            children.append(
                span(
                    classes=[
                        "w-1.5",
                        "h-1.5",
                        "rounded-full",
                        "bg-current",
                        "mr-1.5",
                    ]
                )
            )

        children.append(self.children[0])

        return span(*children, classes=classes)
```

### 3.7 Navigation (`ludic.contrib.tailwind.catalog.navigation`)

```python
from typing import override
from ludic.attrs import GlobalAttrs, AnchorAttrs
from ludic.components import Component
from ludic.html import nav, a, ul, li, div
from ludic.types import AnyChildren, PrimitiveChildren


class Navigation(Component[AnyChildren, GlobalAttrs]):
    """Navigation container.

    Example:
        Navigation(
            NavBrand("MyApp"),
            NavMenu(
                NavLink("Home", href="/", active=True),
                NavLink("About", href="/about"),
                NavLink("Contact", href="/contact"),
            )
        )
    """

    @override
    def render(self) -> nav:
        return nav(
            div(
                *self.children,
                classes=[
                    "flex",
                    "items-center",
                    "justify-between",
                    "flex-wrap",
                ]
            ),
            classes=[
                "bg-white",
                "shadow",
                "px-4", "py-3",
                *self.attrs.get("classes", [])
            ]
        )


class NavBrand(Component[AnyChildren, GlobalAttrs]):
    """Navigation brand/logo.

    Example:
        NavBrand("MyApp", href="/")
    """

    @override
    def render(self) -> a | div:
        href = self.attrs.get("href")

        classes = [
            "text-xl",
            "font-bold",
            "text-gray-800",
            *self.attrs.get("classes", [])
        ]

        if href:
            return a(*self.children, href=href, classes=classes)
        else:
            return div(*self.children, classes=classes)


class NavMenu(Component[AnyChildren, GlobalAttrs]):
    """Navigation menu container.

    Example:
        NavMenu(
            NavLink("Home", href="/"),
            NavLink("About", href="/about"),
        )
    """

    @override
    def render(self) -> ul:
        return ul(
            *self.children,
            classes=[
                "flex",
                "space-x-1",
                *self.attrs.get("classes", [])
            ]
        )


class NavLink(Component[PrimitiveChildren, AnchorAttrs]):
    """Navigation link.

    Example:
        NavLink("Home", href="/", active=True)

    Attributes:
        active: Whether link is for current page
    """

    @override
    def render(self) -> li:
        active = self.attrs.get("active", False)

        link_classes = [
            "px-4", "py-2",
            "rounded-md",
            "text-sm",
            "font-medium",
            "transition-colors",
        ]

        if active:
            link_classes.extend([
                "bg-primary",
                "text-white",
            ])
        else:
            link_classes.extend([
                "text-gray-700",
                "hover:bg-gray-100",
            ])

        return li(
            a(
                self.children[0],
                **self.attrs_for(a),
                classes=link_classes
            )
        )
```

### 3.8 Tables (`ludic.contrib.tailwind.catalog.tables`)

```python
from typing import override
from ludic.attrs import GlobalAttrs
from ludic.components import Component
from ludic.html import table, thead, tbody, tr, th, td, div
from ludic.types import AnyChildren


class Table(Component[AnyChildren, GlobalAttrs]):
    """Styled table component.

    Example:
        Table(
            TableHead(
                TableRow(
                    TableHeader("Name"),
                    TableHeader("Email"),
                    TableHeader("Role"),
                )
            ),
            TableBody(
                TableRow(
                    TableCell("John Doe"),
                    TableCell("john@example.com"),
                    TableCell("Admin"),
                ),
            ),
            striped=True,
            hoverable=True
        )

    Attributes:
        striped: Whether to stripe rows
        hoverable: Whether rows highlight on hover
        bordered: Whether to show borders
    """

    @override
    def render(self) -> div:
        striped = self.attrs.get("striped", False)
        hoverable = self.attrs.get("hoverable", True)
        bordered = self.attrs.get("bordered", False)

        table_classes = [
            "min-w-full",
            "divide-y",
            "divide-gray-200",
        ]

        if bordered:
            table_classes.append("border")

        # Wrapper for responsive scrolling
        return div(
            table(
                *self.children,
                classes=table_classes
            ),
            classes=[
                "overflow-x-auto",
                "shadow",
                "rounded-lg",
                *self.attrs.get("classes", [])
            ],
            **{"data-striped": str(striped).lower()},
            **{"data-hoverable": str(hoverable).lower()}
        )


class TableHead(Component[AnyChildren, GlobalAttrs]):
    """Table head section."""

    @override
    def render(self) -> thead:
        return thead(
            *self.children,
            classes=[
                "bg-gray-50",
                *self.attrs.get("classes", [])
            ]
        )


class TableBody(Component[AnyChildren, GlobalAttrs]):
    """Table body section."""

    @override
    def render(self) -> tbody:
        return tbody(
            *self.children,
            classes=[
                "bg-white",
                "divide-y",
                "divide-gray-200",
                *self.attrs.get("classes", [])
            ]
        )


class TableRow(Component[AnyChildren, GlobalAttrs]):
    """Table row."""

    @override
    def render(self) -> tr:
        return tr(
            *self.children,
            classes=[
                "hover:bg-gray-50",
                "transition-colors",
                *self.attrs.get("classes", [])
            ]
        )


class TableHeader(Component[AnyChildren, GlobalAttrs]):
    """Table header cell."""

    @override
    def render(self) -> th:
        return th(
            *self.children,
            classes=[
                "px-6", "py-3",
                "text-left",
                "text-xs",
                "font-medium",
                "text-gray-500",
                "uppercase",
                "tracking-wider",
                *self.attrs.get("classes", [])
            ]
        )


class TableCell(Component[AnyChildren, GlobalAttrs]):
    """Table data cell."""

    @override
    def render(self) -> td:
        return td(
            *self.children,
            classes=[
                "px-6", "py-4",
                "whitespace-nowrap",
                "text-sm",
                "text-gray-900",
                *self.attrs.get("classes", [])
            ]
        )
```

### 3.9 Typography (`ludic.contrib.tailwind.catalog.typography`)

```python
from typing import Literal, override
from ludic.attrs import GlobalAttrs, AnchorAttrs
from ludic.components import Component
from ludic.html import h1, h2, h3, h4, h5, h6, p, a, code, pre, blockquote
from ludic.types import PrimitiveChildren, AnyChildren


HeadingLevel = Literal[1, 2, 3, 4, 5, 6]


class Heading(Component[PrimitiveChildren, GlobalAttrs]):
    """Heading component with consistent styling.

    Example:
        Heading("Page Title", level=1)
        Heading("Section Title", level=2, weight="semibold")

    Attributes:
        level: Heading level (1-6)
        weight: Font weight (normal, medium, semibold, bold)
        color: Text color variant
    """

    @override
    def render(self) -> h1 | h2 | h3 | h4 | h5 | h6:
        level = self.attrs.get("level", 1)
        weight = self.attrs.get("weight", "bold")
        color = self.attrs.get("color", "gray-900")

        # Size mapping
        size_classes = {
            1: "text-4xl",
            2: "text-3xl",
            3: "text-2xl",
            4: "text-xl",
            5: "text-lg",
            6: "text-base",
        }

        # Weight mapping
        weight_classes = {
            "normal": "font-normal",
            "medium": "font-medium",
            "semibold": "font-semibold",
            "bold": "font-bold",
        }

        classes = [
            size_classes.get(level, "text-2xl"),
            weight_classes.get(weight, "font-bold"),
            f"text-{color}",
            *self.attrs.get("classes", [])
        ]

        heading_map = {
            1: h1,
            2: h2,
            3: h3,
            4: h4,
            5: h5,
            6: h6,
        }

        heading_tag = heading_map.get(level, h2)
        return heading_tag(self.children[0], classes=classes)


class Paragraph(Component[AnyChildren, GlobalAttrs]):
    """Paragraph component with consistent styling.

    Example:
        Paragraph("Some text content", size="lg", color="gray-600")
    """

    @override
    def render(self) -> p:
        size = self.attrs.get("size", "base")
        color = self.attrs.get("color", "gray-700")

        size_classes = {
            "xs": "text-xs",
            "sm": "text-sm",
            "base": "text-base",
            "lg": "text-lg",
            "xl": "text-xl",
        }

        return p(
            *self.children,
            classes=[
                size_classes.get(size, "text-base"),
                f"text-{color}",
                "leading-relaxed",
                *self.attrs.get("classes", [])
            ]
        )


class Link(Component[PrimitiveChildren, AnchorAttrs]):
    """Styled link component.

    Example:
        Link("Click here", href="/page", external=True)

    Attributes:
        external: Whether link is external (adds icon/indicator)
        variant: Link style (default, subtle, button)
    """

    @override
    def render(self) -> a:
        variant = self.attrs.get("variant", "default")
        external = self.attrs.get("external", False)

        variant_classes = {
            "default": [
                "text-primary",
                "hover:text-primary-dark",
                "underline",
                "transition-colors",
            ],
            "subtle": [
                "text-gray-600",
                "hover:text-gray-900",
                "transition-colors",
            ],
            "button": [
                "inline-flex", "items-center",
                "px-4", "py-2",
                "bg-primary", "text-white",
                "rounded-md",
                "hover:bg-primary-dark",
                "transition-colors",
            ],
        }

        classes = [
            *variant_classes.get(variant, variant_classes["default"]),
            *self.attrs.get("classes", [])
        ]

        attrs = self.attrs_for(a)

        if external:
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener noreferrer"

        return a(self.children[0], **attrs, classes=classes)


class Code(Component[PrimitiveChildren, GlobalAttrs]):
    """Inline code component.

    Example:
        Code("const x = 42")
    """

    @override
    def render(self) -> code:
        return code(
            self.children[0],
            classes=[
                "px-1.5", "py-0.5",
                "bg-gray-100",
                "text-danger",
                "rounded",
                "text-sm",
                "font-mono",
                *self.attrs.get("classes", [])
            ]
        )


class CodeBlock(Component[PrimitiveChildren, GlobalAttrs]):
    """Code block component.

    Example:
        CodeBlock(
            '''def hello():
    print("Hello, world!")''',
            language="python"
        )
    """

    @override
    def render(self) -> pre:
        return pre(
            code(
                self.children[0],
                classes=["font-mono", "text-sm"]
            ),
            classes=[
                "p-4",
                "bg-gray-900",
                "text-gray-100",
                "rounded-lg",
                "overflow-x-auto",
                *self.attrs.get("classes", [])
            ]
        )


class BlockQuote(Component[AnyChildren, GlobalAttrs]):
    """Blockquote component.

    Example:
        BlockQuote(
            p("The only way to do great work is to love what you do."),
            cite="Steve Jobs"
        )
    """

    @override
    def render(self) -> blockquote:
        return blockquote(
            *self.children,
            classes=[
                "border-l-4",
                "border-primary",
                "pl-4",
                "py-2",
                "italic",
                "text-gray-700",
                *self.attrs.get("classes", [])
            ]
        )
```

### 3.10 Additional Components

Other catalog modules to include (abbreviated for brevity):

- **Modals** (`modals.py`): Dialog/modal components with overlay
- **Dropdowns** (`dropdowns.py`): Dropdown menus and select components
- **Tooltips** (`tooltips.py`): Tooltip components (may require JS)
- **Breadcrumbs** (`breadcrumbs.py`): Breadcrumb navigation
- **Pagination** (`pagination.py`): Page navigation components
- **Spinners** (`spinners.py`): Loading spinner components
- **Progress** (`progress.py`): Progress bars and indicators
- **Tabs** (`tabs.py`): Tabbed content interfaces
- **Accordion** (`accordion.py`): Collapsible content sections

## 4. Usage Examples

### 4.1 Basic Setup

```python
# app.py
from ludic.contrib.tailwind.theme import LightTailwindTheme
from ludic.contrib.tailwind.pages import TailwindPage
from ludic.contrib.tailwind.catalog.layouts import Container, Stack
from ludic.contrib.tailwind.catalog.buttons import Button
from ludic.contrib.tailwind.catalog.typography import Heading, Paragraph

# Configure theme
theme = LightTailwindTheme(css_path="/static/tailwind.css")

# Generate Tailwind config
theme.generate_config_file("tailwind.config.js")

# Create page
class HomePage(TailwindPage):
    def render(self):
        return Container(
            Stack(
                Heading("Welcome to Ludic + Tailwind", level=1),
                Paragraph("Build beautiful UIs with type-safe components."),
                Button("Get Started", variant="primary", size="lg"),
                spacing="lg"
            ),
            size="lg"
        )
```

### 4.2 Build Setup

```bash
# Install dependencies
npm install -D tailwindcss

# Build CSS (development)
python -m ludic.contrib.tailwind.build --watch

# Build CSS (production)
python -m ludic.contrib.tailwind.build --build --minify
```

### 4.3 Form Example

```python
from ludic.contrib.tailwind.catalog.forms import (
    Form, InputField, Select, Option, Checkbox, Button
)
from ludic.contrib.tailwind.catalog.cards import Card, CardHeader, CardBody, CardFooter
from ludic.contrib.tailwind.catalog.typography import Heading

def RegistrationForm():
    return Card(
        CardHeader(
            Heading("Create Account", level=2)
        ),
        CardBody(
            Form(
                InputField(
                    label="Full Name",
                    name="name",
                    required=True,
                    placeholder="John Doe"
                ),
                InputField(
                    label="Email",
                    name="email",
                    type="email",
                    required=True,
                    help_text="We'll never share your email"
                ),
                InputField(
                    label="Password",
                    name="password",
                    type="password",
                    required=True,
                    help_text="At least 8 characters"
                ),
                Select(
                    Option("Select a role...", value="", selected=True, disabled=True),
                    Option("Developer", value="dev"),
                    Option("Designer", value="design"),
                    Option("Manager", value="manager"),
                    label="Role",
                    name="role"
                ),
                Checkbox(
                    name="terms",
                    label="I accept the terms and conditions",
                    required=True
                ),
                spacing="md"
            ),
            padding="lg"
        ),
        CardFooter(
            ButtonGroup(
                Button("Register", type="submit", variant="primary", size="md"),
                Button("Cancel", type="button", variant="outline", size="md"),
            )
        )
    )
```

### 4.4 Dashboard Example

```python
from ludic.contrib.tailwind.catalog.layouts import Container, Grid, Stack
from ludic.contrib.tailwind.catalog.cards import Card, CardHeader, CardBody
from ludic.contrib.tailwind.catalog.typography import Heading, Paragraph
from ludic.contrib.tailwind.catalog.badges import Badge
from ludic.contrib.tailwind.catalog.buttons import Button

def Dashboard():
    return Container(
        Stack(
            Heading("Dashboard", level=1),

            Grid(
                Card(
                    CardBody(
                        Stack(
                            div(
                                Paragraph("Total Users", size="sm", color="gray-600"),
                                Badge("↑ 12%", variant="success", size="sm"),
                                classes=["flex", "justify-between", "items-center"]
                            ),
                            Heading("1,234", level=2),
                            spacing="sm"
                        ),
                        padding="lg"
                    ),
                    variant="shadow",
                    hoverable=True
                ),

                Card(
                    CardBody(
                        Stack(
                            div(
                                Paragraph("Revenue", size="sm", color="gray-600"),
                                Badge("↑ 8%", variant="success", size="sm"),
                                classes=["flex", "justify-between", "items-center"]
                            ),
                            Heading("$45,678", level=2),
                            spacing="sm"
                        ),
                        padding="lg"
                    ),
                    variant="shadow",
                    hoverable=True
                ),

                Card(
                    CardBody(
                        Stack(
                            div(
                                Paragraph("Active Sessions", size="sm", color="gray-600"),
                                Badge("↑ 23%", variant="success", size="sm"),
                                classes=["flex", "justify-between", "items-center"]
                            ),
                            Heading("89", level=2),
                            spacing="sm"
                        ),
                        padding="lg"
                    ),
                    variant="shadow",
                    hoverable=True
                ),

                cols={"default": 1, "md": 2, "lg": 3},
                gap="md"
            ),

            Button("Export Data", variant="primary"),

            spacing="lg"
        ),
        size="xl"
    )
```

## 5. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

- [ ] Create `ludic/contrib/tailwind/` module structure
- [ ] Implement `TailwindTheme` class
- [ ] Build theme synchronization utilities
- [ ] Create `TailwindPage` base component
- [ ] Set up build utilities (`build.py`)
- [ ] Write comprehensive tests for theme system

### Phase 2: Core Catalog (Week 3-4)

- [ ] Implement buttons.py (Button, ButtonGroup, IconButton)
- [ ] Implement layouts.py (Stack, Box, Container, Grid, Flex, Center)
- [ ] Implement forms.py (Form, Input, Select, TextArea, Checkbox, etc.)
- [ ] Implement cards.py (Card, CardHeader, CardBody, CardFooter)
- [ ] Implement alerts.py (Alert, AlertTitle, AlertDescription)
- [ ] Implement typography.py (Heading, Paragraph, Link, Code, etc.)
- [ ] Write tests for all core components

### Phase 3: Extended Catalog (Week 5-6)

- [ ] Implement badges.py
- [ ] Implement navigation.py
- [ ] Implement tables.py
- [ ] Implement modals.py
- [ ] Implement dropdowns.py
- [ ] Implement breadcrumbs.py
- [ ] Implement pagination.py
- [ ] Implement spinners.py
- [ ] Implement progress.py
- [ ] Write tests for extended components

### Phase 4: Documentation & Examples (Week 7)

- [ ] Write API documentation for all components
- [ ] Create example applications
- [ ] Write migration guide (native catalog → Tailwind catalog)
- [ ] Create comparison examples
- [ ] Document best practices
- [ ] Add to official Ludic documentation

### Phase 5: Polish & Release (Week 8)

- [ ] Performance optimization
- [ ] Accessibility audit (ARIA attributes, keyboard navigation)
- [ ] Cross-browser testing
- [ ] Create starter templates
- [ ] Publish to PyPI as `ludic[tailwind]`
- [ ] Announce release

## 6. Technical Considerations

### 6.1 Build Pipeline

The module requires Node.js and Tailwind CLI for CSS generation:

```json
// package.json
{
  "name": "ludic-tailwind",
  "scripts": {
    "build:css": "tailwindcss -i ./styles/tailwind.css -o ./static/tailwind.css --minify",
    "watch:css": "tailwindcss -i ./styles/tailwind.css -o ./static/tailwind.css --watch"
  },
  "devDependencies": {
    "tailwindcss": "^3.4.1",
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10"
  }
}
```

### 6.2 Type Safety

All components maintain type safety using Ludic's typing system:

```python
from typing import Literal, TypedDict

class ButtonAttrs(TypedDict, total=False):
    variant: Literal["primary", "secondary", "success", "danger", "warning", "info"]
    size: Literal["xs", "sm", "md", "lg", "xl"]
    full_width: bool
```

### 6.3 Tailwind Configuration

Generated config maps Ludic theme:

```javascript
// tailwind.config.js (generated)
module.exports = {
  content: [
    "./ludic/**/*.py",
    "./your_app/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4ecdc4',
          dark: '#276662',
          light: '#dbf5f3',
        },
        // ... more colors from theme
      },
      fontFamily: {
        primary: ['Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
        // ... more fonts
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### 6.4 CSS Loading Strategy

- **Development**: Include full Tailwind CSS or use CDN fallback
- **Production**: Build and minify CSS with unused classes purged
- **Optimization**: Use JIT mode for fastest rebuilds

### 6.5 Accessibility

All components follow WCAG 2.1 Level AA guidelines:

- Proper ARIA attributes
- Keyboard navigation support
- Focus indicators
- Semantic HTML
- Color contrast compliance

### 6.6 Testing Strategy

```python
# tests/contrib/tailwind/test_buttons.py
def test_button_renders_with_correct_classes():
    btn = Button("Click", variant="primary", size="lg")
    html = btn.to_html()
    assert "bg-primary" in html
    assert "px-5" in html
    assert "py-3" in html
```

## 7. Migration Guide

### From Native Catalog

```python
# Before (native catalog)
from ludic.catalog.buttons import ButtonPrimary
from ludic.catalog.layouts import Stack

# After (Tailwind catalog)
from ludic.contrib.tailwind.catalog.buttons import Button
from ludic.contrib.tailwind.catalog.layouts import Stack

# Usage change
ButtonPrimary("Save")  # Before
Button("Save", variant="primary")  # After
```

### Theme Mapping

| Native Catalog | Tailwind Catalog |
|----------------|------------------|
| `theme.colors.primary` | `bg-primary`, `text-primary` |
| `theme.sizes.xl` | `space-y-8`, `p-8` |
| `theme.rounding.normal` | `rounded-md` |
| `theme.fonts.primary` | `font-primary` |

## 8. FAQ

**Q: Can I use this alongside the native catalog?**
A: Yes! Both catalogs can coexist. Import from different paths.

**Q: Do I need Node.js?**
A: Yes, for building optimized CSS. Development can use CDN.

**Q: Is this production-ready?**
A: After implementation and testing phases, yes.

**Q: Can I customize Tailwind config?**
A: Yes, either manually edit `tailwind.config.js` or extend `TailwindTheme`.

**Q: What about dark mode?**
A: Use `DarkTailwindTheme` or Tailwind's `dark:` variant classes.

**Q: How big is the CSS bundle?**
A: With JIT and purging: 10-50KB typically. CDN: ~300KB gzipped.

---

## Conclusion

This specification provides a complete blueprint for implementing a TailwindCSS-based catalog for Ludic. The design maintains Ludic's type-safe, component-based philosophy while leveraging Tailwind's utility-first approach and extensive ecosystem.

Key benefits:
- ✅ Developer choice between native and Tailwind catalogs
- ✅ Type-safe components with excellent DX
- ✅ Familiar Tailwind patterns for faster development
- ✅ Production-ready with optimized builds
- ✅ Comprehensive component library
- ✅ Clear migration path

The implementation will require approximately 8 weeks following the roadmap outlined above.
