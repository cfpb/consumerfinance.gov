const Cookie = require( 'js-cookie' );
const ChoiceField = require( './ChoiceField' );
const { ANSWERS_SESS_KEY } = require( './result-page' );

/**
 * @param {HTMLDivElement} el Element with survey data
 */
function surveyPage( el ) {
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
}

export { surveyPage };
