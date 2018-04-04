import {
  addEventListenerToElem,
  delay,
  track
} from './util/analytics-util';

const OAHRCAnalytics = ( function() {

  // credit score slider
  const rangeSliders = document.querySelectorAll( '.rangeslider' );
  let rangeSliderEl;
  for ( let i = 0, len = rangeSliders.length; i < len; i++ ) {
    rangeSliderEl = rangeSliders[i];
    addEventListenerToElem( rangeSliderEl, 'click', _rangeSliderEventHandler );
    addEventListenerToElem(
      rangeSliderEl, 'touchend', _rangeSliderEventHandler
    );
  }

  /**
   * Event handler for range slider interactions.
   */
  function _rangeSliderEventHandler() {
    const sliderRangeEl = document.querySelector( '#slider-range' );
    const score = sliderRangeEl.textContent;
    track( 'OAH Rate Tool Interactions', 'Score range', score );
  }


  // state select
  const locationEl = document.querySelector( '#location' );
  addEventListenerToElem( locationEl, 'change', function( evt ) {
    const target = evt.target;
    const value = target.value;
    track( 'OAH Rate Tool Interactions', 'Select state', value );
  } );

  // house price
  const housePriceEl = document.querySelector( '#house-price' );
  addEventListenerToElem( housePriceEl, 'keyup', function( evt ) {
    const target = evt.target;
    const value = target.value;
    delay( function() {
      track( 'OAH Rate Tool Interactions', 'House price', value );
    }, 5000 );
  } );

  // down payment percentage
  const percentDownEl = document.querySelector( '#percent-down' );
  addEventListenerToElem( percentDownEl, 'keyup', function( evt ) {
    const target = evt.target;
    const value = target.value;
    delay( function() {
      track( 'OAH Rate Tool Interactions', 'Down payment percent', value );
    }, 5000 );
  } );

  // down payment $
  const downPaymentEl = document.querySelector( '#down-payment' );
  addEventListenerToElem( downPaymentEl, 'keyup', function( evt ) {
    const target = evt.target;
    const value = target.value;
    delay( function() {
      track( 'OAH Rate Tool Interactions', 'Down payment amount', value );
    }, 5000 );
  } );

  // rate structure
  const rateStructureEl = document.querySelector( '#rate-structure' );
  addEventListenerToElem( rateStructureEl, 'change', function( evt ) {
    const target = evt.target;
    const value = target.value;
    track( 'OAH Rate Tool Interactions', 'Rate structure', value );
  } );

  // loan term
  const loanTermEl = document.querySelector( '#loan-term' );
  addEventListenerToElem( loanTermEl, 'change', function( evt ) {
    const target = evt.target;
    const value = target.value;
    track( 'OAH Rate Tool Interactions', 'Loan term', value );
  } );

  // loan type
  const loanTypeEl = document.querySelector( '#loan-type' );
  addEventListenerToElem( loanTypeEl, 'change', function( evt ) {
    const target = evt.target;
    const value = target.value;
    track( 'OAH Rate Tool Interactions', 'Loan type', value );
  } );

  // arm type
  const armTypeEl = document.querySelector( '#arm-type' );
  addEventListenerToElem( armTypeEl, 'change', function( evt ) {
    const target = evt.target;
    const value = target.value;
    track( 'OAH Rate Tool Interactions', 'ARM type', value );
  } );

  // rate comparison select #1
  const rateCompare1El = document.querySelector( '#rate-compare-1' );
  addEventListenerToElem( rateCompare1El, 'change', function( evt ) {
    const target = evt.target;
    const value = target.value;
    track( 'OAH Rate Tool Interactions', 'Interest cost 1', value );
  } );

  // rate comparison select #2
  const rateCompare2El = document.querySelector( '#rate-compare-2' );
  addEventListenerToElem( rateCompare2El, 'change', function( evt ) {
    const target = evt.target;
    const value = target.value;
    track( 'OAH Rate Tool Interactions', 'Interest cost 2', value );
  } );

  // page reload link
  const reloadLinkEl = document.querySelector( '#reload-link' );
  addEventListenerToElem( reloadLinkEl, 'click', function() {
    track( 'OAH Rate Tool Interactions', 'Revert', '/owning-a-home/rate-checker' );
  } );

  // next steps: I plan to buy in the next couple of months
  const planToBuyTabEl = document.querySelector( '#plan-to-buy-tab' );
  addEventListenerToElem( planToBuyTabEl, 'click', function() {
    track( 'OAH Rate Tool Interactions', 'Click', 'Collapsed_Tabs_Buying' );
  } );

  // next steps: I won't buy for several months
  const wontBuyTabEl = document.querySelector( '#wont-buy-tab' );
  addEventListenerToElem( wontBuyTabEl, 'click', function() {
    track( 'OAH Rate Tool Interactions', 'Click', 'Collapsed_Tabs_Not_Buying' );
  } );
} )();
