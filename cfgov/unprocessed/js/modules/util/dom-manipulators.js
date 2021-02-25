import { queryOne } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

/**
 * Shortcut for creating new dom elements.
 * @param {string} tag - The html elem to create.
 * @param {Object} options - The options for building the elem.
 * @returns {HTMLNode} The created elem.
 */
function create( tag, options ) {
  const elem = document.createElement( tag );

  let i;
  for ( i in options ) {
    if ( options.hasOwnProperty( i ) ) {
      const val = options[i];
      let ref;

      if ( i === 'inside' ) {
        ref = queryOne( val );
        ref.appendChild( elem );
      } else if ( i === 'around' ) {
        ref = queryOne( val );
        ref.parentNode.insertBefore( elem, ref );
        elem.appendChild( ref );
      } else if ( i in elem ) {
        elem[i] = val;
      } else {
        elem.setAttribute( i, val );
      }
    }
  }

  return elem;
}

export {
  create
};
