export function transform(obj, callback, initialValue = {}) {
  return [...Object.entries(obj)].reduce(callback, initialValue);
}
