export function transform(obj, callback, initialValue = {}) {
  return [...Object.entries(obj)].reduce(callback, initialValue);
}

export function pluck(obj, props = []) {
  const output = {};

  for (const prop of props) {
    if (typeof obj[prop] === 'undefined') continue;
    output[prop] = obj[prop];
  }

  return output;
}
