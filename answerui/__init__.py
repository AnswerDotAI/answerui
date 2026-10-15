"""A semantic HTML UI framework for FastHTML apps

Modules:

- `answerui.base`: The reset, the document on the tokens, and prose
- `answerui.behaviors`: The client runtime: delegated event rules that survive htmx swaps
- `answerui.controls`: Buttons, button groups, fields, switches, checkboxes, radios, ranges, and fieldsets
- `answerui.demo`: Isolated rendering of markup with current styles and behaviors, for notebooks and docs
- `answerui.hdrs`: App integration: the headers that carry the registry's assets
- `answerui.layout`: Stack, cluster, grid, and document flow
- `answerui.navigation`: The navbar
- `answerui.overlays`: Popovers, menus, dialogs, drawers, and tooltips
- `answerui.registry`: Defining hyperelements and collecting their styles and behaviors
- `answerui.skill`: Style a FastHTML app with answerui: build pages from its components, change how they look through the registry, and check the result
- `answerui.status`: Feedback, loading, and empty states
- `answerui.surfaces`: Containers and small pieces of visual information
- `answerui.tokens`: The styling surface: colour, space, radius, type, motion, and elevation"""

__version__ = "0.0.1"

from .registry import *
from .behaviors import *
from .demo import *
from .hdrs import *
from .tokens import *
from .base import *
from .layout import *
from .controls import *
from .surfaces import *
from .status import *
from .overlays import *
from .navigation import *
