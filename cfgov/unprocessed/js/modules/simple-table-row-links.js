'use strict';

/**
 * Makes a table row whose first table cell child is a link become the link
 * for the entire table row.
 */
function init() {
  var tables = document.querySelectorAll( '.simple-table__row-links' );

  for ( var i = tables.length - 1; i >= 0; i-- ) {
    tables[i].addEventListener( 'click', _tableClicked, false );
  }
}

/**
 * Handle a click of the table.
 *
 * @param {Object} event Mouse event for click on the table.
 */
function _tableClicked( event ) {
  var target = event.target;
  var tagName;
  while ( target.tagName !== 'TR' ) {
    tagName = target.tagName;
    if ( tagName === 'TH' || tagName === 'A' ) {
      return;
    }
    target = target.parentNode;
  }
  window.location = target.querySelector( 'a' ).getAttribute( 'href' );
}

module.exports = { init: init };
