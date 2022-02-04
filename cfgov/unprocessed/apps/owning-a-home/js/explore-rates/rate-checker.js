import * as params from './params';
import * as tab from './tab';
import * as template from './template-loader';
import {
  calcLoanAmount,
  checkIfZero,
  delay,
  isKeyAllowed,
  isVisible,
  removeDollarAddCommas,
  renderAccessibleData,
  renderDatestamp,
  renderLoanAmount,
  setSelections
} from './util';
import {
  getCounties,
  getData
} from './data-loader';
import { getSelection } from './dom-values';
import { uniquePrimitives } from '../../../../js/modules/util/array-helpers';
import amortize from 'amortize';
import dropdown from '../dropdown-utils';
import formatUSD from 'format-usd';
import jumbo from 'jumbo-mortgage';
import median from 'median';
import RateCheckerChart from './RateCheckerChart';
import Slider from './Slider';
import unFormatUSD from 'unformat-usd';

// TODO: remove jquery.
import $ from 'jquery';

// References to alert HTML.
let creditAlertDom;
let dpAlertDom;

// Range slider for credit rating.
let slider;
let chart;

let timeStampDom;
let loanAmountResultDom;
let accessibleDataTableHeadDom;
let accessibleDataTableBodyDom;
let rcSummaryDom;
let rcDisclaimerDom;
let dataLoadedDomList;

let rateSelectsDom;
let rateCompare1Dom;
let rateCompare2Dom;

/**
 * Calculate and render the loan amount.
 */
function renderLoanAmountResult() {
  const loanAmount = calcLoanAmount(
    params.getVal( 'house-price' ),
    params.getVal( 'down-payment' )
  );
  params.setVal( 'loan-amount', loanAmount );
  renderLoanAmount( loanAmountResultDom, loanAmount );
}

/**
 * Render all applicable rate checker areas.
 */
