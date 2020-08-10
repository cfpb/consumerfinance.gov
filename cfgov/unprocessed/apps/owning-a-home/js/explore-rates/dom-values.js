const unFormatUSD = require( 'unformat-usd' );

/**
 * Get value(s) of an individual HTML element in the control panel.
 * @param   {string} param Name of parameter to get.
 *                         Usually the HTML element's id attribute.
 * @returns {Object} Hash of element id and its value(s).
 */
function getSelection( param ) {

  const elm = document.querySelector( '#' + param );
  let val;

  if ( !elm ) {
    return val;
  }

  switch ( param ) {
    case 'location':
    case 'rate-structure':
    case 'loan-term':
    case 'loan-type':
    case 'arm-type':
      val = elm.value;
      break;
    default:
      val = unFormatUSD(
        elm.value ||
        elm.getAttribute( 'placeholder' )
      );
  }

  return val;
}

export {
  getSelection
};
