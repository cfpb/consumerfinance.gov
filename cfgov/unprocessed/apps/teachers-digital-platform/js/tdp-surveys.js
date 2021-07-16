const Cookie = require( 'js-cookie' );
const encodeName = require( './encode-name' );
const ChoiceField = require( './survey/ChoiceField' );
const modals = require( './modals' );
const initials = require( './survey/initials' );

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
    modals.init();
    sessionStorage.removeItem( ANSWERS_SESS_KEY );
    Cookie.remove( 'wizard_survey_wizard' );
    initials.init();

    document.addEventListener( 'input', event => {
      const t = event.target;
      if (t.hasAttribute( 'data-initials-setter' )) {
        const fixed = String( t.value ).toUpperCase().trim().substr( 0, 3 );

        initials.update( fixed );

        // Set value on all setters!
        const allSetters = document.querySelectorAll('[data-initials-setter]');
        [].forEach.call(allSetters, input => input.value = fixed);

        t.value = fixed;

        // Show shared URL
        const shareUrlOutput = $( '.shared-url' );
        const a = document.createElement( 'a' );
        a.href = '../view/?r=' + encodeURIComponent(
          shareUrlOutput.dataset.rparam
        );
        // href property read gives you full URL
        const shareUrl = a.href;
        shareUrlOutput.value = encodeName.encodeNameInUrl(
          shareUrl, initials.get()
        );
        $( '.share-output' ).hidden = false;
      }
    } );

    document.addEventListener( 'click', event => {
      const t = event.target;
      const id = t.dataset.closePrint;
      if ( id ) {
        event.stopPropagation();
        modals.close( id );
        window.print();
      }
    } );

    const startOver = $( '.results-start-over' );
    if (startOver) {
      startOver.addEventListener( 'click', () => {
        Cookie.remove( 'resultUrl' );
      } );
    }
  }
};

module.exports = surveys;
