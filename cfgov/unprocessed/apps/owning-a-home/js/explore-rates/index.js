const $ = require( 'jquery' );
const amortize = require( 'amortize' );
const formatUSD = require( 'format-usd' );
const isNum = require( 'is-money-usd' );
const jumbo = require( 'jumbo-mortgage' );
const median = require( 'median' );
const unFormatUSD = require( 'unformat-usd' );

// Load and style Highcharts library. https://www.highcharts.com/docs.
const Highcharts = require( '../../node_modules/highcharts' );
require( '../../node_modules/highcharts/modules/exporting' )( Highcharts );
const highchartsTheme = require( './highcharts-theme' );
highchartsTheme.applyThemeTo( Highcharts );

// var geolocation = require('./geolocation');
const config = require( '../../config.json' );
const domValues = require( './dom-values' );
const dropdown = require( '../dropdown-utils' );
const fetchRates = require( '../rates' );
const formatTime = require( '../format-timestamp' );
const params = require( './params' );

require( '../../node_modules/rangeslider.js' );
require( './tab' );
require( '../placeholder-polyfill' );

// Load our handlebar templates.
const template = require( './template-loader' );

// Set some properties for the histogram.
var chart = {
  $el:           $( '#chart' ),
  $wrapper:      $( '.chart' ),
  $load:         $( '.data-enabled' ),
  $summary:      $( '#rc-summary' ),
  $timestamp:    $( '#timestamp-p' ),
  $clear:        $( '#rc-summary, #timestamp-p' ),
  isInitialized: false,
  startLoading:  function() {
    removeAlerts();
    this.$load.addClass( 'loading' ).removeClass( 'loaded' );
  },
  stopLoading:   function( state ) {
    this.$wrapper.removeClass( 'geolocating' );
    if( this.$clear.hasClass( 'clear' ) && state !== 'error' ) {
      this.$clear.removeClass( 'clear' );
    }

    if ( state !== 'error' ) {
      this.$load.removeClass( 'loading' ).addClass( 'loaded' );
    }
  }
};

let highChart;

// Set some properties for the credit score slider.
var slider = {
  $el:    $( '#credit-score' ),
  min:    params.getVal( 'credit-score' ),
  max:    params.getVal( 'credit-score' ) + 20,
  step:   20,
  update: function() {
    var leftVal = +Number( $( '.rangeslider__handle' ).css( 'left' ).replace( 'px', '' ) );
    this.min = domValues.getSelection( 'credit-score' );
    if ( this.min === 840 || this.min === '840' ) {
      this.max = this.min + 10;
    } else {
      this.max = this.min + 19;
    }
    $( '#slider-range' ).text( template.sliderLabel( this ) ).css( 'left', leftVal - 9 + 'px' );
  }
};

// options object
// dp-constant: track the down payment interactions
// request: Keep the latest AJAX request accessible so we can terminate it if need be.
var options = {
  'dp-constant': 'percent-down',
  'request':     ''
};

/**
 * Simple (anonymous) delay function
 * @return {object} function that has been delayed
 */
var delay = ( function() {
  var t = 0;
  return function( callback, delay ) {
    clearTimeout( t );
    t = setTimeout( callback, delay );
  };
} )();

/**
 * Get data from the API.
 * @returns {Object} jQuery promise.
 */
function getData() {
  params.update();

  var promise = fetchRates( {
    price:          params.getVal( 'house-price' ),
    loan_amount:    params.getVal( 'loan-amount' ),
    minfico:        slider.min,
    maxfico:        slider.max,
    state:          params.getVal( 'location' ),
    rate_structure: params.getVal( 'rate-structure' ),
    loan_term:      params.getVal( 'loan-term' ),
    loan_type:      params.getVal( 'loan-type' ),
    arm_type:       params.getVal( 'arm-type' )
  } );

  promise.fail( function( request, status, errorThrown ) {
    resultFailWarning();
  } );

  return promise;
}

/**
 * Set value(s) of all HTML elements in the control panel.
 * @param {string} options - TODO: Add description.
 */
function setSelections( options ) {
  for ( var param in params ) {
    setSelection( param, options );
  }
}

/**
 * Set value(s) of an individual HTML element in the control panel.
 * @param  {string} param Name of parameter to set. Usually the HTML element's id attribute.
 * @param  {Object} options Hash of options.
 */
