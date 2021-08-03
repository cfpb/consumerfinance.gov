const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } = require( './config' );
const ChoiceField = require( './ChoiceField' );
const ProgressBar = require( './ProgressBar' );

const $ = document.querySelector.bind( document );

let progressBar;

/**
 * @param {HTMLDivElement} el Element with survey data
 */
function surveyPage( el ) {
  if ( userTriedReentry() ) {
    return;
  }

  /**
   * @typedef {Object} SurveyData
   * @property {number} pageIdx
   * @property {number[]} questionsByPage
   * @property {number} numAnswered
   */

  /**
   * Store data- attributes from python
   *
   * @type {SurveyData}
   */
  const data = Object.create( null );
  Object.entries( el.dataset ).forEach( ( [ k, v ] ) => {
    data[k] = JSON.parse( v );
  } );

  // Init radios and re-select any that were saved in session storage but
  // which python doesn't know about.
  ChoiceField.init();
  const store = ChoiceField.restoreFromSession( ANSWERS_SESS_KEY );
  data.numAnswered = Object.keys( store ).length;

  if ( userSkippedAhead( data ) ) {
    return;
  }

  const totalQuestions = data.questionsByPage.reduce(
    ( prev, curr ) => prev + curr,
    0
  );
  initProgressListener();
  progressBar = new ProgressBar( totalQuestions, data.numAnswered );

  handleNewSelections( data, store );

  allowStartOver();
}

/**
 *
 * @param {SurveyData} data Survey data
 * @returns {boolean} True if execution should halt.
 */
function userSkippedAhead( data ) {
  /**
   * Figure out if the user has answered enough questions in total
   * to be on this page without skipping.
   */
  let questionsOnEarlierPages = 0;
  for ( let i = 0; i < data.pageIdx; i++ ) {
    questionsOnEarlierPages += data.questionsByPage[i];
  }

  if ( data.numAnswered < questionsOnEarlierPages ) {
    // User skipped a page, send them to first page
    location.href = '../p1/';
    return true;
  }

  return false;
}

/**
 * Make sure new selections are recorded in sessionStorage and that the
 * numAnswered data is updated for progress updates.
 *
 * @param {SurveyData} data
 * @param {Record<string, any>} store
 */
function handleNewSelections( data, store ) {
  const onStoreUpdate = () => {
    data.numAnswered = Object.keys( store ).length;
    if ( progressBar ) {
      progressBar.update( data.numAnswered );
    }
  };

  ChoiceField.watchAndStore( ANSWERS_SESS_KEY, store, onStoreUpdate );
}

/**
 * If the user has results, don't allow re-entry into the survey.
 *
 * @returns {boolean} True if execution should halt
 */
function userTriedReentry() {
  if ( Cookie.get( RESULT_COOKIE ) ) {
    // Has not cleared results.
    location.href = '../../results/';
    return true;
  }

  return false;
}

/**
 * Allow the user to start a survey over with reset data.
 */
function allowStartOver() {
  const a = document.querySelector( 'a.survey-start-over' );
  if ( a ) {
    a.addEventListener( 'click', e => {
      if ( window.confirm( 'Are you sure?' ) ) {
        sessionStorage.removeItem( ANSWERS_SESS_KEY );
        Cookie.remove( SURVEY_COOKIE );
      } else {
        e.preventDefault();
      }
    } );
  }
}

/**
 * Keep UI in sync with ProgressBar updates
 */
function initProgressListener() {
  document.addEventListener( ProgressBar.UPDATE_EVT, event => {
    /**
     * @type {ProgressBar}
     */
    const pb = event.detail.progressBar;
    const barEl = $( '.tdp-survey-progress-bar--bar' );
    if ( barEl ) {
      const perc = `${ pb.getPercentage() }%`;
      barEl.style.width = perc;
      barEl.parentElement.setAttribute( 'aria-label', `${ perc } complete` );
    }
    const outOfEl = $( '.tdp-survey-progress-out-of' );
    if ( outOfEl ) {
      outOfEl.textContent = `${ pb.numDone } out of ${ pb.totalNum }`;
    }
  } );
}

export { surveyPage };