function updateView() {
  removeAlerts();
  startLoading();

  // reset view
  dropdown( [ 'county', 'loan-term' ] ).hideHighlight();

  // Check ARM
  checkARM();

  const data = {
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

  let request = params.getVal( 'request' );

  // Abort the previous request.
  if ( request && typeof request.cancel === 'function' ) {
    request.cancel( 'Aborting request for a new request.' );
  }

  // And start a new one.
  if ( +Number( params.getVal( 'loan-amount' ) ) === 0 ) {
    resultWarning();
    downPaymentWarning();
  } else {

    params.update();
    const fieldsToFetch = {
      price:          params.getVal( 'house-price' ),
      loan_amount:    params.getVal( 'loan-amount' ),
      minfico:        slider.valMin(),
      maxfico:        slider.valMax(),
      state:          params.getVal( 'location' ),
      rate_structure: params.getVal( 'rate-structure' ),
      loan_term:      params.getVal( 'loan-term' ),
      loan_type:      params.getVal( 'loan-type' ),
      arm_type:       params.getVal( 'arm-type' )
    };

    request = getData( fieldsToFetch );
    params.setVal( 'request', request );

    // Handle errors
    request.promise.catch( () => {
      resultFailWarning();
    } );

    // If it succeeds, update the DOM.
    request.promise.then( rawResults => {
      const results = rawResults.data.data;

      // sort results by interest rate, ascending
      const sortedKeys = [];
      const sortedResults = {};
      let key;
      for ( key in results ) {
        if ( results.hasOwnProperty( key ) ) {
          sortedKeys.push( key );
        }
      }

      sortedKeys.sort();

      const len = sortedKeys.length;
      for ( let x = 0; x < len; x++ ) {
        sortedResults[sortedKeys[x]] = results[sortedKeys[x]];
      }

      $.each( sortedResults, function( key, val ) {
        data.intLabels.push( Number( key ) );
        data.labels.push( key + '%' );

        data.vals.push( val );
        if ( val > data.largest.val ) {
          data.largest.val = val;
          data.largest.label = key + '%';
        }

        for ( let i = 0; i < val; i++ ) {
          data.totalVals.push( Number( key ) );
        }
      } );

      // fade out chart and highlight county if no county is selected
      if ( $( '#county' ).is( ':visible' ) && $( '#county' ).val() === null ) {
        removeAlerts();
        startLoading();
        dropdown( 'county' ).showHighlight();
        document.querySelector( '#hb-warning' ).classList.add( 'u-hidden' );
        return;
      }

      // display an error message if less than 2 results are returned
      if ( data.vals.length < 2 ) {
        resultWarning();
        return;
      }

      // display an error message if the downpayment is greater than the house price
      if ( +Number( params.getVal( 'house-price' ) ) <
           +Number( params.getVal( 'down-payment' ) ) ) {
        resultWarning();
        downPaymentWarning();
        return;
      }

      data.uniqueLabels = uniquePrimitives( data.labels.slice( 0 ) );

      finishLoading();
      hideSummary();
      removeAlerts();
      updateLanguage( data.totalVals );
      renderAccessibleData(
        accessibleDataTableHeadDom, accessibleDataTableBodyDom,
        data.labels, data.vals
      );
      chart.render( data );

      // Update timestamp
      let _timestamp = rawResults.data.timestamp;

      try {
        /* Safari 8 seems to have a bug with date conversion:
           The following: new Date("2015-01-07T05:00:00Z")
           Incorrectly returns: Tue Jan 06 2015 21:00:00 GMT-0800 (PST)
           The following will detect it and will offset the timezone enough
           to get the correct date (but not time) */
        if ( new Date( results.timestamp ).getDate() !== parseInt( results.timestamp.split( 'T' )[0].split( '-' )[2], 10 ) ) {
          _timestamp = _timestamp.split( 'T' )[0] + 'T15:00:00Z';
        }
      } catch ( err ) {
        // An error occurred.
      }

      renderDatestamp( timeStampDom, _timestamp );

      updateComparisons( data );
      renderInterestAmounts();
    } );
  }
}

/**
 * Updates the sentence above the chart.
 * @param {Array} totalVals - List of interest rates.
 */
function updateLanguage( totalVals ) {

  /**
   * Set the state text in the sentence above the chart to be the same as
   * the state drop-down selected.
   */
  function renderLocation() {
    const stateDropDown = document.querySelector( '#location' );
    const selectedDropDown = stateDropDown.options[stateDropDown.selectedIndex];
    const state = selectedDropDown.textContent;
    const locations = document.querySelectorAll( '.location' );
    // forEach could be used here, but it's not supported in IE11.
    for ( let i = 0, len = locations.length; i < len; i++ ) {
      locations[i].innerText = state;
    }
  }

  /**
   * Set the loan length text in the summary below the chart.
   */
  function updateTerm() {
    const termVal = getSelection( 'loan-term' );
    $( '.rc-comparison-long .loan-years' ).text( termVal ).fadeIn();
    // Change from 5 years to x if an ARM.
    if ( getSelection( 'rate-structure' ) === 'arm' ) {
      const armVal = getSelection( 'arm-type' );
      const term = armVal.match( /[^-]*/i )[0];
      $( '.rc-comparison-short .loan-years, .arm-comparison-term' ).text( term ).fadeIn();
    } else {
      $( '.rc-comparison-short .loan-years' ).text( 5 ).fadeIn();
    }
  }

  renderLocation();
  renderMedian( totalVals );
  updateTerm();
}

/**
 * Render the median percentage.
 * @param {Array} totalVals - List of interest rates.
 */
function renderMedian( totalVals ) {
  const loansMedian = median( totalVals ).toFixed( 3 );
  const medianRate = document.querySelector( '#median-rate' );
  medianRate.innerText = loansMedian + '%';
}

/**
 * Request a list of counties and bring them into the DOM.
 */
function loadCounties() {

  // And request 'em.
  const request = getCounties( params.getVal( 'location' ) );
  request.promise.then( resp => {

    if ( params.getVal( 'location' ) ) {
      /* Empty the current counties and cache the current state so we
         can monitor if it changes. */
      $( '#county' ).html( '' ).data( 'state', params.getVal( 'location' ) );

      // Inject each county into the DOM.
      const parseCountyData = resp.data.data;
      $.each( parseCountyData, function( i, countyData ) {
        if ( countyData.county ) {
          countyData.county = countyData.county.replace( ' County', '' );
        }
        const countyOption = template.county( countyData );
        $( '#county' ).append( countyOption );
      } );

      // Alphabetize counties
      const countyOptions = $( '#county option' );
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
      const countyDropDownDom = document.querySelector( '#county' );
      countyDropDownDom.selectedIndex = -1;
    } else {
      // If they haven't yet selected a state highlight the field.
      dropdown( 'location' ).showHighlight();
    }
  } );

  // Hide loading animation regardless of whether or not we're successful.
  dropdown( 'county' ).hideLoadingAnimation();
}

/**
 * Check the loan amount and initiate the jumbo loan interactions if need be.
 */
function checkForJumbo() {
  const jumbos = [ 'jumbo', 'agency', 'fha-hb', 'va-hb' ];
  const norms = [ 'conf', 'fha', 'va' ];
  const warnings = {
    conf: template.countyConfWarning,
    fha:  template.countyFHAWarning,
    va:   template.countyVAWarning
  };
  const bounces = { 'fha-hb': 'fha', 'va-hb': 'va' };

  const loan = jumbo( {
    loanType:   params.getVal( 'loan-type' ),
    loanAmount: params.getVal( 'loan-amount' )
  } );
  dropdown( 'loan-type' ).enable( norms );
  dropdown( 'loan-type' ).hideHighlight();
  document.querySelector( '#county-warning' ).classList.add( 'u-hidden' );

  // if loan is not a jumbo, hide the loan type warning
  if ( $.inArray( params.getVal( 'loan-type' ), jumbos ) < 0 ) {
    document.querySelector( '#hb-warning' ).classList.add( 'u-hidden' );
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
  document.querySelector( '#county-warning' ).classList.add( 'u-hidden' );
  if ( warnings.hasOwnProperty( params.getVal( 'loan-type' ) ) ) {
    $( '#county-warning' ).removeClass( 'u-hidden' ).find( 'span' ).text( warnings[params.getVal( 'loan-type' )] );
  } else {
    $( '#county-warning' ).removeClass( 'u-hidden' ).find( 'span' ).text( template.countyGenWarning );
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
  const $counties = $( '#county' );
  const $county = $( '#county' ).find( ':selected' );
  const $loan = dropdown( 'loan-type' );
  const norms = [ 'conf', 'fha', 'va' ];
  const jumbos = [ 'jumbo', 'agency', 'fha-hb', 'va-hb' ];
  const loanTypes = {
    'agency': 'Conforming jumbo',
    'jumbo':  'Jumbo (non-conforming)',
    'fha-hb': 'FHA high-balance',
    'va-hb':  'VA high-balance'
  };

  // If the county field is u-hidden or they haven't selected a county, abort.
  if ( !$counties.is( ':visible' ) || !$counties.val() ) {
    return;
  }

  const loan = jumbo( {
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

    /* If loan-type has changed as a result of the jumbo() operation,
       make sure everything is updated. */
    if ( loan.type === params.getVal( 'loan-type' ) ) {
      dropdown( 'loan-type' ).hideHighlight();
    } else {
      params.setVal( 'prevLoanType', params.getVal( 'loan-type' ) );
      params.setVal( 'loan-type', loan.type );
      dropdown( 'loan-type' ).disable( params.getVal( 'prevLoanType' ) ).showHighlight();
    }
    // When the loan-type is agency or jumbo, disable conventional.
    if ( $.inArray( params.getVal( 'loan-type' ), [ 'agency', 'jumbo' ] ) >= 0 ) {
      dropdown( 'loan-type' ).disable( 'conf' );
    }
    // Add links to loan messages.
    loan.msg = loan.msg.replace( 'jumbo (non-conforming)', '<a href="/owning-a-home/loan-options/conventional-loans/" target="_blank" rel="noopener noreferrer">jumbo (non-conforming)</a>' );
    loan.msg = loan.msg.replace( 'conforming jumbo', '<a href="/owning-a-home/loan-options/conventional-loans/" target="_blank" rel="noopener noreferrer">conforming jumbo</a>' );
    $( '#hb-warning' ).removeClass( 'u-hidden' ).find( 'span' ).html( loan.msg );

  } else {
    params.setVal( 'isJumbo', false );
    dropdown( 'loan-type' ).removeOption( jumbos );
    dropdown( 'loan-type' ).enable( norms );

    document.querySelector( '#hb-warning' ).classList.add( 'u-hidden' );
    const loanTypeDom = document.querySelector( '#loan-type' );
    // Select appropriate loan type if loan was kicked out of jumbo
    if ( params.getVal( 'prevLoanType' ) === 'fha-hb' ) {
      loanTypeDom.value = 'fha';
    } else if ( params.getVal( 'prevLoanType' ) === 'va-hb' ) {
      loanTypeDom.value = 'va';
    }

    if ( loanTypeDom.value === null ) {
      loanTypeDom.value = 'conf';
    }
  }

  // Hide the county warning.
  document.querySelector( '#county-warning' ).classList.add( 'u-hidden' );
}

/**
 * Store the loan amount and down payment, process the county data,
 * check if it's a jumbo loan.
 * @param {HTMLNode} element - TODO: Add description.
 */
function processLoanAmount( element ) {
  const name = element.getAttribute( 'name' );

  /* Save the dp-constant value when the user interacts with
     down payment or down payment percentages. */
  if ( name === 'down-payment' || name === 'percent-down' ) {
    params.setVal( 'dp-constant', name );
  }

  renderDownPayment.apply( element );
  params.setVal( 'house-price', getSelection( 'house-price' ) );
  params.setVal( 'down-payment', getSelection( 'down-payment' ) );
  params.update();
  renderLoanAmountResult();
  checkForJumbo();
  processCounty();
  updateView();
}

/**
 * Update either the down payment % or $ amount
 * depending on the input they've changed.
 */
function renderDownPayment() {

  const $el = $( this );
  const price = document.querySelector( '#house-price' );
  const percent = document.querySelector( '#percent-down' );
  const down = document.querySelector( '#down-payment' );
  let val;

  if ( !$el.val() ) {
    return;
  }

  if ( checkIfZero( params.getVal( 'house-price' ) ) ) {
    removeAlerts();
    finishLoading();
    hideSummary();
    downPaymentWarning();
  }

  if ( price.value !== 0 ) {
    if ( $el.attr( 'id' ) === 'down-payment' ||
         params.getVal( 'dp-constant' ) === 'down-payment' ) {
      val = ( getSelection( 'down-payment' ) / getSelection( 'house-price' ) * 100 ) || '';
      percent.value = Math.round( val );
    } else {
      val = getSelection( 'house-price' ) * ( getSelection( 'percent-down' ) / 100 );
      val = val >= 0 ? Math.round( val ) : '';
      val = removeDollarAddCommas( val );
      down.value = val;
    }
  }
}

/**
 * Hides the rate checker summary above the chart.
 */
function hideSummary() {
  if ( rcSummaryDom.classList.contains( 'clear' ) &&
       chart.currentState !== RateCheckerChart.STATUS_ERROR ) {
    rcSummaryDom.classList.remove( 'clear' );
    rcDisclaimerDom.classList.remove( 'clear' );
  }
}

/**
 * Update the values in the dropdowns in the comparison section
 * @param {Object} data - Data object created by the updateView method.
 */
function updateComparisons( data ) {
  // Update the options in the dropdowns.
  const uniqueLabels = data.uniqueLabels;
  $( '.compare select' ).html( '' );
  $.each( uniqueLabels, function( i, rate ) {
    const option = '<option value="' + rate + '">' + rate + '</option>';
    $( '.compare select' ).append( option );
  } );
  // In the second comparison dropdown, select the last (largest) rate.
  rateCompare2Dom.value = uniqueLabels[uniqueLabels.length - 1];
}

/**
 * Calculate and display the interest rates in the comparison section.
 */
function renderInterestAmounts() {
  const shortTermVal = [];
  const longTermVal = [];
  let rate;
  const fullTerm = Number( getSelection( 'loan-term' ) ) * 12;

  const interestCostDoms = document.querySelectorAll( '.interest-cost' );
  const interestCostList = Array.prototype.slice.call( interestCostDoms );

  interestCostList.forEach( item => {

    if ( item.classList.contains( 'interest-cost-primary' ) ) {
      rate = rateCompare1Dom.value.replace( '%', '' );
    } else {
      rate = rateCompare2Dom.value.replace( '%', '' );
    }

    const length = parseInt( $( item ).parents( '.rc-comparison-section' ).find( '.loan-years' ).text(), 10 ) * 12;
    const amortizedVal = amortize( {
      amount: params.getVal( 'loan-amount' ),
      rate: rate,
      totalTerm: fullTerm,
      amortizeTerm: length
    } );
    const totalInterest = amortizedVal.interest;
    const roundedInterest = Math.round( unFormatUSD( totalInterest ) );
    const $el = $( item ).find( '.new-cost' );
    $el.text( formatUSD( { amount: roundedInterest, decimalPlaces: 0 } ) );
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
  const id = '#rc-comparison-summary-' + term;

  const sortedRates = intVals.sort( function( a, b ) {
    return a.rate - b.rate;
  } );

  const rawDiff = sortedRates[sortedRates.length - 1].interest -
                  sortedRates[0].interest;
  const diff = formatUSD( { amount: rawDiff, decimalPlaces: 0 } );
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
  document.querySelector( '#arm-warning' ).classList.add( 'u-hidden' );
  $( '.arm-info' ).addClass( 'u-hidden' );
  const disallowedTypes = [ 'fha', 'va', 'va-hb', 'fha-hb' ];
  const disallowedTerms = [ '15' ];

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
    document.querySelector( '#arm-warning' ).classList.add( 'u-hidden' );
    $( '.arm-info' ).addClass( 'u-hidden' );
    $( '.no-arm' ).removeClass( 'u-hidden' );
  }
}

/**
 * Low credit score warning displayed if the user selects a
 * score of 620 or below.
 */
function scoreWarning() {
  slider.setState( Slider.STATUS_WARNING );
  creditAlertDom.classList.remove( 'u-hidden' );
  resultWarning();
}

/**
 * Overlays a warning/error message on the chart.
 */
function resultWarning() {
  chart.finishLoading( RateCheckerChart.STATUS_WARNING );
}

/**
 * Show alert that data call to the API failed.
 */
function resultFailWarning() {
  chart.finishLoading( RateCheckerChart.STATUS_ERROR );
}

/**
 * Show alert that down payment is greater than house price.
 */
function downPaymentWarning() {
  dpAlertDom.classList.remove( 'u-hidden' );
}

/**
 * Hide all alert messages that are showing.
 */
function removeAlerts() {
  if ( isVisible( dpAlertDom ) ) {
    chart.setStatus( RateCheckerChart.STATUS_OKAY );
    dpAlertDom.classList.add( 'u-hidden' );
    removeCreditScoreAlert();
  }
}

/**
 * Hide the credit score alert message.
 */
function removeCreditScoreAlert() {
  if ( params.getVal( 'credit-score' ) >= 620 ) {
    slider.setState( Slider.STATUS_OKAY );
    creditAlertDom.classList.add( 'u-hidden' );
  }
}

/**
 * Event handler for when slider is released.
 */
function onSlideEndHandler() {
  params.update();
  if ( params.getVal( 'credit-score' ) < 620 ) {
    removeAlerts();
    scoreWarning();
  } else {
    updateView();
    removeCreditScoreAlert();
  }
}

/**
 * Initialize the rate checker app.
 * @returns {undefined}
 */
function init() {
  // Only attempt to do things if we're on the rate checker page.
  if ( document.querySelectorAll( '.rate-checker' ).length === 0 ) {
    return false;
  }

  creditAlertDom = document.querySelector( '#credit-score-alert' );
  dpAlertDom = document.querySelector( '#dp-alert' );

  rateSelectsDom = document.querySelector( '#rate-selects' );
  rateCompare1Dom = document.querySelector( '#rate-compare-1' );
  rateCompare2Dom = document.querySelector( '#rate-compare-2' );

  dataLoadedDomList = document.querySelectorAll( '#rate-results .data-enabled' );

  const sliderDom = document.querySelector( '#credit-score-range' );
  const creditScore = params.getVal( 'credit-score' );
  slider = new Slider( sliderDom );
  slider.init(
    {
      min: 600,
      max: 850,
      value: creditScore,
      // callbacks
      onSlideEnd: onSlideEndHandler
    }
  );

  chart = new RateCheckerChart();
  chart.init();

  // Record timestamp HTML element that's updated from date from API.
  timeStampDom = document.querySelector( '#timestamp' );

  loanAmountResultDom = document.querySelector( '#loan-amount-result' );

  const accessibleDataDom = document.querySelector( '#accessible-data' );
  accessibleDataTableHeadDom = accessibleDataDom.querySelector( '.table-head' );
  accessibleDataTableBodyDom = accessibleDataDom.querySelector( '.table-body' );

  rcSummaryDom = document.querySelector( '#rc-summary' );
  rcDisclaimerDom = document.querySelector( '#timestamp-p' );

  chart.render();
  renderLoanAmountResult();
  setSelections( params.getAllParams() );
  registerEvents();
  tab.init();

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
  return true;
}

/**
 * Add loading CSS class to all items with data-loaded class.
 */
function startLoading() {
  chart.startLoading();
  let item;
  for ( let i = 0, len = dataLoadedDomList.length; i < len; i++ ) {
    item = dataLoadedDomList[i];
    item.classList.add( 'loading' );
    item.classList.remove( 'loaded' );
  }
}

/**
 * Add loaded CSS class to all items with data-loaded class.
 */
function finishLoading() {
  chart.finishLoading();
  if ( chart.currentState !== RateCheckerChart.STATUS_ERROR ) {
    let item;
    for ( let i = 0, len = dataLoadedDomList.length; i < len; i++ ) {
      item = dataLoadedDomList[i];
      item.classList.remove( 'loading' );
      item.classList.add( 'loaded' );
    }
  }
}

/**
 * Register event handlers.
 */
function registerEvents() {
  // ARM highlighting handler.
  const rateStructureDom = document.querySelector( '#rate-structure' );
  rateStructureDom.addEventListener( 'change', event => {
    if ( event.target.value !== params.getVal( 'rate-structure' ) ) {
      dropdown( 'arm-type' ).showHighlight();
    }
  } );

  const armTypeDom = document.querySelector( '#arm-type' );
  armTypeDom.addEventListener( 'change', () => {
    dropdown( 'arm-type' ).hideHighlight();
  } );

  // Recalculate everything when drop-down menus are changed.
  $( '.demographics, .calc-loan-details, .county' ).on( 'change', '.recalc', function() {
    /* If the loan-type is conf, and there's a county visible,
       then we just exited a HB situation.
       Clear the county before proceeding. */
    document.querySelector( '#hb-warning' ).classList.add( 'u-hidden' );
    // If the state field changed, wipe out county.
    if ( $( this ).attr( 'id' ) === 'location' ) {
      $( '#county' ).html( '' );
      // dropdown('county').hide();
    }
    processLoanAmount( this );
  } );

  // Prevent non-numeric characters from being entered.
  $( '.calc-loan-amt .recalc' ).on( 'keydown', function( event ) {
    const key = event.which;
    const allowedKeys = [
      8, 9, 37, 38, 39, 40, 48, 49,
      50, 51, 52, 53, 54, 55, 56, 57,
      96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 188, 190
    ];

    /* If it's not an allowed key OR the shift key is held down
       (and they're not tabbing) stop everything. */
    if ( allowedKeys.indexOf( key ) === -1 ||
         ( event.shiftKey && key !== 9 ) ) {
      event.preventDefault();
    }
  } );

  /* Check if input value is a number.
     If not, replace the character with an empty string. */
  $( '.calc-loan-amt .recalc' ).on( 'keyup', function( event ) {
    const key = event.which;
    // on keyup (not tab or arrows), immediately gray chart
    if ( isKeyAllowed( key ) ) {
      removeAlerts();
      startLoading();
    }

  } );

  // Delayed function for processing and updating
  const calcLoanAmountDom = document.querySelector( '#loan-amt-inputs' );
  const creditScoreDom = document.querySelector( '#credit-score-container' );

  calcLoanAmountDom.addEventListener( 'keyup', NoCalcOnForbiddenKeys );
  creditScoreDom.addEventListener( 'keyup', NoCalcOnForbiddenKeys );

  /**
   * @param  {KeyboardEvent} event Event object.
   */
  function NoCalcOnForbiddenKeys( event ) {
    const element = event.target;
    const key = event.keyCode;

    // Don't recalculate on TAB or arrow keys.
    if ( isKeyAllowed( key ) || element.classList.contains( 'a-range' ) ) {
      delay( () => processLoanAmount( element ), 500 );
    }
  }

  const housePriceDom = document.querySelector( '#house-price' );
  const downPaymentDom = document.querySelector( '#down-payment' );

  housePriceDom.addEventListener( 'focusout', priceFocusOutHandler );
  downPaymentDom.addEventListener( 'focusout', priceFocusOutHandler );

  /**
   * @param  {FocusEvent} event Event object.
   */
  function priceFocusOutHandler( event ) {
    event.target.value = removeDollarAddCommas( event.target.value );
  }


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
  rateSelectsDom.addEventListener( 'change', renderInterestAmounts );
}

export { init };
