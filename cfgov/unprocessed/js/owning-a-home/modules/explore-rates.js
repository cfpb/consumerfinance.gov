'use strict';

var $ = require( 'jquery' );
var Highcharts = require( 'highcharts' );
var formatUSD = require( 'format-usd' );
var unFormatUSD = require( 'unformat-usd' );

// var geolocation = require('./geolocation');
var dropdown = require( './dropdown-utils' );
var jumbo = require( 'jumbo-mortgage' );
var median = require( 'median' );
var amortize = require( 'amortize' );
var config = require( '../config/config.json' );
var fetchRates = require( './rates' );
var isNum = require( 'is-money-usd' );
var formatTime = require( './format-timestamp' );
require( './highcharts-theme' );
require( 'rangeslider.js' );
require( './tab' );
require( './placeholder-polyfill' );

// Load our handlebar templates.
var county = require( '../templates/county-option.hbs' );
var countyConfWarning = require( '../templates/county-conf-warning.hbs' );
var countyFHAWarning = require( '../templates/county-fha-warning.hbs' );
var countyVAWarning = require( '../templates/county-va-warning.hbs' );
var countyGenWarning = require( '../templates/county-general-warning.hbs' );
var sliderLabel = require( '../templates/slider-range-label.hbs' );
var creditAlert = require( '../templates/credit-alert.hbs' );
var resultAlert = require( '../templates/result-alert.hbs' );
var failAlert = require( '../templates/fail-alert.hbs' );
var dpWarning = require( '../templates/down-payment-warning.hbs' );
var chartTooltipSingle = require( '../templates/chart-tooltip-single.hbs' );
var chartTooltipMultiple = require( '../templates/chart-tooltip-multiple.hbs' );

var template = {
  county: county,
  countyConfWarning: countyConfWarning,
  countyFHAWarning: countyFHAWarning,
  countyVAWarning: countyVAWarning,
  countyGenWarning: countyGenWarning,
  sliderLabel: sliderLabel,
  creditAlert: creditAlert,
  resultAlert: resultAlert,
  failAlert: failAlert,
  dpWarning: dpWarning,
  chartTooltipSingle: chartTooltipSingle,
  chartTooltipMultiple: chartTooltipMultiple
};

var UNDEFINED;

// List all the parameters the user can change and set
// their default values.
var params = {
  'credit-score':   700,
  'down-payment':   '20,000',
  'house-price':    '200,000',
  'loan-amount':    UNDEFINED,
  'location':       'AL',
  'rate-structure': 'fixed',
  'loan-term':      30,
  'loan-type':      'conf',
  'arm-type':       '5-1',
  'edited':         false,
  'isJumbo':        false,
  'prevLoanType':   '',
  'prevLocation':   '',
  'verbotenKeys':   [ 9, 37, 38, 39, 40, 13, 16 ], // tab, arrow keys, enter, shift
  'update':         function() {
    this.prevLoanType = this['loan-type'];
    this.prevLocation = this.location;
    $.extend( params, getSelections() );
  }
};

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
    if ( this.$clear.hasClass( 'clear' ) && state !== 'error' ) {
      this.$clear.removeClass( 'clear' );
    }

    if ( state !== 'error' ) {
      this.$load.removeClass( 'loading' ).addClass( 'loaded' );
    }
  }
};

