# AnswerUI source

The notebooks in `nbs/` own the CSS and Python components. The first five derive the palette, typography, layout, controls and interactions. The following notebooks add the FastHTML registry, browser adapter, previews and Python constructors. Read them in sidebar order.

A `#| asset styles.css` cell contains a CSS string. `nbdev-export` joins these sections in notebook and cell order. The palette notebook writes `nbs/palette.css` after fitting the colour ladders; ordinary exports read that file without repeating the calculations. The authored vanilla modules live in `answerui/assets/`. The HTML auto-initialiser, `browser.js`, is exported from the behaviors notebook to that same directory. FastHTML includes it automatically. Plain HTML apps can import `@answerdotai/answerui/browser.js`; Svelte components mount the individual controllers through their own lifecycle instead.

Run `npm run build` to export the styles and Python modules using nbdev from your Python environment. `answerui/assets/` is the asset directory for both distributions. The npm package `@answerdotai/answerui` contains CSS, optional fonts and dependency-free browser modules. The Python distribution `answerui-py` contains those assets, FastHTML constructors and the app registry. No JavaScript bundler is needed to build the library.

Shared styles use the cascade layers `reset`, `tokens`, `base`, `layout`, `components`, `app` and `utilities`. Python app rules normally use `app`. Direct foundation rules stay inside `@scope (:root, [ui]) to ([unstyle])`; opaque widgets can stop the skin with `[unstyle]`. Components own padding; layout containers own gaps.

The HTML lessons use `answerui.preview.preview` to show a markup string in an isolated frame with the built stylesheet. The Python lessons use `demo(page)` with the registry's current app rules and browser adapter. Both keep readable markup in saved notebook outputs rather than repeated copies of the stylesheet. Run `nbdev-test` on changed notebooks and `nbdev-readme` after updating `nbs/index.ipynb`.

In a fastws workspace, include `AnswerDotAI/answerui[dev]` in the repo list. `ws-sync` installs the Python development dependencies, links the npm package and exports its assets before building dependent apps. Consumers declare an ordinary `@answerdotai/answerui` dependency without sibling paths or aliases. Outside the workspace, use the published package or a built package artifact.

## Release

The Python version in `answerui/__init__.py` and the npm version in `package.json` are kept together by Fastship. `ship-release` tags the current version. The tag workflow exports the assets and publishes `@answerdotai/answerui` to npm and `answerui-py` to PyPI. Fastship advances both version files for the next release.

Before the first npm release, publish the reviewed package once with normal authenticated `npm publish`, then configure npm's trusted publisher for owner `AnswerDotAI`, repository `answerui` and workflow `ci.yml`, with **Allow npm publish** selected. Configure PyPI trusted publishing for `answerui-py` with the same repository and workflow. The workflow uses no registry tokens or GitHub environment. Advance both version files with `ship-bump` before the first tag-driven release when that bootstrap npm version already exists.
