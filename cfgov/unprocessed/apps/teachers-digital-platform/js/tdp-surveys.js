import { gradeLevelPage } from './survey/grade-level-page';
import { surveyPage } from './survey/survey-page';
import { resultsPage } from './survey/result-page';

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

export default surveys;
