# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
r"""Build and customise FastHTML interfaces with AnswerUI's shared CSS, native HTML, utilities and browser behavior.

notation: /why

## Pieces and where to read more

- model: shared CSS + vanilla JS foundation (`answerui` npm) paired with thin FastHTML constructors (`answerui-py`) and `reg` for app CSS/events; unmarked HTML stays native, opt-in marker attributes (`btn`, `card`, `stack`, `input`, ...) opt elements in
- Python API: `doc(answerui.<mod>)` and `doc(<Component>)` (signatures, docments, variants, rules, `.example()`); site index: https://AnswerDotAI.github.io/answerui/llms.txt (`<page>.html.md` for every page)
- CSS/JS foundation: `00_palette`..`04_interactions` docs, or read packaged `answerui.assets / 'styles.css'` and `answerui.assets / '*.js'` directly

piece|what it covers|read more
-|-|-
palette & tokens|OKLCH neutral/vivid ladders, `--hue`, light/dark, `ui-tone`, `[ui]` scoping|`00_palette`, `styles.css`
typography & prose|`--text`/`--space`/`--radius` scales, `[prose]`, `[prose-size]`, base `:focus-visible`|`01_typography`, `styles.css`
layout & utilities|`Stack`, `Cluster`, `Grid`, `Flow`, `[grow]`, `@layer utilities`, `[responsive-layout]`|`doc(answerui.layout)`, `02_layout`
controls|`Btn`, `Input`, `Textarea`, `Select`, `Group`, `Toolbar`, `Copy`, `Switch`, `Checkbox`, `Radio`, `Range`, `Field`, `Fieldset`|`doc(answerui.controls)`, `03_controls`
surfaces & data|`Card`, `Badge`, `Avatar`, `DataTable`, `Table(..., table=True)`|`doc(answerui.surfaces, answerui.data)`
status|`Alert`, `Toaster`, `Toast`, `add_toast`, `setup_toasts`, `Progress`, `Spinner`, `Skeleton`|`doc(answerui.status)`
overlays & nav|`Popover`, `Dropdown`, `Dialog` (and drawers), `Tooltip`, `NavBar`|`doc(answerui.overlays, answerui.navigation)`, `04_interactions`
registry, headers, preview|`reg`, `@hypelt`, `reg.serve(app)`/`reg.hdrs()`, delegated JS `on=`, `demo()`, `@example`|`doc(answerui.registry, answerui.hdrs, answerui.behaviors, answerui.demo)`

## Best practices

- setup: `from fasthtml.common import *; from answerui.all import *; app = FastHTML(); reg.serve(app)` for cached content-hashed asset routes + `fastlucide` sprite footer; inline dynamic alternative: `FastHTML(hdrs=reg.hdrs(), ftrs=reg.ftrs())`; bundled IBM Plex faces live in `fonts.css` (optional, select via `--font`/`--font-mono`)
- semantic tags over wrappers: put layout and surface markers directly on native tags (`Section(..., stack=True)`, `Form(..., stack=True)`, `Article(..., card=True)`, `Article(..., prose=True)`, `Ul(..., stack=True)` clears list markers and padding)
- parent owns spacing, component owns padding: `Card` is a surface only (no implicit layout), so pair explicitly (`Card(..., stack=True)`); prefer `@layer utilities` (`cls='gap-2'`) over inline `style='--gap: ...'`
- cascade layers: `reset, tokens, base, layout, components, app, utilities`; register app CSS via `reg.rule` (whole-app tokens or scoped regions), component tweaks via `Btn.rule`, named app variants via `Btn.variant`, custom components via `@hypelt`    /`app` overrides component defaults; `utilities` overrides everything
- idiomatic CSS: prefer native CSS nesting and semantic tokens (`--color-border`, `--color-muted`, `--color-accent`, `--space*`, `--radius*`) over raw ladder steps or hardcoded sizes
- form controls & a11y: `Btn` defaults to `type='button'` (pass `type='submit'` on form submits); use `Checkbox`, `Radio` and `Range`, never `Input(type=...)` (`Input` raises `ValueError`); use unmarked FastHTML `Input` (e.g. `fh.Input`) for `type='file'` or submit inputs; wrap labelled controls in `Field`; pass `icon=True` and `aria_label` on icon-only buttons (`fastlucide` SVGs inherit size and colour); name scrollable `DataTable`s (`role='region', tabindex=0, aria_label='...'`)

## Non-obvious opportunities

- `@layer utilities` (last in cascade — overrides `[stack]`/`[cluster]`/`[grid]`, components and `app` rules cleanly):
  - spacing: `.p-*`, `.px-*`, `.py-*` (`0`, `1`..`4`, `6`), `.gap-*` (`0`, `1`..`4`, `6`, `8`, `12` mapping `0` and `--space-3`..`--space3`), `.mx-auto`
  - flex: `.flex`, `.flex-col`, `.flex-wrap`, `.flex-nowrap`, `.items-start`, `.items-center`, `.justify-center`, `.justify-between`, `.justify-end`, `.flex-1`, `.flex-none`, `.min-w-0`
  - text & visibility: `.text-center`, `.text-muted`, `.truncate`, `.tabular-nums`, `.ui-visually-hidden`, `.ui-hidden`
  - container-query visibility (no viewport breakpoints): `[responsive-layout]` + `.ui-wide-only` or `.ui-compact-only` (`48rem` threshold)
- `[grow]`: `grow=True` on a child of `[stack]` or `[cluster]` sets `flex: 1; min-inline-size: 0; min-block-size: 0`    /pushes trailing actions to the far edge or aligns card footers without custom CSS
- `Btn` links & sizes: `Btn('Sign up', href='/signup', variant='secondary', size='lg')` emits `<a>` without `type`; `size='sm'` and `size='lg'` cover compact and CTA buttons without custom variants
- third-party mounted inputs: `Div(id='card-element', input=True)` styles Stripe Elements or similar containers as an input well
- `Group(inset=True)`: places action buttons inside the input's well border; joined `[toolbar][group]` resets `gap: 0` automatically
- tones & dynamic hues: `ui_tone` (`danger`, `warning`, `success`, `info`, `neutral`) keeps neutral hue for `neutral` and tints components plus standalone `small`/`p` for non-neutral tones (form-level errors outside `Field`); `Div(..., ui=True, ui_theme='dark', style='--hue: 300')` scopes a subtree; add `ui=True` on any element whose state CSS overrides `--hue` dynamically so its lightness ladder recomputes
- declarative browser behaviors (mounted across htmx swaps via `browser.js`): `Btn(..., disabled=True, enable='changed valid')` (form dirty/validity gating), `Checkbox(..., reveals='id')` (show/hide), `Copy(copy=...)` / `Copy(copyfor=...)` (clipboard + feedback), `[btn]` auto-spinner on `aria-busy='true'` or `.htmx-request` (delayed by `--busy-delay`), `Dialog(..., side='start' or 'end')` (slide-over drawers via native `command='show-modal'`/`commandfor`), `Tooltip` (CSS anchor positioning, no JS), `setup_toasts(app)` + `add_toast(sess, ...)` (OOB toasts on htmx fragments too)
- app event handlers: `reg.rule(..., on={(sel, ev): js})` installs delegated document listeners surviving htmx swaps (`&` = component selector; `init`/`cleanup` = element lifetime; leading `:` = htmx event; see `doc(answerui.behaviors)`)
- escape hatches & prose sizing: `[unstyle]` stops `@scope` inheritance for third-party embeds; `[prose-size]` (`sm`, `lg`, `xl`, `2xl`) scales prose; `@layer base` provides `:focus-visible` ring globally
- inspect & preview: `reg.elements`, `Btn.rules`, `Btn.variants`, `Btn.example()`, `demo(markup, width='24rem')` (isolated iframe with current assets/app rules; `nbdev-clean` strips iframe bloat); `reg` describes registrations, not computed layout — inspect real DOM/styles in a browser
"""
from .all import *
