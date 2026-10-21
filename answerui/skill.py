"""Style a FastHTML app with answerui: build pages from its components, change how they look through the registry, and check the result

Read this before writing markup for an answerui app, before changing how a page or a component looks, and before adding a component.

answerui styles semantic HTML. A component is a native tag, or a custom tag where HTML has no element for the concept. A variant or a state is an attribute, and a class does only a utility job. `Button('Save', secondary=True)` renders `<button secondary>`. Every rule, component, and behavior lives in one registry, `reg`, and a page carries them all in two headers:

```python
from fasthtml.common import *
from answerui import *
app = FastHTML(hdrs=reg.hdrs())
```

Import answerui after FastHTML. It redefines the constructors it styles, and a later `from fasthtml.common import *` puts FastHTML's plain ones back. The headers render from the registry per response. A rule registered after the app starts is in the next page.

## Building a page

A page is native HTML. Headings, paragraphs, lists, code, and links are styled by the base layer with no attribute. A table is styled by the base layer too: it hugs its content, scrolls sideways when wider than its container, and a cell marked `num` holds a number. `Table()` puts one in a frame it fills. Long-form content goes in an element carrying `prose`. Layout is four attributes that go on any element, `stack`, `cluster`, `grid`, and `flow`, and the constructors `Stack`, `Cluster`, `Grid`, and `Flow` add them to a `Div`. A component owns its inner space only, so its parent sets the spacing.

`reg.elements` names every component, `doc(answerui)` lists the modules that define them, and `doc(Button)` describes one. A component's variants are attributes: `Button('Save', secondary=True)`. A link carrying `button` is styled as one: `A('Sign up', href='/signup', button=True)`. A severity is an attribute on any element, and every component inside it takes the colour: `Alert('Saved.', success=True)`, `Badge('3', danger=True)`. A dark island is an element that sets `color-scheme: dark` together with its own `background: var(--n-3)` and `color: var(--n2)`, and the ladders re-derive inside it.

Icons come from fastlucide. Import an icon's constructor and `spritesheet` from `fastlucide.icons`, and render `spritesheet` once in the page body. A sprite icon, or any inline `svg` carrying `icon`, takes the text's colour and size, so pass it no size. A button whose only child is an icon is square. Give it an `aria-label`.

A toast for the next page is queued in the session: `add_toast(sess, 'Saved.', success=True)`. The page renders the queue in its region, `Toasts(*pop_toasts(sess))`, and `setup_toasts(app)` delivers what a route queued beside a fragment response.

## Reading what is registered

`doc(Button)` shows a component's purpose, root selector, declared variants, and rules. `Button.rules['base'].css` is its CSS text, `Button.variants` its variants, and `Button.behaviors` its handlers. `Button.example()` is the markup its preview renders, and it composes into larger markup.

`reg.elements` maps names to components. `reg.layers['app']` lists one layer's rules, and `reg.rules` every rule by key. `reg.contexts` maps context selectors to hues. `reg.behaviors()` is the effective handler per key, with the rule that declared it. `reg.build_css()` and `reg.build_js()` are the assets a page ships.

The registry records what was registered and nothing more. Which rules reach an element, and how a state renders, are questions for a browser.

## How the stylesheet is organised

The stylesheet declares cascade layers in the order `reset, tokens, base, layout, components, app, utilities`. A later layer wins over an earlier one for normal declarations, whatever the specificity of the selectors. A rule you register defaults to `app`, so it beats the framework's own rules. The `hidden` attribute is a utility, so it beats any display a component sets.

Colour derives from `--hue`. Two ladders follow it: the neutral ladder from `--n-3`, the page, to `--n2`, body text, and the vivid ladder from `--v-3`, a wash, to `--v2`. Each rung is a `light-dark()` pair, so `color-scheme` alone decides light or dark. A colour context re-points `--hue` inside its scope. The contexts are `[danger]`, `[warning]`, `[success]`, `[info]`, and `mark`. Space, radius, and type each derive a scale from one base value: `--space`, `--radius`, and `--text`. The derived steps are recomputed on every element, so a base value set on a region rescales that region. Depth derives from `--face` and `--relief`. Rims and shadows follow the face colour, and `--relief: 0` flattens a scope.

A component owns its inner space only. Parents space their children with `gap` through the layout containers `stack`, `cluster`, `grid`, and `flow`, and `prose` styles long-form content.

A behavior is a delegated event handler keyed by `(selector, event[, capture])`. It is installed once per document and runs for every matching element, including elements htmx swaps in later. `&` in a selector stands for the component's root selector, and `:load` is short for `htmx:load`.

## Changing the look

Pick the smallest scope that covers the change. Register the rules at import time in the app module, and every response carries them.

A page-wide change is a token set on the root. Every component that reads the token follows:

```python
reg.rule('theme', ':root { --hue: 150; --radius: 0; }')
```

One component everywhere is a rule on that component. Its CSS nests under the root selector, and a state nests with `&`:

```python
Button.rule('corners', 'border-radius: 0;')
```

A new treatment of a component is a variant. It becomes an attribute the constructor accepts, and `doc(Button)` lists it. Its CSS restates the states it changes, because the base rule's state selectors still apply:

```python
Button.variant('cta', '--pad-block: var(--space); --pad-inline: var(--space2); font-size: var(--text1);', doc='The landing page call to action.')
Button('Start free', cta=True)
```

A change confined to a region is a rule with a selector, or a colour context:

```python
reg.rule('sidebar', '[sidebar] { --space: .75rem; }')
reg.context('[project]', 300)
```

A behavior is replaced by registering the same `(selector, event, capture)` later in registry order. The library's alert removes itself on dismiss. An app that hides it instead registers the same key on the component:

```python
Alert.rule('hide', on={('& > button[dismiss]', 'click'): "el.closest('[alert]').hidden = true"})
```

Registering a key that exists replaces its definition in place and keeps its position, so re-running a library definition never outranks an app override. `reg.remove(key)` removes a rule. A component's root selector is fixed by its first registration.

## Checking the result

In a notebook, `Button.demo()` renders the component's example with the registry's current stylesheet and script in an isolated iframe, so a change followed by `demo()` shows the change. `demo(markup)` renders any composition. `height=` fixes the frame for dialogs, popovers, and other top-layer content the frame cannot measure.

For a measured check, put the same document in Chrome with `fastcdp` and read computed values:

```python
from fastcdp import CDP
cdp = await CDP.launch(headless=True)
page = await cdp.new_page()
await page.set_content(demo_html(Button('Save')))
await page.wait_for_selector('button')
await page.eval("getComputedStyle(document.querySelector('button')).borderRadius")
await page.matched_styles('button')
await cdp.quit()
```

`matched_styles` lists every rule that matches the element, in cascade order. A state renders by forcing it: set `aria-pressed` on the element before reading. The behavior script installs once per document, and a second copy in the same document stacks listeners, so check a behavior in a fresh preview or page.

## Adding a component

A component is a constructor and its base rule:

```python
Notice = hypelt('NoticeBox', css='notice-box { display: block; padding: var(--space); }',
    on={('& [dismiss]', 'click'): "el.closest('notice-box').remove()"})
```

A tag name takes FastHTML's constructor, and the tag is the root selector. A handwritten constructor goes through the decorator form with `sel=`, and its docstring is the description:

```python
@hypelt(sel='aside[banner]')
def Banner(title, *c, **attrs):
    "A notice across the top of a page"
    ...
```

`@example(Notice)` attaches the markup `Notice.demo()` renders. Variants and scoped rules attach as above.

Docs: https://AnswerDotAI.github.io/answerui/skill.html.md"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/14_skill.ipynb.

# %% auto #0
__all__ = ['reg', 'hypelt', 'Registry', 'Hyperelement', 'demo', 'demo_html', 'example']

# %% ../nbs/14_skill.ipynb #a5c5bb77
from .registry import reg, hypelt, Registry, Hyperelement
from .demo import demo, demo_html, example
_all_ = ['reg', 'hypelt', 'Registry', 'Hyperelement', 'demo', 'demo_html', 'example']

