function inlineSize(style, box) {
  const edges = ['Start', 'End'].reduce((n, end) => n + parseFloat(style[`paddingInline${end}`]) +
    parseFloat(style[`borderInline${end}Width`]), 0);
  const size = parseFloat(style.writingMode.startsWith('horizontal') ? style.width : style.height);
  if (box === 'content') return style.boxSizing === 'border-box' ? size - edges : size;
  return style.boxSizing === 'border-box' ? size : size + edges;
}

export function watchInlineFit(host, row, onCompact) {
  const doc = host.ownerDocument, win = doc.defaultView;
  const events = new win.AbortController(), {signal} = events;
  let frame, compact;
  function measure() {
    frame = undefined;
    if (!host.getClientRects().length) return;
    const available = inlineSize(win.getComputedStyle(host), 'content');
    host.setAttribute('data-fitting', '');
    const needed = inlineSize(win.getComputedStyle(row), 'border');
    host.removeAttribute('data-fitting');
    if (!Number.isFinite(needed) || !Number.isFinite(available)) return;
    const next = needed > available;
    if (compact !== next) onCompact(compact = next);
  }
  function schedule() { frame ??= win.requestAnimationFrame(measure); }
  const resize = new win.ResizeObserver(schedule);
  resize.observe(host);
  if (row !== host) resize.observe(row);
  const children = new Set();
  function observeChildren() {
    const next = new Set(row.children);
    for (const child of children) if (!next.has(child)) { resize.unobserve(child); children.delete(child); }
    for (const child of next) if (!children.has(child)) { resize.observe(child); children.add(child); }
  }
  const mutations = new win.MutationObserver(records => {
    if (records.some(r => r.type === 'childList' && r.target === row)) observeChildren();
    if (records.some(r => r.target !== host || r.attributeName !== 'data-fitting')) schedule();
  });
  mutations.observe(row, {subtree: true, attributes: true, childList: true, characterData: true});
  row.addEventListener('load', schedule, {capture: true, signal});
  doc.fonts?.addEventListener('loadingdone', schedule, {signal});
  observeChildren();
  measure();
  return () => {
    events.abort();
    win.cancelAnimationFrame(frame);
    resize.disconnect();
    mutations.disconnect();
  };
}

export function mountNavbar(host, {open = false, onOpenChange} = {}) {
  const doc = host.ownerDocument, root = doc.documentElement;
  const sticky = host.hasAttribute('navbar-sticky') ? new doc.defaultView.ResizeObserver(() =>
    root.style.setProperty('--navbar-size', `${host.offsetHeight}px`)) : null;
  sticky?.observe(host);
  function stopSticky() { sticky?.disconnect(); if (sticky) root.style.removeProperty('--navbar-size'); }
  const row = host.querySelector(':scope > [navbar-row]'), nav = row?.querySelector(':scope > nav');
  const toggle = row?.querySelector(':scope > [navbar-toggle]');
  if (!nav || !toggle) return {setOpen() {}, dispose: stopSticky};
  const events = new doc.defaultView.AbortController();
  let compact, expanded = Boolean(open);
  function setOpen(next) {
    const changed = expanded !== Boolean(next);
    expanded = Boolean(next);
    host.toggleAttribute('data-open', compact && expanded);
    toggle.setAttribute('aria-expanded', String(Boolean(compact && expanded)));
    if (changed) onOpenChange?.(expanded);
  }
  const stop = watchInlineFit(host, row, next => {
    const wasCompact = compact, focus = doc.activeElement;
    compact = next;
    if (compact && nav.contains(focus)) setOpen(true);
    else if (wasCompact && !compact) setOpen(false);
    else setOpen(expanded);
    host.toggleAttribute('data-compact', compact);
    if (wasCompact && !compact && toggle.contains(focus))
      (nav.querySelector('a[href]') ?? row.querySelector('[navbar-brand]'))?.focus({preventScroll: true});
  });
  const {signal} = events;
  toggle.addEventListener('click', () => setOpen(!expanded), {signal});
  doc.addEventListener('click', event => {
    if (compact && expanded && (!host.contains(event.target) || nav.contains(event.target.closest?.('a[href]') ?? null))) setOpen(false);
  }, {signal});
  host.addEventListener('keydown', event => {
    if (!compact || !expanded || event.key !== 'Escape' || event.defaultPrevented) return;
    event.preventDefault();
    setOpen(false);
    toggle.focus({preventScroll: true});
  }, {signal});
  return {setOpen, dispose() {
    events.abort();
    stop();
    stopSticky();
    host.removeAttribute('data-compact');
    host.removeAttribute('data-open');
    toggle.setAttribute('aria-expanded', 'false');
  }};
}
