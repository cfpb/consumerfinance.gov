/* ==========================================================================
   Common application-wide scripts for rural-or-underserved-tool.
   ========================================================================== */

import Expandable from '@cfpb/cfpb-expandables/src/Expandable.js';
import addressUtils from './address-utils';
import axios from 'axios';
import callCensus from './call-census';
import contentControl from './content-control';
import count from './count';
import DT from './dom-tools';
import fileInput from './file-input';
import Papaparse from 'papaparse';
import ruralCounties from './get-rural-counties';
import textInputs from './text-inputs';
import tiger from './call-tiger';

require( './show-map' );
// Polyfill ES6 Promise for IE11.
require( 'es6-promise' ).polyfill();

// Polyfill SVG classList API for IE11.
if ( !( 'classList' in SVGElement.prototype ) ) {
  Object.defineProperty( SVGElement.prototype, 'classList', {
    get() {
      return {
        contains: className => this.className.baseVal.split( ' ' ).indexOf( className ) !== -1,
        add: className => this.setAttribute( 'class', this.getAttribute( 'class' ) + ' ' + className ),
        remove: className => {
          const removedClass = this.getAttribute( 'class' ).replace( new RegExp( '(\\s|^)' + className + '(\\s|$)', 'g' ), '$2' );
          if ( this.classList.contains( className ) ) {
            this.setAttribute( 'class', removedClass );
          }
        }
      };
    }
  } );
}

Expandable.init();

const MAX_CSV_ROWS = 250;

window.callbacks = {};
window.callbacks.censusAPI = function( data, rural ) {
  const result = {};
  if ( addressUtils.isFound( data.result ) ) {
    result.x = data.result.addressMatches[0].coordinates.x;
    result.y = data.result.addressMatches[0].coordinates.y;

    /*
    In the 2019 tigerweb API the layer IDs/name mappings are as follows:
    84 = Counties
    64 = 2010 Census Urban Clusters
    62 = 2010 Census Urbanized Areas
    */
    axios.all(
      [
        tiger( result.x, result.y, '84' ),
        tiger( result.x, result.y, '64' ),
        tiger( result.x, result.y, '62' )
      ]
    )
      .then( axios.spread( function( censusCounty, censusUC, censusUA ) {
        result.input = data.result.input.address.address;
        result.address = data.result.addressMatches[0].matchedAddress;
        result.countyName = censusCounty.features[0].attributes.BASENAME;

        const fips = censusCounty.features[0].attributes.STATE +
                 censusCounty.features[0].attributes.COUNTY;

        if ( addressUtils.isInCounty( fips, rural ) ) {
          result.type = 'rural';
        } else if ( addressUtils.isRuralCensus( censusUC.features, censusUA.features ) ) {
          result.type = 'rural';
        } else {
          result.type = 'notRural';
        }

        result.id = Date.now();

        addressUtils.render( result );
        count.updateCount( result.type );
      } ) )
      .catch( function( error ) {
        console.log( error );
      } );
  } else {
    result.input = data.result.input.address.address;
    result.address = 'Address not identfied';
    result.countyName = '-';
    result.block = '-';
    result.type = 'notFound';
    count.updateCount( result.type );
    addressUtils.render( result );
  }
};

function processAddresses( addresses ) {
  const processed = [];

  ruralCounties( DT.getEl( '#year' ).value )
    .then( function( rural ) {
      addresses.forEach( function( address, index ) {

        if ( addressUtils.isDup( address, processed ) ) {
          // setup the result to render
          const result = {};
          result.input = address;
          result.address = 'Duplicate';
          result.countyName = '-';
          result.block = '-';
          result.type = 'duplicate';
          addressUtils.render( result );
          count.updateCount( result.type );
        } else {
          // if its not dup
          callCensus( address, rural, 'callbacks.censusAPI' );
          processed.push( address );
        }
      } );
    } );
}

// On submit of address entered manually.
const addressFormDom = document.querySelector( '#geocode' );
addressFormDom.addEventListener( 'submit', function( e ) {
  e.preventDefault();

  window.location.hash = 'rural-or-underserved';
  const addresses = [];

  contentControl.setup();

  [].slice.call( DT.getEls( '.input-address' ) ).forEach(
    function( element ) {
      if ( element.value !== '' ) {
        addresses.push( element.value );
      }
    }
  );

  if ( addresses.length > 1 ) {
    DT.removeClass( '#results-total', 'u-hidden' );
  }

  count.updateAddressCount( addresses.length );
  processAddresses( addresses );
} );

