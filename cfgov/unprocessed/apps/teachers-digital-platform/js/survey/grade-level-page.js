const Cookie = require( 'js-cookie' );
const { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } = require( './config' );

function gradeLevelPage() {
  // Entry links clear session before entry
  const link = $( '.survey-entry-link' );

  const forgetEverything = () => {
    Cookie.remove( RESULT_COOKIE );
    Cookie.remove( SURVEY_COOKIE );
    sessionStorage.removeItem( ANSWERS_SESS_KEY );
  };

  link.addEventListener( 'click', forgetEverything );
  link.addEventListener( 'mouseover', forgetEverything );
}

export { gradeLevelPage };
