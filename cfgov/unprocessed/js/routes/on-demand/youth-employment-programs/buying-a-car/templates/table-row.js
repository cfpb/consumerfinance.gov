/**
 * @param {Array|string} items - A list of strings or a single string.
 * @returns {string} An HTML snippet.
 */
function tableRow(items) {
  const finalItems = items instanceof Array ? items : [items];
  const td = finalItems.reduce((memo, item) => `${memo}<td>${item}</td>`, '');

  return `<tr>${td}</tr>`;
}

export default tableRow;
