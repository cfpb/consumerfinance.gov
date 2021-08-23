const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } = require( './config' );
const modals = require( '../modals' );

/**
 * Initialize a grade-level intro page
 */
function gradeLevelPage() {
  // Clear session to prepare for fresh entry
  Cookie.remove( RESULT_COOKIE );
  Cookie.remove( SURVEY_COOKIE );
  sessionStorage.removeItem( ANSWERS_SESS_KEY );

  modals.init();
}

export { gradeLevelPage };
