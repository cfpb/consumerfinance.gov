/**
 * Makes a table row whose first table cell child is a link become the link
 * for the entire table row.
 */
function init() {
  const tables = document.querySelectorAll( '.o-table__row-links' );

  for ( let i = tables.length - 1; i >= 0; i-- ) {
    tables[i].addEventListener( 'click', _tableClicked, false );
  }
}

/**
 * Handle a click of the table.
 *
 * @param {Object} event Mouse event for click on the table.
 */
function _tableClicked( event ) {
  let target = event.target;
  let tagName;
  while ( target.tagName !== 'TR' ) {
    tagName = target.tagName;
    if ( tagName === 'TH' || tagName === 'A' ) {
      return;
    }
    target = target.parentNode;
  }
  window.location.assign( target.querySelector( 'a' ).getAttribute( 'href' ) );
}

module.exports = { init: init };