function setSelection( param, options ) {

  var opts = options || {};
  var $el = $( '#' + param );
  var val = opts.value || params.getVal( param );

  switch ( param ) {
    case 'credit-score':
      $el.val( val ).change();
      break;
    default:
      if ( opts.usePlaceholder && $el.is( '[placeholder]' ) ) {
        $el.attr( 'placeholder', val );
      } else {
        $el.val( val );
      }
  }
}

/**
 * Calculate and render the loan amount.
 */
function renderLoanAmount() {
  var loan = unFormatUSD( params.getVal( 'house-price' ) ) - unFormatUSD( params.getVal( 'down-payment' ) );
  if ( loan > 0 ) {
    params.setVal( 'loan-amount', loan );
  } else {
    params.setVal( 'loan-amount', 0 );
  }
  $( '#loan-amount-result' ).text( formatUSD( params.getVal( 'loan-amount' ), { decimalPlaces: 0 } ) );
}

/**
 * Render all applicable rate checker areas.
 */
function updateView() {

  chart.startLoading();

  // reset view
  dropdown( [ 'county', 'loan-term' ] ).hideHighlight();

  // Check ARM
  checkARM();

  var data = {
    labels:       [],
    intLabels:    [],
    uniqueLabels: [],
    vals:         [],
    totalVals:    [],
    largest:      {
      label: 4,
      val:   0
    }
  };

  // Abort the previous request.
  if ( typeof options.request === 'object' ) {
    options.request.abort();
  }

  // And start a new one.
  if ( +Number( params.getVal( 'loan-amount' ) ) === 0 ) {
    resultWarning();
    downPaymentWarning();
  } else {
    options.request = getData();

    // If it succeeds, update the DOM.
    options.request.done( function( results ) {
      // sort results by interest rate, ascending
      var sortedKeys = [],
          sortedResults = {},
          key, x, len;

      for ( key in results.data ) {
        if ( results.data.hasOwnProperty( key ) ) {
          sortedKeys.push( key );
        }
      }

      sortedKeys.sort();
      len = sortedKeys.length;

      for ( x = 0; x < len; x++ ) {
        sortedResults[sortedKeys[x]] = results.data[sortedKeys[x]];
      }

      $.each( sortedResults, function( key, val ) {
        data.intLabels.push( +key );
        data.labels.push( key + '%' );

        data.vals.push( val );
        if ( val > data.largest.val ) {
          data.largest.val = val;
          data.largest.label = key + '%';
        }

        for ( var i = 0; i < val; i++ ) {
          data.totalVals.push( +key );
        }
      } );

      // fade out chart and highlight county if no county is selected
      if ( $( '#county' ).is( ':visible' ) && $( '#county' ).val() === null ) {
        chart.startLoading();
        dropdown( 'county' ).showHighlight();
        $( '#hb-warning' ).addClass( 'u-hidden' );
        return;
      }

      // display an error message if less than 2 results are returned
      if( data.vals.length < 2 ) {
        resultWarning();
        return;
      }

      // display an error message if the downpayment is greater than the house price
      if( +Number( params.getVal( 'house-price' ) ) < +Number( params.getVal( 'down-payment' ) ) ) {
        resultWarning();
        downPaymentWarning();
        return;
      }

      data.uniqueLabels = unique( data.labels.slice( 0 ) );

      chart.stopLoading();
      removeAlerts();
      updateLanguage( data );
      renderAccessibleData( data );
      renderChart( data );

      // Update timestamp
      var _timestamp = results.timestamp;
      try {
        // Safari 8 seems to have a bug with date conversion:
        //    The following: new Date("2015-01-07T05:00:00Z")
        //    Incorrectly returns: Tue Jan 06 2015 21:00:00 GMT-0800 (PST)
        // The following will detect it and will offset the timezone enough
        // to get the correct date (but not time)
        if ( ( new Date( results.timestamp ) ).getDate() !== parseInt( results.timestamp.split( 'T' )[0].split( '-' )[2], 10 ) ) {
          _timestamp = _timestamp.split( 'T' )[0] + 'T15:00:00Z';
        }
      } catch( evt ) {
        // An error occurred.
      }

      renderTime( _timestamp );

      updateComparisons( data );
      renderInterestAmounts();
    } );
  }
}

function unique( arr ) {
  var m = {};
  var newarr = [];
  var v;
  for ( var i = 0, len = arr.length; i < len; i++ ) {
    v = arr[i];
    if ( !m[v] ) {
      newarr.push( v );
      m[v] = true;
    }
  }

  return newarr;
}

/**
 * Updates the sentence above the chart
 * @param {string} data - TODO: Add description.
 */
