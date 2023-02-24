import { gradeLevelPage } from './survey/grade-level-page.js';
import { surveyPage } from './survey/survey-page.js';
import { resultsPage } from './survey/result-page.js';

const $ = document.querySelector.bind(document);

const surveys = {
  init() {
    if ($('[data-tdp-page="results"]')) {
      resultsPage();
      return;
    }

    if ($('[data-tdp-page="grade-level"]')) {
      gradeLevelPage();
      return;
    }

    if ($('[data-tdp-page="survey"]')) {
      surveyPage();
    }
  },
};

export default surveys;
