'use strict';

// CommonJS
const $ = require( 'jquery' );
const Expandable = require( '../../organisms/Expandable' );
const secondaryExpandableTarget = require( './secondary-expandable-target' );
require( 'jquery.scrollto' );

/**
 * @param {string} selector - Selector to search for in the document.
 * @param {Function} Constructor - A constructor function.
 * @returns {Array} List of instances that were instantiated.
 */
function instantiateExpandables( selector, Constructor ) {
  var expandable;
  var expandableElement;
  var expandableElements = document.querySelectorAll( selector );
  var expandables = [];

  for ( var i = 0, len = expandableElements.length; i < len; i++ ) {
    expandableElement = expandableElements[i];
    expandable = new Constructor( expandableElement );
    expandable.init();
    expandables.push( expandable );
    secondaryExpandableTarget( expandable, expandableElement );
  }

  return expandables;
}

/**
 * @returns {boolean} False if URL hash isn't valid, true otherwise.
 */
function jumpToAnchorLink() {
  // check for hash value - hash is first priority
  var hash = window.location.hash.substr( 1 ).toLowerCase();
  var re = /^[a-zA-Z0-9\-]*$/;

  // Only allow letters, digits and - symbols in hashes.
  if ( !re.test( hash ) ) { return false; }

  var $el = $( '#' + hash );
  var $expandable = $el.closest( '.o-expandable' );

  if ( hash !== '' &&
       $expandable.length &&
       !$expandable.hasClass( 'expandable__expanded' ) ) {
    $expandable.find( '.o-expandable_target' )[0].click();
    $.scrollTo( $el, {
      duration: 600,
      offset:   -30
    } );
  }

  return true;
}

$( document ).ready( function() {

  jumpToAnchorLink();
  $( window ).on( 'hashchange', function() {
    jumpToAnchorLink();
  } );

  instantiateExpandables( '.o-expandable', Expandable );

} );
