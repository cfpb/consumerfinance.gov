import isFocusable from './isFocusable';

/**
 * Determines if the given element is focusable using Tab key navigation
 *
 * Note: This is a naive/simplified version adapted from jQuery UI
 * It does not support image maps, disabled fieldsets, among other things
 *
 * @param {string} $element - tab element
 * @returns {number} tab index
 */
export default function isTabbable( $element ) {
  const tabIndex = $element.attr( 'tabindex' );
  return ( !tabIndex || parseInt( tabIndex, 10 ) >= 0 ) &&
    isFocusable( $element );
}