function updateLanguage( data ) {

  function renderLocation() {
    var state = $( '#location option:selected' ).text();
    $( '.location' ).text( state );
  }

  function renderMedian( data ) {
    var loansMedian = median( data.totalVals ).toFixed( 3 );
    $( '#median-rate' ).text( loansMedian + '%' );
  }

  function updateTerm() {
    var termVal = domValues.getSelection( 'loan-term' );
    $( '.rc-comparison-long .loan-years' ).text( termVal ).fadeIn();
    // change from 5 years to x if an ARM
    if ( domValues.getSelection( 'rate-structure' ) === 'arm' ) {
      var armVal = domValues.getSelection( 'arm-type' );
      var term = armVal.match( /[^-]*/i )[0];
      $( '.rc-comparison-short .loan-years, .arm-comparison-term' ).text( term ).fadeIn();
    } else {
      $( '.rc-comparison-short .loan-years' ).text( 5 ).fadeIn();
    }
  }

  renderLocation();
  renderMedian( data );
  updateTerm( data );
}


/**
 * Get a list of counties from the API for the selected state.
 * @returns {Object} jQuery promise.
 */
function getCounties() {
  return $.get( config.countyAPI, {
    state: params.getVal( 'location' )
  } );

}

/**
 * Request a list of counties and bring them into the DOM.
 */
function loadCounties() {

  // And request 'em.
  var request = getCounties();
  request.done( function( resp ) {

    // If they haven't yet selected a state highlight the field.
    if ( !params.getVal( 'location' ) ) {
      dropdown( 'location' ).showHighlight();
    } else {
      // Empty the current counties and cache the current state so we
      // can monitor if it changes.
      $( '#county' ).html( '' ).data( 'state', params.getVal( 'location' ) );

      // Inject each county into the DOM.
      $.each( resp.data, function( i, countyData ) {
        var countyOption = template.county( countyData );
        $( '#county' ).append( countyOption );
      } );

      // Alphabetize counties
      var countyOptions = $( '#county option' );
      countyOptions.sort( function( x, y ) {
        if ( x.text > y.text ) {
          return 1;
        } else if ( x.text < y.text ) {
          return -1;
        }

        return 0;
      } );

      $( '#county' ).empty().append( countyOptions );

      // Don't select any options by default.
      $( '#county' ).prop( 'selectedIndex', -1 );
    }
  } );

  // Hide loading animation regardless of whether or not we're successful.
  request.then( function() {
    dropdown( 'county' ).hideLoadingAnimation();
  } );
}

/**
 * Check the loan amount and initiate the jumbo loan interactions if need be.
 */
function checkForJumbo() {
  var loan;
  var jumbos = ['jumbo', 'agency', 'fha-hb', 'va-hb'];
  var norms = [ 'conf', 'fha', 'va' ];
  var warnings = {
    conf: template.countyConfWarning,
    fha:  template.countyFHAWarning,
    va:   template.countyVAWarning
  };
  var bounces = { 'fha-hb': 'fha', 'va-hb': 'va' };
  var request;

  loan = jumbo( {
    loanType:   params.getVal( 'loan-type' ),
    loanAmount: params.getVal( 'loan-amount' )
  } );
  dropdown( 'loan-type' ).enable( norms );
  dropdown( 'loan-type' ).hideHighlight();
  $( '#county-warning' ).addClass( 'u-hidden' );

  // if loan is not a jumbo, hide the loan type warning
  if ( $.inArray( params.getVal( 'loan-type' ), jumbos ) < 0 ) {
    $( '#hb-warning' ).addClass( 'u-hidden' );
    dropdown( 'loan-type' ).hideHighlight();
  }

  // If county is not needed and loan-type is a HB loan, bounce it to a regular loan
  if ( !loan.needCounty && $.inArray( params.getVal( 'loan-type' ), jumbos ) >= 0 ) {
    // Change loan-type according to the bounces object
    if ( bounces.hasOwnProperty( params.getVal( 'prevLoanType' ) ) ) {
      params.setVal( 'loan-type', bounces[params.getVal( 'prevLoanType' )] );
      $( '#loan-type' ).val( params.getVal( 'loan-type' ) );
    } else {
      params.setVal( 'loan-type', 'conf' );
      $( '#loan-type' ).val( 'conf' );
    }
    $( '#county-warning, #hb-warning' ).addClass( 'u-hidden' );
    dropdown( 'loan-type' ).enable( norms );
    dropdown( 'loan-type' ).showHighlight();
  }

  // If we don't need to request a county, hide the county dropdown and jumbo options.
  if ( !loan.needCounty && $.inArray( params.getVal( 'loan-type' ), jumbos ) < 0 ) {
    dropdown( 'county' ).hide();
    $( '#county' ).val( '' );
    dropdown( 'loan-type' ).removeOption( jumbos );
    return;
  }

  // Otherwise, make sure the county dropdown is shown.
  dropdown( 'county' ).show();

  // Hide any existing message, then show a message if appropriate.
  $( '#county-warning' ).addClass( 'u-hidden' );
  if ( warnings.hasOwnProperty( params.getVal( 'loan-type' ) ) ) {
    $( '#county-warning' ).removeClass( 'u-hidden' ).find( 'p' ).text( warnings[params.getVal( 'loan-type' )].call() );
  } else {
    $( '#county-warning' ).removeClass( 'u-hidden' ).find( 'p' ).text( template.countyGenWarning() );
  }

  // If the state hasn't changed, we also cool. No need to load new counties.
  if ( $( '#county' ).data( 'state' ) === params.getVal( 'location' ) ) {
    dropdown( 'county' ).hideHighlight();
    return;
  }

  // Let's load us some counties.
  loadCounties();

}