// when file upload is used
const fileChangeDom = document.querySelector( '#file' );
fileChangeDom.addEventListener( 'change', function( evt ) {
  let rowCount = 0;
  const fileElement = DT.getEl( '#file' );
  const fileValue = fileElement.value;

  textInputs.reset();
  DT.getEl( '#file-name' ).value = fileInput.getUploadName( fileValue );

  fileInput.resetError();

  if ( fileInput.isCSV( fileValue ) ) {

    // parse the csv to get the count
    Papaparse.parse( fileElement.files[0], {
      header: true,
      step: function( results, parser ) {
        if ( !addressUtils.isValid( results ) ) {
          parser.abort();
          fileInput.setError(
            'The header row of your CSV file does not match' +
            ' our <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
            ' title="Download CSV template">CSV template</a>.' +
            ' Please adjust your CSV file and try again.'
          );
          return;
        }
        if ( results.data['Street Address'] !== '' ) {
          rowCount++;
        }

      },
      error: function() {
        console.log( arguments );
      },
      complete: function( results, file ) {
        if ( rowCount === 0 ) {
          fileInput.setError(
            'There are no rows in this csv. Please update and try again.'
          );
        }
        if ( rowCount >= MAX_CSV_ROWS ) {
          const leftOver = rowCount - MAX_CSV_ROWS;
          fileInput.setError(
            'You entered ' +
            rowCount +
            ' addresses for ' +
            DT.getEl( '#year' ).value +
            ' safe harbor designation. We have a limit of ' + MAX_CSV_ROWS +
            ' addresses. You can run the first ' + MAX_CSV_ROWS +
            ' now, but please recheck the remaining ' + leftOver + '.'
          );
        }
      }
    } );
  } else {
    fileInput.setError(
      'The file uploaded is not a CSV file. ' +
      'Please try again with a CSV file that uses ' +
      'our <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
      'title="Download CSV template">CSV template</a>.' +
      ' For more information about CSV files, view our' +
      ' Frequently Asked Questions below.'
    );
  }
} );

// on file submission
const geocodeCSVDom = document.querySelector( '#geocode-csv' );
geocodeCSVDom.addEventListener( 'submit', function( evt ) {
  evt.preventDefault();

  window.location.hash = 'rural-or-underserved';
  let fileElement = DT.getEl( '#file-name' );
  const fileValue = fileElement.value;
  if ( fileValue === '' || fileValue === 'No file chosen' ||
       fileValue === null ) {
    fileInput.setError(
      'You have not selected a file. ' +
      'Use the "Select file" button to select the file with your addresses.'
    );

  } else if ( fileInput.isCSV( fileValue ) ) {
    let pass = true;
    let rowCount = 0;
    let addresses = [];
    fileElement = DT.getEl( '#file' );
    textInputs.reset();

    // Parse the csv to get the count.
    Papaparse.parse( fileElement.files[0], {
      header: true,
      step: function( results, parser ) {
        if ( addressUtils.isValid( results ) ) {
          if ( rowCount < MAX_CSV_ROWS && results.data['Street Address'] !== '' ) {
            addresses = addressUtils.pushAddress( results, addresses );
          }
          rowCount++;
        } else {
          parser.abort();
          pass = false;
          fileInput.setError(
            'The header row of your CSV file does not match' +
            ' our <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
            ' title="Download CSV template">CSV template</a>.' +
            ' Please adjust your CSV file and try again.'
          );
        }
      },
      complete: function( results, file ) {
        if ( rowCount === 0 ) {
          pass = false;
          fileInput.setError(
            'There are no rows in this csv. Please update and try again.'
          );
        }
        if ( rowCount >= MAX_CSV_ROWS ) {
          const leftOver = rowCount - MAX_CSV_ROWS;
          fileInput.setError(
            'You entered ' + rowCount + ' addresses for ' +
            DT.getEl( '#year' ).value +
            ' safe harbor designation. We have a limit of ' + MAX_CSV_ROWS +
            ' addresses. You can run the first ' + MAX_CSV_ROWS +
            ' now, but please recheck the remaining ' + leftOver + '.'
          );
        }
        if ( addresses.length > 1 ) {
          DT.removeClass( '#results-total', 'u-hidden' );
        }
        if ( pass === true ) {
          contentControl.setup();
          count.updateAddressCount( addresses.length );
          processAddresses( addresses );
        }
      }
    } );
  } else {
    fileInput.setError(
      'The file uploaded is not a CSV file.' +
      ' Please try again with a CSV file that uses our' +
      ' <a href="https://files.consumerfinance.gov/rural-or-underserved-tool/csv-template.csv"' +
      ' title="Download CSV template">CSV template</a>.' +
      ' For more information about CSV files,' +
      ' view our Frequently Asked Questions below.'
    );
  }

  return false;
} );

