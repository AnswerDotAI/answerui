"""Styles and browser behavior for semantic HTML, with FastHTML components

Modules:

- `answerui.behaviors`: Delegated event-handler runtime (`Registry.build_js`) and `browser.js` DOM hookup for AnswerUI's built-in interactions across htmx swaps.
- `answerui.controls`: FastHTML constructors for native buttons, inputs, groups, toolbars, copy actions, toggles, sliders, fields, and fieldsets styled from browser and ARIA states
- `answerui.data`: Styled data tables (`table[table]`) and horizontally scrolling `DataTable` frames
- `answerui.demo`: Render FastHTML markup in isolated previews with current styles, behaviors, canned htmx routes, and reusable component examples
- `answerui.hdrs`: Inline or content-hashed page headers and footers for the registry's stylesheet, scripts, and icon spritesheet.
- `answerui.layout`: FastHTML constructors for stack, cluster, grid, and document flow layouts
- `answerui.navigation`: Top-of-page navbar (`NavBar`) with a brand link, navigation links, actions, and an optional disclosure button for narrow screens
- `answerui.overlays`: Popovers, menus, dialogs, drawers, and tooltips
- `answerui.registry`: Defining hyperelements and collecting their styles and behaviors
- `answerui.skill`: Build and customise FastHTML interfaces with AnswerUI's shared CSS, native HTML, utilities and browser behavior.
- `answerui.status`: Feedback and loading states: alerts, toasts, progress bars, spinners and skeletons
- `answerui.surfaces`: Cards for grouping content, badges for short labels, and avatars for people and teams"""

__version__ = "0.0.6"




from importlib.resources import files

assets = files(__package__) / 'assets'
