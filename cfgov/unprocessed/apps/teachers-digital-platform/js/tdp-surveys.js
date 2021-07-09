const Cookie = require( 'js-cookie' );
const encodeName = require( './encode-name' );
const ChoiceField = require( './survey/ChoiceField' );

const $ = document.querySelector.bind( document );
const ANSWERS_SESS_KEY = 'tdp-survey-choices';

const surveys = {
  init() {
    if ( $( '.tdp-survey-results' ) ) {
      return surveys.resultsPage();
    }

    if ( $( '.tdp-survey-grade-level' ) ) {
      return surveys.gradeLevelIntroPage();
    }

    const el = $( '.tdp-survey-page' );
    if ( el ) {
      return surveys.surveyPage( el );
    }

    return null;
  },

  gradeLevelIntroPage() {
    // Entry links clear session before entry
    const link = $( '.survey-entry-link' );

    const forgetEverything = () => {
      Cookie.remove( 'resultUrl' );
      Cookie.remove( 'wizard_survey_wizard' );
      sessionStorage.removeItem( ANSWERS_SESS_KEY );
    };

    link.addEventListener( 'click', forgetEverything );
    link.addEventListener( 'mouseover', forgetEverything );
  },

  surveyPage( el ) {
    if ( Cookie.get( 'resultUrl' ) ) {
      // Has not cleared results.
      location.href = '../../results/';
      return;
    }

    /**
     * @typedef {Object} SurveyData
     * @property {number} pageIdx
     * @property {number[]} questionsByPage
     * @property {number} numAnswered
     */

    /**
     * @type {SurveyData}
     */
    const data = Object.create( null );

    // Data from python
    Object.entries( el.dataset ).forEach( ( [ k, v ] ) => {
      data[k] = JSON.parse( v );
    } );

    ChoiceField.init();
    const store = ChoiceField.restoreFromSession( ANSWERS_SESS_KEY );
    data.numAnswered = Object.keys( store ).length;

    let expectedDone = 0;
    for ( let i = 0; i < data.pageIdx; i++ ) {
      expectedDone += data.questionsByPage[i];
    }
    if ( data.numAnswered < expectedDone ) {
      // User skipped a page, send them to first page
      location.href = '../p1/';
      return;
    }

    const onStoreUpdate = () => {
      data.numAnswered = Object.keys( store ).length;
    };

    ChoiceField.watchAndStore( ANSWERS_SESS_KEY, store, onStoreUpdate );
  },

  resultsPage() {
    sessionStorage.removeItem( ANSWERS_SESS_KEY );
    Cookie.remove( 'wizard_survey_wizard' );

    const showInitials = $( '.show-initials' );
    if ( showInitials ) {
      // Show initials encoded in URL hash
      const initials = encodeName.decodeNameFromUrl( location.href );
      if ( initials ) {
        showInitials.querySelector( 'strong' ).textContent = initials;
        showInitials.hidden = false;
      }
    }

    const shareForm = $( '.share-url-form' );
    if ( shareForm ) {
      // Create share URL and show input once initials are entered
      shareForm.addEventListener( 'submit', event => {
        event.preventDefault();

        // Create URL with initials
        const initials = $( '.share-customize [name=initials]' ).value.trim();
        const output = $( '.shared-url' );
        const a = document.createElement( 'a' );
        a.href = '../view/?r=' + encodeURIComponent( output.dataset.rparam );
        // Read property gives you full URL
        const shareUrl = a.href;
        output.value = encodeName.encodeNameInUrl( shareUrl, initials );
        $( '.share-output' ).hidden = false;
      } );
    }

    const startOver = $( '.results-start-over' );
    if ( startOver ) {
      startOver.addEventListener( 'click', () => {
        Cookie.remove( 'resultUrl' );
      } );
    }
  }
};

module.exports = surveys;
