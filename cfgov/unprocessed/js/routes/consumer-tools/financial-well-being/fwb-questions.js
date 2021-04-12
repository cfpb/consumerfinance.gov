import Analytics from '../../../modules/Analytics.js';

let questionsDom;
let radiosDom;
let submitDom;
let questionStates;

/**
 * Checks the selection status of a group of radio inputs,
 * belonging to a parent fieldset
 * @param {HTMLNode} childRadios - An array of DOM elements.
 * @returns {boolean} The status of the group of inputs
 */
function checkQuestionState( childRadios ) {
  let radioIsChecked = false;
  const radiosLength = childRadios.length;

  for ( let i = 0; i < radiosLength; i++ ) {
    if ( childRadios[i].checked ) {
      radioIsChecked = true;
    }
  }

  return radioIsChecked;
}

/**
 * Checks the status of each fieldset to determine if
 * the user has completed the form
 * @returns {boolean} The completion status of the form
 */
function checkFormCompletion() {
  let formCompleted = true;

  Object.keys( questionStates ).forEach( key => {
    if ( !questionStates[key] ) {
      formCompleted = false;
    }
  } );

  return formCompleted;
}

/**
 * Event handler to prevent clicking the submit button before
 * the form is completed
 * @param {Object} event - The event object for the click event.
 */
function handleDisabledSubmit( event ) {
  event.preventDefault();
}


/**
 * Sets the disabled state of the submit button
 */
function disableSubmit() {
  submitDom.disabled = true;
  submitDom.addEventListener( 'click', handleDisabledSubmit );
}

/**
 * Sets the enabled state of the submit button
 */
function enableSubmit() {
  submitDom.title = 'Get your score';
  submitDom.disabled = false;
  submitDom.removeEventListener( 'click', handleDisabledSubmit );
  submitDom.addEventListener( 'click', evt => handleAnalytics( evt.target ) );
}


/**
 * Updates the status of the fieldset in the data store
 * and checks if the form has been completed
 * @param {HTMLNode} input - A DOM element
 */
function handleRadio( input ) {
  if ( input.name && input.checked ) {
    questionStates[input.name] = true;
  }

  if ( checkFormCompletion() ) {
    enableSubmit();
  }
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
 * @param {HTMLNode} el - A DOM element
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
 * Event handler to watch user interaction on each input
 */
function setUpListeners() {
  [].forEach.call( radiosDom, function( el ) {
    el.addEventListener( 'click', function( event ) {
      const input = event.target;

      handleRadio( input );
      handleAnalytics( input );
    } );
  } );
}

/**
 * Initializes a data store from the initial state of each fieldset
 */
function setUpData() {
  const questionsLength = questionsDom.length;

  for ( let i = 0; i < questionsLength; i++ ) {
    const questionID = questionsDom[i].id;
    const childRadios = document.querySelectorAll(
      '#' + questionID + ' input'
    );

    questionStates[questionID] = checkQuestionState( childRadios );
  }
}

/**
 * Determines the state of the form and modifies the UI appropriately
 */
function setUpUI() {
  if ( checkFormCompletion() ) {
    // Enable submit button initially if the answers are completed
    enableSubmit();
  } else {
    // Otherwise disable submit button initially
    disableSubmit();
  }

  setUpListeners();
}

/**
 * Initialize the questionnaire
 */
function init() {
  questionsDom = document.querySelectorAll( '#quiz-form fieldset' );
  radiosDom = document.querySelectorAll( '#quiz-form [type="radio"]' );
  submitDom = document.querySelector( '#submit-quiz' );
  questionStates = {};

  setUpData();
  setUpUI();
}

export default { init };
