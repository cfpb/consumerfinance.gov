/* eslint no-extra-semi: "off" */


const Analytics = require( '../../modules/Analytics' );
const Expandable = require( '../../organisms/Expandable' );

const expandableDom = document.querySelectorAll( '.content .o-expandable' );
let expandable;

if ( expandableDom ) {
  for ( let i = 0, len = expandableDom.length; i < len; i++ ) {
    expandable = new Expandable( expandableDom[i] );
    expandable.init();
  }
}

/**
 * Initialize the results interactions
 */
function init() {

  const buttonsDom = document.querySelectorAll(
    '.comparison-chart_toggle-button'
  );

  /**
   * Changes the visibility of the results by category
   * based on user input
   * @param {string} category - The category to display
   */
  function switchComparisons( category ) {
    const allCategories = document.querySelectorAll( '.comparison_data-point' );
    const showCategory = document.querySelectorAll(
      '[class^="comparison_data-point ' + category + '"]'
    );
    const selectedButton = document.querySelector(
      '[data-compare-by="' + category + '"]'
    );
    const selectedButtonClass = 'comparison-chart_toggle-button__selected';
    const hiddenClass = 'u-hidden';

    // Hide all categories ...
    [].forEach.call( allCategories, function( el ) {
      el.classList.add( hiddenClass );
    } );
    // ... and deselect all toggle buttons ...
    [].forEach.call( buttonsDom, function( el ) {
      el.classList.remove( selectedButtonClass );
    } );
    // ... so that we can show only the right category data ...
    [].forEach.call( showCategory, function( el ) {
      el.classList.remove( hiddenClass );
    } );
    // ... and then highlight the correct button.
    selectedButton.classList.add( selectedButtonClass );
  }

  /**
   * Sends the user interaction to Analytics
   * @param {string} action - A GTM data attribute
   * @param {string} label - A GTM data attribute
   * @param {string} category - A GTM data attribute
   */
  function sendEvent( action, label, category ) {
    const eventData = Analytics.getDataLayerOptions( action, label, category );
    Analytics.sendEvent( eventData );
  }

  /**
   * Grabs analytics event data from the passed element's data attributes.
   * Determines the state of the Analytics module and either passes the data
   * or waits for Analytics to report readiness, then passes the data.
   * @param {HTMLNode} el - A dom element
   */
  function handleAnalytics( el ) {
    const action = el.getAttribute( 'data-gtm-action' );
    const label = el.getAttribute( 'data-gtm-label' );
    const category = el.getAttribute( 'data-gtm-category' );

    if ( Analytics.tagManagerIsLoaded ) {
      sendEvent( action, label, category );
    } else {
      /* istanbul ignore next */
      Analytics.addEventListener( 'gtmLoaded', sendEvent );
    }
  }

  /**
   * Event handler to watch user interaction on each button
   */
  function setUpListeners() {
    [].forEach.call( buttonsDom, function( el ) {
      el.addEventListener( 'click', function( event ) {
        const input = event.target;

        switchComparisons( input.getAttribute( 'data-compare-by' ) );
        handleAnalytics( input );
      } );
    } );
  }

  /**
   * Sets up the UI for the default age category
   */
  function setUpUI() {
    switchComparisons( 'age' );
    setUpListeners();
  }

  setUpUI();
}

module.exports = { init: init };
