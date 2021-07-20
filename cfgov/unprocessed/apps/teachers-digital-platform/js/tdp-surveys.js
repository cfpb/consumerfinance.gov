const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, resultsPage } = require( './survey/result-page' );
const { surveyPage } = require( './survey/survey-page' );

const $ = document.querySelector.bind( document );

const surveys = {
  init() {
    if ( $( '.tdp-survey-results' ) ) {
      return resultsPage();
    }

    if ( $( '.tdp-survey-grade-level' ) ) {
      return surveys.gradeLevelIntroPage();
    }

    const el = $( '.tdp-survey-page' );
    if ( el ) {
      return surveyPage( el );
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
};

module.exports = surveys;