// Set some properties for the credit score slider.
var slider = {
  $el:    $( '#credit-score' ),
  min:    params['credit-score'],
  max:    params['credit-score'] + 20,
  step:   20,
  update: function() {
    var leftVal = +Number( $( '.rangeslider__handle' ).css( 'left' ).replace( 'px', '' ) );
    this.min = getSelection( 'credit-score' );
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
 * @returns {object} jQuery promise.
 */
function getData() {
  params.update();

  var promise = fetchRates( {
    price:          params['house-price'],
    loan_amount:    params['loan-amount'],
    minfico:        slider.min,
    maxfico:        slider.max,
    state:          params.location,
    rate_structure: params['rate-structure'],
    loan_term:      params['loan-term'],
    loan_type:      params['loan-type'],
    arm_type:       params['arm-type']
  } );

  promise.fail( function( request, status, errorThrown ) {
    resultFailWarning();
  } );

  return promise;
}

/**
 * Get values of all HTML elements in the control panel.
 * @returns {Object} Key-value hash of element ids and values.
 */
function getSelections() {

  var selections = {};
  var ids = [];

  for ( var param in params ) {
    selections[param] = getSelection( param );
  }

  return selections;

}

/**
 * Get value(s) of an individual HTML element in the control panel.
 * @param   {string} param Name of parameter to get. Usually the HTML element's id attribute.
 * @returns {Object} Hash of element id and its value(s).
 */
function getSelection( param ) {

  var $el = $( '#' + param );
  var val;

  switch ( param ) {
    case 'location':
    case 'rate-structure':
    case 'loan-term':
    case 'loan-type':
    case 'arm-type':
      val = $el.val();
      break;
    default:
      val = unFormatUSD( $el.val() || $el.attr( 'placeholder' ) );
  }

  return val;

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
  var val = opts.value || params[param];

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
  var loan = unFormatUSD( params['house-price'] ) - unFormatUSD( params['down-payment'] );
  if ( loan > 0 ) {
    params['loan-amount'] = loan;
  } else {
    params['loan-amount'] = 0;
  }
  $( '#loan-amount-result' ).text( formatUSD( params['loan-amount'], { decimalPlaces: 0 } ) );
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
  if ( +Number( params['loan-amount'] ) === 0 ) {
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
        data.intLabels.push( Number( key ) );
        data.labels.push( key + '%' );

        data.vals.push( val );
        if ( val > data.largest.val ) {
          data.largest.val = val;
          data.largest.label = key + '%';
        }

        for ( var i = 0; i < val; i++ ) {
          data.totalVals.push( Number( key ) );
        }
      } );

      // fade out chart and highlight county if no county is selected
      if ( $( '#county' ).is( ':visible' ) && $( '#county' ).val() === null ) {
        chart.startLoading();
        dropdown( 'county' ).showHighlight();
        $( '#hb-warning' ).addClass( 'hidden' );
        return;
      }

      // display an error message if less than 2 results are returned
      if ( data.vals.length < 2 ) {
        resultWarning();
        return;
      }

      // display an error message if the downpayment is greater than the house price
      if ( +Number( params['house-price'] ) < +Number( params['down-payment'] ) ) {
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
      } catch ( evt ) {
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
    var termVal = getSelection( 'loan-term' );
    $( '.rc-comparison-long .loan-years' ).text( termVal ).fadeIn();
    // change from 5 years to x if an ARM
    if ( getSelection( 'rate-structure' ) === 'arm' ) {
      var armVal = getSelection( 'arm-type' );
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
    state: params.location
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
    if ( !params.location ) { // eslint-disable-line no-negated-condition
      dropdown( 'location' ).showHighlight();
    } else {
      // Empty the current counties and cache the current state so we
      // can monitor if it changes.
      $( '#county' ).html( '' ).data( 'state', params.location );

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
  var jumbos = [ 'jumbo', 'agency', 'fha-hb', 'va-hb' ];
  var norms = [ 'conf', 'fha', 'va' ];
  var warnings = {
    conf: template.countyConfWarning,
    fha:  template.countyFHAWarning,
    va:   template.countyVAWarning
  };
  var bounces = { 'fha-hb': 'fha', 'va-hb': 'va' };
  var request;

  loan = jumbo( {
    loanType:   params['loan-type'],
    loanAmount: params['loan-amount']
  } );
  dropdown( 'loan-type' ).enable( norms );
  dropdown( 'loan-type' ).hideHighlight();
  $( '#county-warning' ).addClass( 'hidden' );

  // if loan is not a jumbo, hide the loan type warning
  if ( $.inArray( params['loan-type'], jumbos ) < 0 ) {
    $( '#hb-warning' ).addClass( 'hidden' );
    dropdown( 'loan-type' ).hideHighlight();
  }

  // If county is not needed and loan-type is a HB loan, bounce it to a regular loan
  if ( !loan.needCounty && $.inArray( params['loan-type'], jumbos ) >= 0 ) {
    // Change loan-type according to the bounces object
    if ( bounces.hasOwnProperty( params.prevLoanType ) ) {
      params['loan-type'] = bounces[params.prevLoanType];
      $( '#loan-type' ).val( params['loan-type'] );
    } else {
      params['loan-type'] = 'conf';
      $( '#loan-type' ).val( 'conf' );
    }
    $( '#county-warning, #hb-warning' ).addClass( 'hidden' );
    dropdown( 'loan-type' ).enable( norms );
    dropdown( 'loan-type' ).showHighlight();
  }

  // If we don't need to request a county, hide the county dropdown and jumbo options.
  if ( !loan.needCounty && $.inArray( params['loan-type'], jumbos ) < 0 ) {
    dropdown( 'county' ).hide();
    $( '#county' ).val( '' );
    dropdown( 'loan-type' ).removeOption( jumbos );
    return;
  }

  // Otherwise, make sure the county dropdown is shown.
  dropdown( 'county' ).show();

  // Hide any existing message, then show a message if appropriate.
  $( '#county-warning' ).addClass( 'hidden' );
  if ( warnings.hasOwnProperty( params['loan-type'] ) ) {
    $( '#county-warning' ).removeClass( 'hidden' ).find( 'p' ).text( warnings[params['loan-type']].call() );
  } else {
    $( '#county-warning' ).removeClass( 'hidden' ).find( 'p' ).text( template.countyGenWarning() );
  }

  // If the state hasn't changed, we also cool. No need to load new counties.
  if ( $( '#county' ).data( 'state' ) === params.location ) {
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

  // If the county field is hidden or they haven't selected a county, abort.
  if ( !$counties.is( ':visible' ) || !$counties.val() ) {
    return;
  }

  loan = jumbo( {
    loanType:       params['loan-type'],
    loanAmount:     params['loan-amount'],
    gseCountyLimit: parseInt( $county.data( 'gse' ), 10 ),
    fhaCountyLimit: parseInt( $county.data( 'fha' ), 10 ),
    vaCountyLimit:  parseInt( $county.data( 'va' ), 10 )
  } );

  if ( loan.success && loan.isJumbo ) {
    params.isJumbo = true;
    dropdown( 'loan-type' ).removeOption( jumbos );
    dropdown( 'loan-type' ).enable( norms );
    $loan.addOption( {
      label:  loanTypes[loan.type],
      value:  loan.type,
      select: true
    } );
    // If loan-type has changed as a result of the jumbo() operation,
    // make sure everything is updated.
    if ( loan.type !== params['loan-type'] ) { // eslint-disable-line no-negated-condition
      params.prevLoanType = params['loan-type'];
      params['loan-type'] = loan.type;
      dropdown( 'loan-type' ).disable( params.prevLoanType ).showHighlight();
    } else {
      dropdown( 'loan-type' ).hideHighlight();
    }
    // When the loan-type is agency or jumbo, disable conventional.
    if ( $.inArray( params['loan-type'], [ 'agency', 'jumbo' ] ) >= 0 ) {
      dropdown( 'loan-type' ).disable( 'conf' );
    }
    // Add links to loan messages.
    loan.msg = loan.msg.replace( 'jumbo (non-conforming)', '<a href="/owning-a-home/loan-options/conventional-loans/" target="_blank">jumbo (non-conforming)</a>' );
    loan.msg = loan.msg.replace( 'conforming jumbo', '<a href="/owning-a-home/loan-options/conventional-loans/" target="_blank">conforming jumbo</a>' );
    $( '#hb-warning' ).removeClass( 'hidden' ).find( 'p' ).html( loan.msg );

  } else {
    params.isJumbo = false;
    dropdown( 'loan-type' ).removeOption( jumbos );
    dropdown( 'loan-type' ).enable( norms );

    $( '#hb-warning' ).addClass( 'hidden' );
    // Select appropriate loan type if loan was kicked out of jumbo
    if ( params.prevLoanType === 'fha-hb' ) {
      $( '#loan-type' ).val( 'fha' );

    // Commented out per: https://github.com/cfpb/owning-a-home/pull/662/files#r68855207
    // } else if ( prevLoanType === 'va-hb' ) {
    // $( '#loan-type' ).val( 'va' );
    } else if ( params.prevLoanType === 'va-hb' ) {
      $( '#loan-type' ).val( 'va' );
    }

    if ( $( '#loan-type' ).val === null ) {
      $( '#loan-type' ).val( 'conf' );
    }
  }

  // Hide the county warning.
  $( '#county-warning' ).addClass( 'hidden' );
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
  params['house-price'] = getSelection( 'house-price' );
  params['down-payment'] = getSelection( 'down-payment' );
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
  if ( params['house-price'] === '0' ||
       +Number( params['house-price'] ) === 0 ) {
    removeAlerts();
    chart.stopLoading();
    downPaymentWarning();
    return true;
  } else if ( $percent.attr( 'placeholder' ) === '' ) {
    return false;
  }

  return UNDEFINED;
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
      val = getSelection( 'down-payment' ) / getSelection( 'house-price' ) * 100 || '';
      $percent.val( Math.round( val ) );
    } else {
      val = getSelection( 'house-price' ) * ( getSelection( 'percent-down' ) / 100 );
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
      fullTerm = Number( getSelection( 'loan-term' ) ) * 12;
  $( '.interest-cost' ).each( function( index ) {
    if ( $( this ).hasClass( 'interest-cost-primary' ) ) {
      rate = $( '#rate-compare-1' ).val().replace( '%', '' );
    } else {
      rate = $( '#rate-compare-2' ).val().replace( '%', '' );
    }
    var length = parseInt( $( this ).parents( '.rc-comparison-section' ).find( '.loan-years' ).text(), 10 ) * 12;
    var amortizedVal = amortize( { amount: params['loan-amount'], rate: rate, totalTerm: fullTerm, amortizeTerm: length } );
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
  $( '#arm-warning' ).addClass( 'hidden' );
  $( '.arm-info' ).addClass( 'hidden' );
  var disallowedTypes = [ 'fha', 'va', 'va-hb', 'fha-hb' ];
  var disallowedTerms = [ '15' ];

  if ( params['rate-structure'] === 'arm' ) {
    // Reset and highlight if the loan term is disallowed
    if ( disallowedTerms.indexOf( params['loan-term'] ) !== -1 ) {
      dropdown( 'loan-term' ).reset();
      dropdown( 'loan-term' ).showHighlight();
      $( '#arm-warning' ).removeClass( 'hidden' );
    }
    // Reset and highlight if the loan type is disallowed
    if ( disallowedTypes.indexOf( params['loan-type'] ) !== -1 ) {
      dropdown( 'loan-type' ).reset();
      dropdown( 'loan-type' ).showHighlight();
      $( '#arm-warning' ).removeClass( 'hidden' );
    }
    dropdown( 'loan-term' ).disable( '15' );
    dropdown( 'loan-type' ).disable( [ 'fha', 'va' ] );
    dropdown( 'arm-type' ).show();
    $( '.no-arm' ).addClass( 'hidden' );
    $( '.arm-info' ).removeClass( 'hidden' );
  } else {
    if ( params.isJumbo === false ) {
      dropdown( [ 'loan-term', 'loan-type' ] ).enable();
    }
    dropdown( 'arm-type' ).hide();
    $( '#arm-warning' ).addClass( 'hidden' );
    $( '.arm-info' ).addClass( 'hidden' );
    $( '.no-arm' ).removeClass( 'hidden' );
  }
}

/**
 * Low credit score warning display if user selects a
 * score of 620 or below
 */
function scoreWarning() {
  $( '.rangeslider__handle' ).addClass( 'warning' );
  if ( !$( '.credit-alert' ).length > 0 ) {
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
    $( '.result-alert' ).not( '.credit-alert' ).remove();
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
 * @returns {string} value - Value with commas and no dollar sign.
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
 * @returns {*} - Value of callback invocation.
 */
function renderSlider( cb ) {

  $( '#credit-score' ).rangeslider( {
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
      if ( params['credit-score'] < 620 ) {
        removeAlerts();
        scoreWarning();
      } else {
        updateView();
        removeCreditScoreAlert();
      }
    }
  } );

  if ( cb ) {
    return cb();
  }

  return UNDEFINED;

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

    Highcharts.setOptions( {
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

    new Highcharts.Chart( {
      chart: {
        renderTo: chart.$el[0],
        type: 'column',
        animation: false
      },
      plotOptions: {
        column: {
          states: {
            hover: {
              color: '#2CB34A'
            }
          }
        }
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

  return UNDEFINED; // eslint-disable-line consistent-return
}

/**
 * Initialize the rate checker app.
 * @returns {undefined}
 */
function init() {

  // Only attempt to do things if we're on the rate checker page.
  if ( $( '.rate-checker' ).length < 1 ) {
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
  if ( $( this ).val() !== params['rate-structure'] ) {
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
  $( '#hb-warning' ).addClass( 'hidden' );
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
  if ( allowedKeys.indexOf( key ) === -1 || event.shiftKey && key !== 9 ) {
    event.preventDefault();
  }
} );

// Check if input value is a number.
// If not, replace the character with an empty string.
$( '.calc-loan-amt .recalc' ).on( 'keyup', function( evt ) {
  // on keyup (not tab or arrows), immediately gray chart
  if ( params.verbotenKeys.indexOf( evt.which ) === -1 ) {
    chart.startLoading();
  }

} );

// delayed function for processing and updating
$( '.calc-loan-amt, .credit-score' ).on( 'keyup', '.recalc', function( evt ) {
  var element = this;
  // Don't recalculate on TAB or arrow keys.
  if ( params.verbotenKeys.indexOf( evt.which ) === -1 ||
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
  if ( params.edited === false ) {
    // Set the other two fields to their placeholder values.
    $( '#house-price, #percent-down, #down-payment' ).not( $( this ) )
      .each( function( i, val ) {
        $( this ).val( $( this ).attr( 'placeholder' ) );
      } );
    $( '#house-price, #percent-down, #down-payment' ).removeAttr( 'placeholder' );
    params.edited = true;
  }
} );

// Recalculate interest costs.
$( '.compare' ).on( 'change', 'select', renderInterestAmounts );

// Do it!
init();
