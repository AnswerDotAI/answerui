"""Live previews for AnswerUI's HTML foundation notebooks."""

from html import escape
from . import assets

_sizer = r"new ResizeObserver(() => frameElement.style.height = document.body.scrollHeight + 2 + 'px').observe(document.body)"
_replay = r'const f = this.parentElement.nextElementSibling; f.srcdoc = f.srcdoc'


class Preview:
    def __init__(self, markup, frame): self.markup, self.frame = markup, frame

    def _repr_mimebundle_(self, include=None, exclude=None):
        return {'text/html': self.frame, 'text/markdown': f'```html\n{self.markup}\n```'}, {'nbdev': {'strip': ['text/html']}}


def preview(
    markup,        # HTML to render
    *,
    css=None,      # Replacement stylesheet; None uses the distributed AnswerUI CSS
    js='',         # Inline module for a live example
    width='100%',  # Frame width as a CSS length
    height=None,   # Fixed height as a CSS length; None fits the content
):
    "Show an isolated, replayable HTML example. Store its markup in the notebook."
    if css is None: css = (assets / 'styles.css').read_text(encoding='utf-8')
    script = f'<script type="module">{js}</script>' if js else ''
    sizer = '' if height else f'<script>{_sizer}</script>'
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
        f'<style>{css} body {{ min-block-size: auto; }}</style></head><body ui>{markup}{script}{sizer}</body></html>')
    frame = (f'<div style="width:{escape(width)}"><div style="text-align:right">'
        f'<button type="button" onclick="{_replay}">Replay preview</button></div>'
        f'<iframe title="AnswerUI preview" srcdoc="{escape(doc, quote=True)}" '
        f'style="display:block;box-sizing:border-box;width:100%;height:{escape(height or "auto")};border:1px solid #ccc"></iframe></div>')
    return Preview(markup, frame)
