const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } = require( './config' );

const $ = document.querySelector.bind( document );

/**
 * Initialize a grade-level intro page
 */
function gradeLevelPage() {
  // Entry links clear session before entry
  const link = $( '.survey-entry-link' );

  link.addEventListener( 'click', () => {
    Cookie.remove( RESULT_COOKIE );
    Cookie.remove( SURVEY_COOKIE );
    sessionStorage.removeItem( ANSWERS_SESS_KEY );
  } );
}

export { gradeLevelPage };
