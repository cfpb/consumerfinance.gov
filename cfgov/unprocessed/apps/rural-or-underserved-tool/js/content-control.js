import DT from './dom-tools';
import count from './count';

const monthNames = [
  'January', 'February', 'March', 'April',
  'May', 'June', 'July', 'August', 'September',
  'October', 'November', 'December'
];

/**
 * Hide the data sections. These get shown as needed in addresses.js (render)
 */
function _hideData() {
  DT.addClass( '#rural', 'u-hidden' );
  DT.addClass( '#notRural', 'u-hidden' );
  DT.addClass( '#duplicate', 'u-hidden' );
  DT.addClass( '#notFound', 'u-hidden' );
}


/**
 * Setup the main UI.
 */
function setup() {
  // set year
  const yearValue = document.querySelector( '#year' ).value;

  DT.changeElText( '.chosenYear', yearValue );
  DT.changeElText( '.chosenYear1', yearValue + 1 );
  DT.changeElText( '.chosenYear2', yearValue + 2 );

  // set report generated date
  const date = new Date();
  const day = date.getDate();
  const monthIndex = date.getMonth();
  const year = date.getFullYear();

  DT.changeElText( '.report-date',
    'Report generated ' + monthNames[monthIndex] + ' ' + day + ', ' + year
  );

  DT.addClass( '#file-error', 'u-hidden' );
  DT.addClass( '#error-message', 'u-hidden' );
  DT.removeClass( '#spinner', 'u-hidden' );

  count.reset();
  _resetHTML();
  _showResults();
}

/**
 * Show the results of a search.
 */
function _showResults() {
  // hide search-tool and about
  DT.addClass( '#search-tool', 'u-hidden' );
  _hideData();

  // show the results
  DT.removeClass( '#results', 'u-hidden' );
}

/**
 * Clear the body of all the tables (data).
 */
function _resetHTML() {
  DT.changeElHTML( 'tbody', '' );
}

export default {
  setup
};
