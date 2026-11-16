"""A semantic HTML UI framework for FastHTML apps

Modules:

- `answerui.base`: The CSS reset, document styles built from the tokens, icon sizing, and prose
- `answerui.behaviors`: The client runtime: delegated event handlers that keep working across htmx swaps
- `answerui.controls`: Native form controls styled through their own states, raised to press and sunken to type into
- `answerui.data`: Tables of structured data
- `answerui.demo`: Isolated rendering of markup with current styles and behaviors, for notebooks and docs
- `answerui.hdrs`: Headers and footer that put the registry's stylesheet, script and icons into an app's pages, inline or served from content-hashed URLs
- `answerui.layout`: Stack, cluster, grid, and document flow
- `answerui.navigation`: The navbar at the top of a page: a brand link, navigation links and actions, with an optional disclosure button for narrow screens
- `answerui.overlays`: Popovers, menus, dialogs, drawers, and tooltips
- `answerui.registry`: Defining hyperelements and collecting their styles and behaviors
- `answerui.skill`: Style a FastHTML app with answerui: build pages from its components, change how they look through the registry, and check the result
- `answerui.status`: Feedback and loading states: alerts, toasts, progress bars, spinners and skeletons
- `answerui.surfaces`: Cards for grouping content, badges for short labels, and avatars for people and teams
- `answerui.tokens`: Design tokens: the shared CSS custom properties for colour, space, radius, type, motion, and elevation"""

__version__ = "0.0.3"
