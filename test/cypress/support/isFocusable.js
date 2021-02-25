const DISABLEABLE_ELEMENTS = [
  'input', 'button', 'select', 'textarea', 'button', 'object'
];

/**
 * Determines if the given element is focusable
 *
 * Note: This is a naive/simplified version adapted from jQuery UI
 * It does not support image maps, disabled fieldsets, among other things
 *
 * @param {string} $element - element name
 * @returns {boolean} true or false
 */
export default function isFocusable( $element ) {
  const nodeName = $element.prop( 'nodeName' ).toLowerCase();
  return (
    nodeName === 'a' || Boolean( $element.attr( 'tabindex' ) ) || (
      DISABLEABLE_ELEMENTS.includes( nodeName ) && $element.is( ':enabled' )
    )
  ) && $element.is( ':visible' );
}
