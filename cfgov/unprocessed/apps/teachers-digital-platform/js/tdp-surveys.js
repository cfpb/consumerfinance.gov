const { gradeLevelPage } = require( './survey/grade-level-page' );
const { resultsPage } = require( './survey/result-page' );
const { surveyPage } = require( './survey/survey-page' );

const $ = document.querySelector.bind( document );

const surveys = {
  init() {
    if ( $( '[data-tdp-page="results"]' ) ) {
      resultsPage();
      return;
    }

    if ( $( '[data-tdp-page="grade-level"]' ) ) {
      gradeLevelPage();
      return;
    }

    if ( $( '[data-tdp-page="survey"]' ) ) {
      surveyPage();
    }
  }
};

module.exports = surveys;
