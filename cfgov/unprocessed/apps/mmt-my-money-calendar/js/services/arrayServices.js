/**
 * Create a range
 * https://wsvincent.com/javascript-array-range-function/
 * @example range(4) => [0,1,2,3]
 *
 * @param {Number} start first value in range
 * @param {Number} edge last value in range
 * @param {Number} step number to increase each range member by
 */
export function range(start, edge, step) {
  // If only 1 number passed make it the edge and 0 the start
  if (arguments.length === 1) {
    edge = start;
    start = 0;
  }

  // Validate edge/start
  edge = edge || 0;
  step = step || 1;

  // Create array of numbers, stopping before the edge
  let arr = [];
  for (arr; (edge - start) * step > 0; start += step) {
    arr.push(start);
  }

  return arr;
}