/**
 * Get data for the chosen county
 */
function processCounty() {
  var $counties = $( '#county' );
  var $county = $( '#county' ).find( ':selected' );
  var $loan = dropdown( 'loan-type' );
  var norms = [ 'conf', 'fha', 'va' ];
  var jumbos = [ 'jumbo', 'agency', 'fha-hb', 'va-hb' ];
  var loanTypes = {
    'agency': 'Conforming jumbo',
    'jumbo':  'Jumbo (non-conforming)',
    'fha-hb': 'FHA high-balance',
    'va-hb':  'VA high-balance'
  };
  var loan;

  // If the county field is u-hidden or they haven't selected a county, abort.
  if ( !$counties.is( ':visible' ) || !$counties.val() ) {
    return;
  }

  loan = jumbo( {
    loanType:       params.getVal( 'loan-type' ),
    loanAmount:     params.getVal( 'loan-amount' ),
    gseCountyLimit: parseInt( $county.data( 'gse' ), 10 ),
    fhaCountyLimit: parseInt( $county.data( 'fha' ), 10 ),
    vaCountyLimit:  parseInt( $county.data( 'va' ), 10 )
  } );

  if ( loan.success && loan.isJumbo ) {
    params.setVal( 'isJumbo', true );
    dropdown( 'loan-type' ).removeOption( jumbos );
    dropdown( 'loan-type' ).enable( norms );
    $loan.addOption( {
      label:  loanTypes[loan.type],
      value:  loan.type,
      select: true
    } );
    // If loan-type has changed as a result of the jumbo() operation,
    // make sure everything is updated.
    if ( loan.type !== params.getVal( 'loan-type' ) ) {
      params.setVal( 'prevLoanType', params.getVal( 'loan-type' ) );
      params.setVal( 'loan-type', loan.type );
      dropdown( 'loan-type' ).disable( params.getVal( 'prevLoanType' ) ).showHighlight();
    } else {
      dropdown( 'loan-type' ).hideHighlight();
    }
    // When the loan-type is agency or jumbo, disable conventional.
    if ( $.inArray( params.getVal( 'loan-type' ), [ 'agency', 'jumbo' ] ) >= 0 ) {
      dropdown( 'loan-type' ).disable( 'conf' );
    }
    // Add links to loan messages.
    loan.msg = loan.msg.replace( 'jumbo (non-conforming)', '<a href="/owning-a-home/loan-options/conventional-loans/" target="_blank">jumbo (non-conforming)</a>' );
    loan.msg = loan.msg.replace( 'conforming jumbo', '<a href="/owning-a-home/loan-options/conventional-loans/" target="_blank">conforming jumbo</a>' );
    $( '#hb-warning' ).removeClass( 'u-hidden' ).find( 'p' ).html( loan.msg );

  } else {
    params.setVal( 'isJumbo', false );
    dropdown( 'loan-type' ).removeOption( jumbos );
    dropdown( 'loan-type' ).enable( norms );

    $( '#hb-warning' ).addClass( 'u-hidden' );
    // Select appropriate loan type if loan was kicked out of jumbo
    if ( params.getVal( 'prevLoanType' ) === 'fha-hb' ) {
      $( '#loan-type' ).val( 'fha' );
    } else if ( prevLoanType === 'va-hb' ) {
      $( '#loan-type' ).val( 'va' );
    } else if ( params.getVal( 'prevLoanType' ) === 'va-hb' ) {
      $('#loan-type').val( 'va' );
    }

    if ( $( '#loan-type' ).val === null ) {
      $( '#loan-type' ).val( 'conf' );
    }
  }

  // Hide the county warning.
  $( '#county-warning' ).addClass( 'u-hidden' );
}

