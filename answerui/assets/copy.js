export async function copyText(textOrPromise) {
  if (typeof textOrPromise === 'string') return navigator.clipboard.writeText(textOrPromise);
  const type = 'text/plain';
  // Safari checks for user activation when write() is called, not when the data is ready.
  const data = Promise.resolve(textOrPromise).then(text => new Blob([text], {type}));
  return navigator.clipboard.write([new ClipboardItem({[type]: data})]);
}
