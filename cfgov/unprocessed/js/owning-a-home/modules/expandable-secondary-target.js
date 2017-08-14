'use strict';

const scrollIntoView = require( '../../modules/util/scroll' ).scrollIntoView;

/**
 * @param {string} expandableInstance - Selector to search for in the document.
 * @param {element} element - Expandable base DOM element.
 */
function secondaryExpandableTarget( expandableInstance, element ) {
  const secondaryTarget = element.querySelector( '.o-expandable_target__secondary' );

  secondaryTarget.addEventListener( 'click', () => {
    scrollIntoView( element, {
      duration: 250,
      offset:   30
    } );
    expandableInstance.collapse();
  } );
}

module.exports = secondaryExpandableTarget;