/**
 * Updates the sentence data date sentence below the chart
 * @param {string} time - Timestamp from API
 */
function renderTime( time ) {
  if ( time ) {
    time = formatTime( time );
  }

  $( '#timestamp' ).text( time );
}


/**
 * Store the loan amount and down payment, process the county data, check if it's a jumbo loan.
 * @param {HTMLNode} element - TODO: Add description.
 */
function processLoanAmount( element ) {
  var name = $( element ).attr( 'name' );
  // Save the dp-constant value when the user interacts with
  // down payment or down payment percentages.
  if ( name === 'down-payment' || name === 'percent-down' ) {
    options['dp-constant'] = name;
  }

  renderDownPayment.apply( element );
  params.setVal( 'house-price', domValues.getSelection( 'house-price' ) );
  params.setVal( 'down-payment', domValues.getSelection( 'down-payment' ) );
  params.update();
  renderLoanAmount();
  checkForJumbo();
  processCounty();
  updateView();
}

/**
 * Check if the house price entered is 0
 * @param {Object} $price - TODO: Add description.
 * @param {Object} $percent - TODO: Add description.
 * @param {Object} $down - TODO: Add description.
 * @returns {boolean} TODO: Add description.
 */
function checkIfZero( $price, $percent, $down ) {
  if ( params.getVal( 'house-price' ) === '0' ||
       +Number( params.getVal( 'house-price' ) ) === 0 ) {
    removeAlerts();
    chart.stopLoading();
    downPaymentWarning();
    return true;
  } else if ( $percent.attr( 'placeholder' ) === '' ) {
    return false;
  }
}

/**
 * Update either the down payment % or $ amount
 * depending on the input they've changed.
 */
function renderDownPayment() {

  var $el = $( this );
  var $price = $( '#house-price' );
  var $percent = $( '#percent-down' );
  var $down = $( '#down-payment' );
  var val;

  if ( !$el.val() ) {
    return;
  }

  checkIfZero( $price, $percent, $down );

  if ( $price.val() !== 0 ) {
    if ( $el.attr( 'id' ) === 'down-payment' || options['dp-constant'] === 'down-payment' ) {
      val = ( domValues.getSelection( 'down-payment' ) / domValues.getSelection( 'house-price' ) * 100 ) || '';
      $percent.val( Math.round( val ) );
    } else {
      val = domValues.getSelection( 'house-price' ) * ( domValues.getSelection( 'percent-down' ) / 100 );
      val = val >= 0 ? Math.round( val ) : '';
      val = addCommas( val );
      $down.val( val );
    }
  }
}

/**
 * Update the values in the dropdowns in the comparison section
 * @param {Object} data - Data object created by the updateView method.
 */
function updateComparisons( data ) {
  // Update the options in the dropdowns.
  var uniqueLabels = data.uniqueLabels;
  $( '.compare select' ).html( '' );
  $.each( uniqueLabels, function( i, rate ) {
    var option = '<option value="' + rate + '">' + rate + '</option>';
    $( '.compare select' ).append( option );
  } );
  // In the second comparison dropdown, select the last (largest) rate.
  $( '#rate-compare-2' ).val( uniqueLabels[uniqueLabels.length - 1] );
}

/**
 * Calculate and display the interest rates in the comparison section.
 */
