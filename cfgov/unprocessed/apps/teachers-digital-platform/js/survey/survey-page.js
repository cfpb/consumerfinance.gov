const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } = require( './config' );
const ChoiceField = require( './ChoiceField' );
const ProgressBar = require( './ProgressBar' );
const SectionLink = require( './SectionLink' );

const $ = document.querySelector.bind( document );
const $$ = document.querySelectorAll.bind( document );

let progressBar;

/**
 * Initialize a survey page
 *
 * @param {HTMLDivElement} el Element with survey data
 */
function surveyPage( el ) {
  if ( userTriedReentry() ) {
    return;
  }

  /**
   * @typedef {Object} SurveyData
   * @property {string} itemBullet
   * @property {number} numAnswered
   * @property {number} pageIdx
   * @property {number[]} questionsByPage
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

  /**
   * Init radios and re-select any that were saved in session storage but
   * which python doesn't know about.
   */
  ChoiceField.init();
  const store = ChoiceField.restoreFromSession( ANSWERS_SESS_KEY );
  data.numAnswered = Object.keys( store ).length;
  SectionLink.init( data );

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

  // Decorative transformations
  indentQuestionsByNumber();
  breakBulletedAnswers( data.itemBullet );
}

/**
 * If the user has skipped ahead, redirect and return true.
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
 * @param {SurveyData} data Survey data
 * @param {Record<string, any>} store Store of selected answers
 */
function handleNewSelections( data, store ) {
  const onStoreUpdate = () => {
    data.numAnswered = Object.keys( store ).length;
    if ( progressBar ) {
      progressBar.update( data.numAnswered );
    }
    SectionLink.update( data.numAnswered );
  };

  ChoiceField.watchAndStore( ANSWERS_SESS_KEY, store, onStoreUpdate );
}

/**
 * If the user has results, don't allow re-entry into the survey.
 * Redirect and return true.
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
  const a = $( '.survey-start-over a' );
  const note = $( '.survey-start-over .m-notification' );
  const yes = $( '.survey-start-over [data-yes]' );
  const cancel = $( '.survey-start-over [data-cancel]' );
  if ( !a || !note || !yes || !cancel ) {
    return;
  }

  a.addEventListener( 'click', event => {
    event.preventDefault();
    note.classList.add( 'm-notification__visible' );
  } );

  yes.addEventListener( 'click', event => {
    event.preventDefault();
    sessionStorage.removeItem( ANSWERS_SESS_KEY );
    Cookie.remove( SURVEY_COOKIE );
    location.href = a.href;
  } );

  cancel.addEventListener( 'click', event => {
    event.preventDefault();
    note.classList.remove( 'm-notification__visible' );
  } );
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
    const outOfEl = $( '.tdp-survey-progress-out-of' );
    const circle = $( '.tdp-survey-progress__circle' );
    const texts = [].slice.call( $$( '.tdp-survey-progress__svg text' ) );
    if ( !outOfEl || !circle || texts.length < 3 ) {
      return;
    }

    const perc = `${ pb.getPercentage() }%`;

    outOfEl.innerHTML = `<b>${ pb.numDone }</b> of <b>${ pb.totalNum }</b>`;

    texts[0].textContent = perc;
    texts[1].textContent = `${ pb.numDone }/${ pb.totalNum } questions`;

    const dashOffset = 1 - ( pb.numDone / pb.totalNum );
    circle.setAttribute( 'stroke-dashoffset', dashOffset );

    const svg = circle.parentElement;
    svg.setAttribute( 'aria-label', `${ perc } complete` );
    svg.style.opacity = '1';
  } );
}

/**
 * Don't allow question text to wrap underneath the number. Indent according
 * to the width of the number.
 */
function indentQuestionsByNumber() {
  /**
   * @type {HTMLElement[]}
   */
  const strongs = [].slice.call( $$( '.tdp-survey-page p > label > strong' ) );
  strongs.forEach( strong => {
    const offset = strong.getBoundingClientRect().width;
    const p = strong.parentElement.parentElement;
    p.style.marginLeft = `${ offset }px`;
    p.style.textIndent = `-${ offset }px`;
  } );
}

/**
 * If a question option is bulleted with ‣, break it into multiple lines.
 *
 * @param {string} bullet Bullet character
 */
function breakBulletedAnswers( bullet ) {
  const spanify = text => {
    // Convert text node into a span with <br> between items.
    const span = document.createElement( 'span' );

    // HTML escape any chars as necessary when splitting
    const htmlItems = text.split( ` ${ bullet } ` ).map( item => {
      span.textContent = item;
      return span.innerHTML;
    } );

    span.innerHTML = ` &nbsp;${ bullet } ` + htmlItems.join( `<br>&nbsp;${ bullet } ` );
    return span;
  };

  const hasTri = str => str.indexOf( ` ${ bullet } ` ) !== -1;

  /**
   * @type {HTMLLabelElement[]}
   */
  const labels = [].slice.call( $$( '.ChoiceField li label' ) );
  labels.forEach( label => {
    if ( !hasTri( label.textContent ) ) {
      return;
    }

    for ( let i = 0; i < label.childNodes.length; i++ ) {
      const node = label.childNodes[i];
      if ( node.nodeType === Node.TEXT_NODE && hasTri( node.textContent ) ) {
        node.replaceWith( spanify( node.textContent ) );
      }
    }
  } );
}

export { surveyPage };
