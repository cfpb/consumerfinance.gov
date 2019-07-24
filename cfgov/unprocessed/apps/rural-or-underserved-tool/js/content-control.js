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
function hideData() {
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

  DT.addClass( '#fileError', 'u-hidden' );
  DT.addClass( '#errorMessage', 'u-hidden' );
  DT.removeClass( '#spinner', 'u-hidden' );

  count.reset();
  this.resetHTML();
  this.showResults();
}

function showResults() {
  // hide search-tool and about
  DT.addClass( '#search-tool', 'u-hidden' );
  hideData();

  // show the results
  DT.removeClass( '#results', 'u-hidden' );
}

/**
 * Show search tool content.
 */
function showSearchTool() {
  // show search-tool and about
  DT.removeClass( '#search-tool', 'u-hidden' );

  // hide the results
  DT.addClass( '#results', 'u-hidden' );

  hideData();
}

/**
 * Clear the body of all the tables (data).
 */
function resetHTML() {
  DT.changeElHTML( 'tbody', '' );
}

/**
 * Show an error message.
 * @param {string} message - An error message.
 */
function error( message ) {
  DT.changeElHTML( '#errorMessage', message );
  DT.removeClass( '#errorMessage', 'u-hidden' );
}

export default {
  setup,
  showResults,
  showSearchTool,
  resetHTML,
  error
};