function renderInterestAmounts() {
  var shortTermVal = [],
      longTermVal = [],
      rate,
      fullTerm = +( domValues.getSelection( 'loan-term' ) ) * 12;
  $( '.interest-cost' ).each( function( index ) {
    if ( $( this ).hasClass( 'interest-cost-primary' ) ) {
      rate = $( '#rate-compare-1' ).val().replace( '%', '' );
    } else {
      rate = $( '#rate-compare-2' ).val().replace( '%', '' );
    }
    var length = ( parseInt( $( this ).parents( '.rc-comparison-section' ).find( '.loan-years' ).text(), 10 ) ) * 12;
    var amortizedVal = amortize( { amount: params.getVal( 'loan-amount' ), rate: rate, totalTerm: fullTerm, amortizeTerm: length } );
    var totalInterest = amortizedVal.interest;
    var roundedInterest = Math.round( unFormatUSD( totalInterest ) );
    var $el = $( this ).find( '.new-cost' );
    $el.text( formatUSD( roundedInterest, { decimalPlaces: 0 } ) );
    // Add short term rates, interest, and term to the shortTermVal array.
    if ( length < 180 ) {
      shortTermVal.push( {
        rate:     parseFloat( rate ),
        interest: parseFloat( totalInterest ),
        term:     length / 12
      } );
      renderInterestSummary( shortTermVal, 'short' );
    } else {
      longTermVal.push( {
        rate:     parseFloat( rate ),
        interest: parseFloat( totalInterest ),
        term:     length / 12
      } );
      renderInterestSummary( longTermVal, 'long' );
    }
  } );
}

/**
 * Calculate and display the plain language loan comparison summary.
 * @param {Array} intVals - array with two objects containing rate, interest accrued, and term
 * @param {number} term - The term used in the HTML element's ID.
 */
function renderInterestSummary( intVals, term ) {

  var sortedRates;
  var diff;
  var id = '#rc-comparison-summary-' + term;

  sortedRates = intVals.sort( function( a, b ) {
    return a.rate - b.rate;
  } );

  diff = formatUSD( sortedRates[sortedRates.length - 1].interest - sortedRates[0].interest, { decimalPlaces: 0 } );
  $( id + ' .comparison-term' ).text( sortedRates[0].term );
  $( id + ' .rate-diff' ).text( diff );
  $( id + ' .higher-rate' ).text( sortedRates[sortedRates.length - 1].rate + '%' );
  $( id + ' .lower-rate' ).text( sortedRates[0].rate + '%' );
}

/**
 * The dropdowns in the control panel need to change if they have
 * an adjustable rate mortgage.
 */
function checkARM() {
  // reset warning and info
  $( '#arm-warning' ).addClass( 'u-hidden' );
  $( '.arm-info' ).addClass( 'u-hidden' );
  var disallowedTypes = [ 'fha', 'va', 'va-hb', 'fha-hb' ];
  var disallowedTerms = [ '15' ];

  if ( params.getVal( 'rate-structure' ) === 'arm' ) {
    // Reset and highlight if the loan term is disallowed
    if ( disallowedTerms.indexOf( params.getVal( 'loan-term' ) ) !== -1 ) {
      dropdown( 'loan-term' ).reset();
      dropdown( 'loan-term' ).showHighlight();
      $( '#arm-warning' ).removeClass( 'u-hidden' );
    }
    // Reset and highlight if the loan type is disallowed
    if ( disallowedTypes.indexOf( params.getVal( 'loan-type' ) ) !== -1 ) {
      dropdown( 'loan-type' ).reset();
      dropdown( 'loan-type' ).showHighlight();
      $( '#arm-warning' ).removeClass( 'u-hidden' );
    }
    dropdown( 'loan-term' ).disable( '15' );
    dropdown( 'loan-type' ).disable( [ 'fha', 'va' ] );
    dropdown( 'arm-type' ).show();
    $( '.no-arm' ).addClass( 'u-hidden' );
    $( '.arm-info' ).removeClass( 'u-hidden' );
  } else {
    if ( params.getVal( 'isJumbo' ) === false ) {
      dropdown( [ 'loan-term', 'loan-type' ] ).enable();
    }
    dropdown( 'arm-type' ).hide();
    $( '#arm-warning' ).addClass( 'u-hidden' );
    $( '.arm-info' ).addClass( 'u-hidden' );
    $( '.no-arm' ).removeClass( 'u-hidden' );
  }
}

/**
 * Low credit score warning display if user selects a
 * score of 620 or below
 */
function scoreWarning() {
  $( '.rangeslider__handle' ).addClass( 'warning' );
  if ( !$( '.credit-alert' ).length  > 0 ) {
    $( '#slider-range' ).after( template.creditAlert );
  }
  resultWarning();
}

/**
 * Overlays a warning/error message on the chart.
 */
function resultWarning() {
  chart.stopLoading( 'error' );
  $( '#chart-section' ).addClass( 'warning' ).append( template.resultAlert );
}

function resultFailWarning() {
  chart.stopLoading( 'error' );
  $( '#chart-section' ).addClass( 'warning' ).append( template.failAlert );
}

function downPaymentWarning() {
  $( '#loan-amt-inputs' ).append( template.dpWarning );
}


