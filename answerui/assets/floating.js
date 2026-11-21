let anchorId = 0;

export function positionFloating(trigger, panel, {side = 'bottom', align = 'start', sideOffset = 6, onReferenceHidden} = {}) {
  const doc = trigger.ownerDocument, win = doc.defaultView, events = new win.AbortController();
  const anchored = win.CSS.supports('position-area', 'center'), name = `--answerui-anchor-${++anchorId}`;
  const previousAnchor = trigger.style.anchorName;
  const horizontal = side === 'left' || side === 'right';
  const start = horizontal ? 'top' : (win.getComputedStyle(trigger).direction === 'rtl' ? 'right' : 'left');
  const end = horizontal ? 'bottom' : (start === 'left' ? 'right' : 'left');
  const extent = align === 'center' ? '' : ` span-${align === 'start' ? end : start}`;
  function place() {
    const r = trigger.getBoundingClientRect(), vw = doc.documentElement.clientWidth, vh = doc.documentElement.clientHeight, edge = 8;
    if (!trigger.getClientRects().length || r.bottom < 0 || r.top > vh || r.right < 0 || r.left > vw) return onReferenceHidden?.();
    if (anchored) return;
    const below = vh - r.bottom - sideOffset - edge, above = r.top - sideOffset - edge;
    const right = vw - r.right - sideOffset - edge, left = r.left - sideOffset - edge;
    const extent = horizontal ? panel.scrollWidth : panel.scrollHeight;
    let placed = side;
    if (side === 'bottom' && extent > below && above > below) placed = 'top';
    if (side === 'top' && extent > above && below > above) placed = 'bottom';
    if (side === 'right' && extent > right && left > right) placed = 'left';
    if (side === 'left' && extent > left && right > left) placed = 'right';
    panel.style.setProperty('--floating-available-height', `${Math.max(0, placed === 'top' ? above : placed === 'bottom' ? below : vh - edge * 2)}px`);
    const cross = align === 'center' ? (horizontal ? (r.top + r.bottom - panel.offsetHeight) / 2 : (r.left + r.right - panel.offsetWidth) / 2) :
      (align === 'start' ? start : end) === (horizontal ? 'top' : 'left') ? (horizontal ? r.top : r.left) :
        (horizontal ? r.bottom - panel.offsetHeight : r.right - panel.offsetWidth);
    const x = horizontal ? (placed === 'left' ? r.left - panel.offsetWidth - sideOffset : r.right + sideOffset) : cross;
    const y = horizontal ? cross : (placed === 'top' ? r.top - panel.offsetHeight - sideOffset : r.bottom + sideOffset);
    panel.style.left = `${Math.max(edge, Math.min(x, vw - panel.offsetWidth - edge))}px`;
    panel.style.top = `${Math.max(edge, Math.min(y, vh - panel.offsetHeight - edge))}px`;
  }
  if (anchored) {
    trigger.style.anchorName = previousAnchor ? `${previousAnchor}, ${name}` : name;
    panel.style.positionAnchor = name;
    panel.style.positionArea = `${side}${extent}`;
    panel.style.setProperty(`margin-${{top: 'bottom', bottom: 'top', left: 'right', right: 'left'}[side]}`, `${sideOffset}px`);
  } else {
    win.addEventListener('resize', place, {signal: events.signal});
    doc.addEventListener('scroll', place, {capture: true, signal: events.signal});
  }
  const resize = new win.ResizeObserver(place);
  resize.observe(trigger);
  if (!anchored) resize.observe(panel);
  place();
  return () => {
    events.abort();
    resize.disconnect();
    if (anchored) trigger.style.anchorName = previousAnchor;
    for (const prop of ['position-anchor', 'position-area', 'left', 'top', 'margin-top', 'margin-bottom', 'margin-left', 'margin-right', '--floating-available-height'])
      panel.style.removeProperty(prop);
  };
}

export function mountPopover(trigger, panel, {onOpenChange, ...position} = {}) {
  const win = panel.ownerDocument.defaultView, events = new win.AbortController();
  let stop;
  function update(open) {
    stop?.();
    trigger.setAttribute('aria-expanded', String(open));
    stop = open ? positionFloating(trigger, panel, {...position, onReferenceHidden: () => panel.hidePopover()}) : undefined;
  }
  panel.addEventListener('beforetoggle', event => {
    if (event.target !== panel) return;
    update(event.newState === 'open');
  }, {signal: events.signal});
  panel.addEventListener('click', event => {
    if (event.target.closest('a[href]') && panel.hasAttribute('dropdown')) panel.hidePopover();
  }, {signal: events.signal});
  panel.addEventListener('toggle', event => {
    if (event.target !== panel) return;
    onOpenChange?.(event.newState === 'open');
    if (event.newState === 'open' && panel.hasAttribute('dropdown') && !panel.contains(panel.ownerDocument.activeElement))
      [...panel.querySelectorAll('button:not(:disabled), a[href]:not([aria-disabled=true]), select:not(:disabled), input:not(:disabled), summary')]
        .find(node => !node.closest('[inert]') && node.getClientRects().length)?.focus();
  }, {signal: events.signal});
  update(panel.matches(':popover-open'));
  return () => { events.abort(); stop?.(); trigger.setAttribute('aria-expanded', 'false'); };
}
