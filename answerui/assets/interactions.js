export function mountToolbar(root) {
  const events = new root.ownerDocument.defaultView.AbortController();
  const controls = () => [...root.querySelectorAll('button:not(:disabled), a[href]:not([aria-disabled=true])')]
    .filter(node => !node.closest('[popover]'));
  function focusable(target = controls().find(node => node.tabIndex === 0) ?? controls()[0]) {
    for (const node of controls()) node.tabIndex = node === target ? 0 : -1;
  }
  root.addEventListener('focusin', event => { if (controls().includes(event.target)) focusable(event.target); }, {signal: events.signal});
  root.addEventListener('keydown', event => {
    const items = controls(), current = items.indexOf(event.target);
    if (current < 0 || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const rtl = root.ownerDocument.defaultView.getComputedStyle(root).direction === 'rtl';
    const step = (event.key === 'ArrowRight') !== rtl ? 1 : -1;
    const next = event.key === 'Home' ? items[0] : event.key === 'End' ? items.at(-1) : items[(current + step + items.length) % items.length];
    focusable(next);
    next.focus();
  }, {signal: events.signal});
  const changes = new root.ownerDocument.defaultView.MutationObserver(() => focusable());
  changes.observe(root, {subtree: true, childList: true, attributes: true, attributeFilter: ['disabled', 'aria-disabled']});
  focusable();
  return () => { events.abort(); changes.disconnect(); for (const node of controls()) node.removeAttribute('tabindex'); };
}

export function mountTabs(root, {activationMode = 'automatic', onValueChange} = {}) {
  const win = root.ownerDocument.defaultView, events = new win.AbortController();
  const list = root.querySelector('[role=tablist]'), tabs = () => [...list.querySelectorAll('[role=tab]')];
  function setValue(value, notify = false) {
    const items = tabs(), selected = items.find(tab => tab.dataset.value === value && !tab.disabled) ?? items.find(tab => !tab.disabled);
    for (const tab of items) {
      const active = tab === selected;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      const panel = root.ownerDocument.getElementById(tab.getAttribute('aria-controls'));
      if (panel) panel.hidden = !active;
    }
    if (notify && selected) onValueChange?.(selected.dataset.value);
    return selected?.dataset.value;
  }
  list.addEventListener('click', event => {
    const tab = event.target.closest('[role=tab]');
    if (tab && !tab.disabled) setValue(tab.dataset.value, true);
  }, {signal: events.signal});
  list.addEventListener('keydown', event => {
    const items = tabs().filter(tab => !tab.disabled), current = items.indexOf(event.target);
    const vertical = list.getAttribute('aria-orientation') === 'vertical', rtl = win.getComputedStyle(list).direction === 'rtl';
    const previous = vertical ? 'ArrowUp' : rtl ? 'ArrowRight' : 'ArrowLeft', next = vertical ? 'ArrowDown' : rtl ? 'ArrowLeft' : 'ArrowRight';
    if (current < 0 || ![previous, next, 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    const target = event.key === 'Home' ? items[0] : event.key === 'End' ? items.at(-1) :
      items[(current + (event.key === next ? 1 : -1) + items.length) % items.length];
    for (const tab of tabs()) tab.tabIndex = tab === target ? 0 : -1;
    target.focus();
    if (activationMode === 'automatic') setValue(target.dataset.value, true);
  }, {signal: events.signal});
  setValue(tabs().find(tab => tab.getAttribute('aria-selected') === 'true')?.dataset.value);
  const changes = new win.MutationObserver(() => {
    const current = tabs().find(tab => tab.getAttribute('aria-selected') === 'true');
    setValue(current?.dataset.value, !current || current.disabled);
  });
  changes.observe(list, {subtree: true, childList: true, attributes: true, attributeFilter: ['disabled']});
  return {setValue, dispose() { events.abort(); changes.disconnect(); }};
}

export function mountHoverPopover(trigger, panel, {openDelay = 0, closeDelay = 300} = {}) {
  const win = trigger.ownerDocument.defaultView, events = new win.AbortController();
  let timer;
  function show() { win.clearTimeout(timer); if (!trigger.disabled && !panel.matches(':popover-open')) panel.showPopover({source: trigger}); }
  function leave() {
    win.clearTimeout(timer);
    timer = win.setTimeout(() => {
      if (!panel.contains(panel.ownerDocument.activeElement)) panel.hidePopover();
    }, closeDelay);
  }
  for (const node of [trigger, panel]) {
    node.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse') return;
      win.clearTimeout(timer);
      timer = win.setTimeout(show, openDelay);
    }, {signal: events.signal});
    node.addEventListener('pointerleave', event => { if (event.pointerType === 'mouse') leave(); }, {signal: events.signal});
  }
  trigger.addEventListener('keydown', event => {
    if (event.key !== 'ArrowDown') return;
    event.preventDefault();
    show();
    win.requestAnimationFrame(() => panel.querySelector('select:not(:disabled), button:not(:disabled), input:not(:disabled), a[href]')?.focus());
  }, {signal: events.signal});
  trigger.addEventListener('click', event => { if (event.pointerType === 'touch') show(); }, {signal: events.signal});
  panel.addEventListener('focusout', event => { if (!panel.contains(event.relatedTarget)) leave(); }, {signal: events.signal});
  return () => { events.abort(); win.clearTimeout(timer); };
}