/**
 * Remove alerts and warnings
 */
function removeAlerts() {
  if ( $( '.result-alert' ) ) {
    $( '#chart' ).removeClass( 'warning' );
    $( '.result-alert' ).not('.credit-alert').remove();
    $( '#dp-alert' ).remove();
  }
}


function removeCreditScoreAlert() {
  if ( $( '.credit-alert' ) || $( '.rangeslider__handle' ).hasClass( 'warning' ) ) {
    $( '.rangeslider__handle' ).removeClass( 'warning' );
    $( '.credit-alert' ).remove();
  }
}

/**
 * Add commas to numbers where appropriate.
 * @param {string} value - Old value where commas will be added.
 * return {string} value - Value with commas and no dollar sign.
 */
function addCommas( value ) {
  value = unFormatUSD( value );
  value = formatUSD( value, { decimalPlaces: 0 } )
    .replace( '$', '' );
  return value;
}

/**
 * Initialize the range slider. http://andreruffert.github.io/rangeslider.js/
 * @param {Function} cb - Optional callback.
 */
function renderSlider( cb ) {

  $( '#credit-score' ).rangeslider({
    polyfill:    false,
    rangeClass:  'rangeslider',
    fillClass:   'rangeslider__fill',
    handleClass: 'rangeslider__handle',
    onInit:      function() {
      slider.update();
    },
    onSlide:     function( position, value ) {
      slider.update();
    },
    onSlideEnd:  function( position, value ) {
      params.update();
      if( params.getVal( 'credit-score' ) < 620 ) {
        removeAlerts();
        scoreWarning();
      } else {
        updateView();
        removeCreditScoreAlert();
      }
    }
  } );

  if ( cb ) {
    cb();
  }
}

/**
 * Render chart data in an accessible format.
 * @param {Object} data - Data processed from the API.
 */
function renderAccessibleData( data ) {
  var $tableHead = $( '#accessible-data .table-head' );
  var $tableBody = $( '#accessible-data .table-body' );

  $tableHead.empty();
  $tableBody.empty();

  $.each( data.labels, function( index, value ) {
    $tableHead.append( '<th>' + value + '</th>' );
  } );

  $.each( data.vals, function( index, value ) {
    $tableBody.append( '<td>' + value + '</td>' );
  } );
}

/**
 * Render (or update) the Highcharts chart.
 * @param  {Object} data Data processed from the API.
 * @param  {Function} cb Optional callback.
 * @returns {*} Value of callback invocation or undefined.
 */
function renderChart( data, cb ) {

  if ( chart.isInitialized ) {

    highChart.update( {
      xAxis: {
        categories: data.labels
      },
      series: {
        data: data.vals
      }
    } );

    chart.$wrapper.removeClass( 'geolocating' );
  } else {

    if ( chart.$el.length < 1 ) {
      return;
    }

    chart.$wrapper.addClass( 'geolocating' );

    highChart = new Highcharts.Chart( {
      chart: {
        renderTo: chart.$el[0],
        type: 'column',
        animation: false
      },
      title: {
        text: ''
      },
      xAxis: {
        categories: [ 1, 2, 3, 4, 5 ]
      },
      yAxis: [ {
        title: {
          text: ''
        },
        labels: {
          formatter: function() {
            return this.value > 9 ? this.value + '+' : this.value;
          }
        },
        max: 10,
        min: 0
      }, {
        title: {
          text: 'Number of lenders offering rate'
        }
      } ],
      series: [ {
        name: 'Number of Lenders',
        data: [ 1, 1, 1, 1, 1 ],
        showInLegend: false,
        dataLabels: {
          enabled:   true,
          useHTML:   true,
          crop:      false,
          overflow:  'none',
          defer:     true,
          color:     '#919395',
          x:         2,
          y:         2,
          formatter: function() {
            var point = this.point;
            window.setTimeout( function() {
              if ( point.y > 9 ) {
                point.dataLabel.attr( {
                  y: -32,
                  x: point.plotX - 24
                } );
              }
            } );
            return '<div class="data-label"><span class="data-label_number">' + this.x + '</span><br>|</div>';
          }
        }
      } ],
      credits: {
        text: ''
      },
      tooltip: {
        useHTML: true,
        formatter: function() {
          if ( this.y === 1 ) {
            return template.chartTooltipSingle( this );
          }

          return template.chartTooltipMultiple( this );
        },
        positioner: function( boxWidth, boxHeight, point ) {
          var x, y;
          if ( point.plotY < 0 ) {
            x = point.plotX - 74;
            y = this.chart.plotTop - 74;
          } else {
            x = point.plotX - 54;
            y = point.plotY - 66;
          }
          return {
            x: x,
            y: y
          };
        }
      }
    } );

    chart.isInitialized = true;
  }

  if ( cb ) {
    return cb(); // eslint-disable-line consistent-return
  }

  return; // eslint-disable-line consistent-return
}