// add inputs
const addAnotherLinkDom = document.querySelector( '#add-another' );
addAnotherLinkDom.addEventListener( 'click', function( evt ) {
  evt.preventDefault();
  textInputs.add();
} );

// input blur
const inputAddressDom = document.querySelector( '.input-address' );
inputAddressDom.addEventListener( 'blur', function( evt ) {
  textInputs.toggleError( evt );
} );

// show more rows
DT.bindEvents( '.button-more', 'click', function( evt ) {
  const moreButton = evt.target;
  evt.preventDefault();
  const tableID = DT.getElData( moreButton, 'table' );
  const tableRows = DT.getEls( '#' + tableID + ' tbody tr.data' );
  const tableRowsLength = tableRows.length;
  const lengthShown = Array.prototype.filter.call(
    tableRows, function( item ) {
      return !item.classList.contains( 'u-hidden' );
    }
  ).length;
  for ( let i = lengthShown; i < lengthShown + 10; i++ ) {
    DT.removeClass( tableRows[i], 'u-hidden' );
  }

  if ( lengthShown + 10 >= tableRowsLength ) {
    DT.addClass( '#' + tableID + 'More', 'u-hidden' );
    DT.addClass( '#' + tableID + 'All', 'u-hidden' );
  }
} );

DT.bindEvents( '.view-all', 'click', function( evt ) {
  evt.preventDefault();
  const tableID = DT.getElData( evt.target, 'table' );
  DT.removeClass( '#' + tableID + ' tbody tr.data', 'u-hidden' );
  DT.addClass( '#' + tableID + 'More', 'u-hidden' );
  DT.addClass( '#' + tableID + 'All', 'u-hidden' );
} );

// print
DT.bindEvents( '#print', 'click', window.print.bind( window ) );

// csv download
function detectIE() {
  const ua = window.navigator.userAgent;

  const msie = ua.indexOf( 'MSIE ' );
  if ( msie > 0 ) {

    // IE 10 or older => return version number
    return parseInt(
      ua.substring( msie + 5, ua.indexOf( '.', msie ) ), 10
    );
  }

  const trident = ua.indexOf( 'Trident/' );
  if ( trident > 0 ) {

    // IE 11 => return version number
    const rv = ua.indexOf( 'rv:' );
    return parseInt(
      ua.substring( rv + 3, ua.indexOf( '.', rv ) ), 10
    );
  }

  const edge = ua.indexOf( 'Edge/' );
  if ( edge > 0 ) {

    // IE 12 => return version number
    return parseInt( ua.substring( edge + 5, ua.indexOf( '.', edge ) ), 10 );
  }

  // other browser
  return false;
}

DT.bindEvents( '#download', 'click', function( evt ) {
  evt.preventDefault();
  const theCSV = generateCSV();
  if ( detectIE() === false ) {
    window.open(
      ' data:text/csv;charset=utf-8,' + encodeURIComponent( theCSV )
    );
  } else {
    const blob = new Blob( [ theCSV ], { type: 'text/csv;charset=utf-8,' } );
    navigator.msSaveOrOpenBlob( blob, 'rural-or-underserved.csv' );
  }
} );

function generateCSV() {
  let theCSV = '';
  const date = new Date();
  const day = date.getDate();
  const monthIndex = date.getMonth();
  const year = date.getFullYear();

  theCSV =
    'Address entered, Address identified, County, Rural' +
    ' or underserved?, Date processed\n';

  function _loopHandler( element ) {
    const isHidden = DT.hasClass( DT.getParentEls( '.js-table' ), 'u-hidden' );

    // add a data row, if table isn't hidden (!)
    if ( isHidden === false ) {

      // map cols have colspan and we don't want those
      if ( element.getAttribute( 'colspan' ) === null ) {
        const CSVLabel = element.textContent.replace( 'Show map', '' );
        theCSV += '"' + CSVLabel + '"'; // put the content in first

        if ( element.matches( ':last-child' ) ) {
          theCSV = theCSV + ',' + monthIndex + '/' + day + '/' + year + '\n';
        } else {
          theCSV += ',';
        }
      }
    }
  }

  // loop through each row
  [].slice.call( DT.getEls( '.rout-results-table tbody tr td' ) )
    .forEach( _loopHandler );

  return theCSV;
}
