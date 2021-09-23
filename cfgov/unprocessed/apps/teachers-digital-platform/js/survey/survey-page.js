const { closest } = require( '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js' );
const objectEntries = require( 'object.entries' );
const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } = require( './config' );
const modals = require( '../modals' );
const ChoiceField = require( './ChoiceField' );
const ProgressBar = require( './ProgressBar' );
const SectionLink = require( './SectionLink' );

const $ = document.querySelector.bind( document );
const $$ = document.querySelectorAll.bind( document );

let progressBar;

/**
 * @typedef {Object} SurveyData
 * @property {string} itemBullet
 * @property {number} numAnswered
 * @property {number} pageIdx
 * @property {number[]} questionsByPage
 */

/**
 * Initialize a survey page
 */
function surveyPage() {
  // Decorative transformations
  indentQuestionsByNumber();
  breakSeparatedAnswers();

  if ( userTriedReentry() ) {
    return;
  }

  const data = readSurveyData();
  modals.init();
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

  initErrorHandling();
  allowStartOver();
}

/**
 * @returns {SurveyData} Survey data
 */
function readSurveyData() {
  const el = $( '[data-tdp-page="survey"]' );

  /**
   * @type {SurveyData}
   */
  const data = Object.create( null );
  objectEntries( el.dataset ).forEach( ( [ k, v ] ) => {
    try {
      data[k] = JSON.parse( v );
    } catch ( err ) {
      data[k] = v;
    }
  } );
  return data;
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
    location.href = '../results/';
    return true;
  }

  return false;
}

/**
 * Allow the user to start a survey over completely.
 */
function allowStartOver() {
  document.addEventListener( 'click', event => {
    const button = closest( event.target, '#modal-restart [data-cancel]' );
    if ( button ) {
      event.preventDefault();
      if ( button.dataset.cancel ) {
        modals.close();
      } else {
        sessionStorage.removeItem( ANSWERS_SESS_KEY );
        Cookie.remove( SURVEY_COOKIE );
        location.href = $( '[data-grade-select-url]' ).dataset.gradeSelectUrl;
      }
    }
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

    // The heading is duplicated, so we must update both
    const outOfEls = $$( '.tdp-survey-progress-out-of' );

    const circle = $( '.tdp-survey-progress__circle' );
    const svg = $( '.tdp-survey-progress__svg' );
    const texts = [].slice.call( $$( '.tdp-survey-progress__svg text' ) );
    if ( !outOfEls.length || !circle || !svg || texts.length < 3 ) {
      return;
    }

    const perc = `${ pb.getPercentage() }%`;

    [].forEach.call( outOfEls, el => {
      el.innerHTML = `<b>${ pb.numDone }</b> of <b>${ pb.totalNum }</b>`;
    } );

    texts[0].textContent = perc;
    texts[1].textContent = `${ pb.numDone }/${ pb.totalNum } questions`;

    const dashOffset = 1 - ( pb.numDone / pb.totalNum );
    circle.setAttribute( 'stroke-dashoffset', dashOffset );

    svg.setAttribute( 'aria-label', `${ perc } complete` );
    svg.style.opacity = '1';
  } );
}

/**
 * Error handling for form
 */
function initErrorHandling() {
  const form = $( '.tdp-survey-page form' );
  const notification = $( '.tdp-survey-page .m-notification' );
  const ul = $( '.tdp-survey-page .m-notification_explanation' );
  if ( form && notification && ul ) {
    form.addEventListener( 'submit', submitEvt => {
      const unsets = ChoiceField.findUnsets();
      if ( !unsets.length ) {
        return;
      }

      submitEvt.preventDefault();
      ul.textContent = '';

      ChoiceField.removeErrors();
      unsets.forEach( cf => {
        cf.markError();

        const fieldset = cf.getUl().parentElement;
        const link = document.createElement( 'a' );
        link.href = '#';
        link.setAttribute('data-gtm_ignore', 'true');
        link.textContent = fieldset.querySelector( 'legend' ).textContent;
        link.addEventListener( 'click', clickEvt => {
          clickEvt.preventDefault();
          scrollToEl( fieldset );
        } );
        const li = document.createElement( 'li' );
        ul.appendChild( li );
        li.appendChild( link );
      } );

      notification.classList.add( 'm-notification__visible' );
      if ( !scrollToEl( notification ) ) {
        // Can't scroll, jump up
        location.href = '#main';
      }
    } );
  }
}

/**
 * @param {Element} el Element
 * @returns {boolean} Success?
 */
function scrollToEl( el ) {
  try {
    el.scrollIntoView( { behavior: 'smooth' } );
    return true;
  } catch ( err1 ) {
    try {
      el.scrollIntoView();
      return true;
    } catch ( err2 ) {
      return false;
    }
  }
}

/**
 * Don't allow question text to wrap underneath the number. Indent according
 * to the width of the number.
 */
function indentQuestionsByNumber() {
  /**
   * @type {HTMLElement[]}
   */
  const strongs = [].slice.call( $$( '.tdp-question-legend > strong' ) );
  strongs.forEach( strong => {
    const offset = Math.round( strong.getBoundingClientRect().width + 3 );
    const legend = strong.parentElement;
    const li = legend.parentElement;
    li.style.paddingLeft = `${ offset }px`;
    legend.style.textIndent = `-${ offset }px`;
  } );
}

/**
 * If a question option has separators, break it into multiple lines.
 *
 */
function breakSeparatedAnswers() {
  const convertToDivs = ( text, charCode ) => {
    // Convert text node into a set of div items
    const wrap = document.createElement( 'div' );
    wrap.className = 'tdp-lines';
    wrap.innerHTML = `<span>(${ String.fromCharCode( charCode ) }) </span>`;

    const ul = document.createElement( 'ul' );

    // HTML escape any chars as necessary when splitting
    const htmlItems = text.split( ' ‣ ' ).map( item => {
      ul.textContent = item;
      return ul.innerHTML;
    } );

    ul.innerHTML = '<li>' +
      htmlItems.join( '</li><li>' ) + '</li>';

    wrap.appendChild( ul );
    return wrap;
  };

  const isSeparated = str => str.indexOf( ' ‣ ' ) !== -1;
  let charCode = 97;

  /**
   * @type {HTMLLabelElement[]}
   */
  const labels = [].slice.call( $$( '.ChoiceField .a-label' ) );
  labels.forEach( label => {
    if ( closest( label, 'li:first-child' ) === label.parentElement ) {
      // Reset to "a"
      charCode = 97;
    }

    if ( !isSeparated( label.textContent ) ) {
      charCode += 1;
      return;
    }

    for ( let i = 0; i < label.childNodes.length; i++ ) {
      const node = label.childNodes[i];
      if ( node.nodeType === Node.TEXT_NODE &&
        isSeparated( node.textContent ) ) {
        node.parentNode.insertBefore(
          convertToDivs( node.textContent, charCode ),
          node
        );
        node.parentNode.removeChild( node );
      }
    }

    charCode += 1;
  } );
}

export { surveyPage };
