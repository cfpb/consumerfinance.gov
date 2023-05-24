import { convertStringToNumber } from '../../../../js/modules/util/format.js';

/**
 * Get value(s) of an individual HTML element in the control panel.
 * @param {string} param - Name of parameter to get.
 *   Usually the HTML element's id attribute.
 * @returns {undefined|string|number}
 *   A loan text or number value from a DOM element,
 *   or undefined if no source element is found.
 */
function getSelection(param) {
  const elm = document.querySelector('#' + param);
  let val;

  if (!elm) {
    return val;
  }

  switch (param) {
    case 'location':
    case 'rate-structure':
    case 'loan-term':
    case 'loan-type':
    case 'arm-type':
      val = elm.value;
      break;
    default:
      val = convertStringToNumber(elm.value || elm.getAttribute('placeholder'));
  }

  return val;
}

export { getSelection };