/**
 * Initialize the rate checker app.
 * @returns {undefined}
 */
function init() {
  // Only attempt to do things if we're on the rate checker page.
  if ( document.querySelectorAll( '.rate-checker' ).length === 0 ) {
    return;
  }

  renderSlider();
  renderChart();
  renderLoanAmount();
  renderTime();
  setSelections( { usePlaceholder: true } );

/*
  geolocation.getState({timeout: 2000}, function( state ){
    // If a state is returned (meaning they allowed the browser
    // to determine their location).
    if ( state ) {
      params.location = state;
      setSelection('location');
    }
  } );
*/
  updateView();
}

// Have the reset button clear selections.
$( '.defaults-link' ).click( function( evt ) {
  evt.preventDefault();
  setSelections( { usePlaceholder: true } );
  updateView();
  removeCreditScoreAlert();
} );

// ARM highlighting handler.
$( '#rate-structure' ).on( 'change', function() {
  if ( $( this ).val() !== params.getVal( 'rate-structure' ) ) {
    dropdown( 'arm-type' ).showHighlight();
  }
} );

$( '#arm-type' ).on( 'change', function() {
  dropdown( 'arm-type' ).hideHighlight();
} );

// Recalculate everything when drop-down menus are changed.
$( '.demographics, .calc-loan-details, .county' ).on( 'change', '.recalc', function() {
  // If the loan-type is conf, and there's a county visible,
  // then we just exited a HB situation.
  // Clear the county before proceeding.
  $( '#hb-warning' ).addClass( 'u-hidden' );
  // If the state field changed, wipe out county.
  if ( $( this ).attr( 'id' ) === 'location' ) {
    $( '#county' ).html( '' );
    // dropdown('county').hide();
  }
  processLoanAmount( this );
} );

// Prevent non-numeric characters from being entered.
$( '.calc-loan-amt .recalc' ).on( 'keydown', function( event ) {
  var key = event.which,
      allowedKeys = [ 8, 9, 37, 38, 39, 40, 48, 49,
                      50, 51, 52, 53, 54, 55, 56, 57,
                      96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 188, 190 ];

  // If it's not an allowed key OR the shift key is held down (and they're not tabbing)
  // stop everything.
  if ( allowedKeys.indexOf( key ) === -1 || ( event.shiftKey && key !== 9 ) ) {
    event.preventDefault();
  }
} );

// Check if input value is a number.
// If not, replace the character with an empty string.
$( '.calc-loan-amt .recalc' ).on( 'keyup', function( evt ) {
  // on keyup (not tab or arrows), immediately gray chart
  if ( params.getVal( 'verbotenKeys' ).indexOf( evt.which ) === -1 ) {
    chart.startLoading();
  }

} );

// delayed function for processing and updating
$( '.calc-loan-amt, .credit-score' ).on( 'keyup', '.recalc', function( evt ) {
  var element = this;
  // Don't recalculate on TAB or arrow keys.
  if ( params.getVal( 'verbotenKeys' ).indexOf( evt.which ) === -1 ||
       $( this ).hasClass( 'range' ) ) {
    delay( function() {
      processLoanAmount( element );
    }, 500 );
  }
} );

$( '#house-price, #down-payment' ).on( 'focusout', function( evt ) {
  var value;
  value = $( evt.target ).val();
  value = addCommas( value );
  $( evt.target ).val( value );
} );


// Once the user has edited fields, put the kibosh on the placeholders
$( '#house-price, #percent-down, #down-payment' ).on( 'keyup', function() {
  if ( params.getVal( 'edited' ) === false ) {
    // Set the other two fields to their placeholder values.
    $( '#house-price, #percent-down, #down-payment' ).not( $( this ) )
      .each( function( i, val ) {
        $( this ).val( $( this ).attr( 'placeholder' ) );
      } );
    $( '#house-price, #percent-down, #down-payment' ).removeAttr( 'placeholder' );
    params.setVal( 'edited', true );
  }
} );

// Recalculate interest costs.
$( '.compare' ).on( 'change', 'select', renderInterestAmounts );

// Do it!
init();
