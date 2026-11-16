# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
r"""Style a FastHTML app with answerui: build pages from its components, change how they look through the registry, and check the result

notation: /why

- semantic HTML: component = native tag, or custom tag where HTML has none; variant, state: attribute; class: utilities only; `Button('Save', secondary=True)` → `<button secondary>`
- `reg`: registry of every rule, component, behavior; app setup:

```python
from fasthtml.common import *
from answerui.all import *
app = FastHTML(hdrs=reg.hdrs(), ftrs=reg.ftrs())
```

- re-importing `fasthtml.common` after answerui restores unstyled constructors
- headers: rebuilt each response; `reg.serve(app)`: cached, content-hashed URLs

## Building a page

- native HTML: styled with no attribute; long-form: `prose` attribute on its container
- layout attributes, any element: `stack` `cluster` `grid` `flow`; `Stack` `Cluster` `Grid` `Flow`: `Div` with one; component owns inner space only: parent spaces children (`gap`)
- `A('Sign up', href='/signup', button=True)`: link styled as button
- colour contexts: `[danger]` `[warning]` `[success]` `[info]` on any element, `mark`: re-point `--hue` inside: `Alert('Saved.', success=True)`, `Badge('3', danger=True)`
- dark island: `color-scheme: dark; background: var(--n-3); color: var(--n2)`; ladders re-derive inside
- icons: fastlucide, imported at module level, join `reg.ftrs()` sprite sheet: `from fastlucide.icons import Trash_2`; `Button(Trash_2(), aria_label='Remove')`; icon, or `svg` marked `icon`: takes text's colour and size; pass no size; icon-only button: needs `aria-label`
- `Tooltip(control, text)`: inline wrapper
- toasts: `add_toast(sess, 'Saved.', success=True)` → next page's `Toasts(*pop_toasts(sess))`; `setup_toasts(app)`: fragment responses deliver them too

## Reading what is registered

- `reg.elements`: every component; `doc(Button)`, `doc(reg)`; members: `doc(Hyperelement)`, `doc(Registry)`; also `Button.rules[key].css`, `Button.example()` (composable markup), `reg.layers[name]`, `reg.rules[key]`

## How the stylesheet is organised

- layers `reset, tokens, base, layout, components, app, utilities`: later wins for normal declarations, whatever specificity; registered rules default to `app` (beat framework); `hidden`: utility (beats component display)
- colour: `--hue`; neutral ladder `--n-3` (page) to `--n2` (body text); vivid `--v-3` (wash) to `--v2`; rungs `light-dark()`: `color-scheme` picks mode
- scales, one base each: `--space` `--radius` `--text`; recomputed per element: base set on a region rescales it
- depth: `--face`, `--relief` (`0`: flat); `--ring`: focus ring; `--tint`: faceless control's hover
- fonts: IBM Plex; `--font`, `--font-mono`; `--font-heading` on a scope: its headings, e.g. `reg.rule('reading', 'article { --font-heading: var(--font-serif); }')`; own font: `@font-face` + `reg.file(name, path, url)`
- popover: CSS-anchored below opener, flips at viewport edge; inside `anchor` element (e.g. navbar): hangs from its bottom
- behavior: delegated handler keyed `(selector, event[, capture])`, installed once per document, covers htmx swaps; `&`: root selector; `init`: on arrival; `cleanup`: before htmx removal (htmx 2, 4); leading `:` = `htmx:`, any spelling

## Changing the look

- smallest scope covering the change; register at import time in app module    /every response carries it
- page: tokens on root: `reg.rule('theme', ':root { --hue: 150; --radius: 0; }')`
- one component, everywhere: `Button.rule('corners', 'border-radius: 0;')`: nests under root selector, states via `&`
- new treatment: `Button.variant('cta', '--pad-block: var(--space); --pad-inline: var(--space2); font-size: var(--text1);', doc='The landing page call to action.')` → `Button('Start free', cta=True)`, listed in `doc(Button)`; restate each state it changes    /base rule's state selectors still apply
- region: `reg.rule('sidebar', '[sidebar] { --space: .75rem; }')`, or colour context `reg.context('[project]', 300)`
- key registered again: behavior key: later in registry order wins, e.g. dismissed alert hidden, not removed: `Alert.rule('hide', on={('& > button[dismiss]', 'click'): "el.closest('[alert]').hidden = true"})`; rule key: replaced in place, position kept    /re-run library code never outranks app override
- `reg.remove(key)`; root selector: fixed at first registration

## Checking the result

- notebook: `Button.demo()`, `demo(markup)`: current CSS, JS, isolated iframe; `width=` is the viewport: `'24rem'` previews a phone (navbar collapses, popovers flip); stored as HTML frame + Markdown markup: models reading dialog see markup
- registry knows registrations only; which rules reach an element, how a state renders: same document in headless Chrome:

```python
from fastcdp import CDP
cdp = await CDP.launch(headless=True)
page = await cdp.new_page()
await page.set_content(demo_html(Button('Save')))
await page.wait_for_selector('button')
await page.eval("getComputedStyle(document.querySelector('button')).borderRadius")
await page.matched_styles('button')   # every matching rule, cascade order
await cdp.quit()
```

- states: force first, e.g. set `aria-pressed`
- behaviors: fresh preview or page    /second script copy stacks listeners

## Adding a component

- constructor + base rule; tag name: FastHTML's constructor, tag = root selector:

```python
Notice = hypelt('NoticeBox', css='notice-box { display: block; padding: var(--space); }',
    on={('& [dismiss]', 'click'): "el.closest('notice-box').remove()"})
```

- handwritten: decorator, `sel=`, docstring = description:

```python
@hypelt(sel='aside[banner]')
def Banner(title, *c, **attrs):
    "A notice across the top of a page"
    ...
```

- `@example(Notice)`: markup `Notice.demo()` renders
"""
from .all import *
