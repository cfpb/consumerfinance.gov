require( '../../on-demand/feedback-form' );
require( '../../on-demand/ask-autocomplete' );
const Analytics = require( '../../../modules/Analytics' );

const analyticsData = document.querySelector( '.analytics-data' );

/**
 * Send event to Google Analytics.
 */
function sendEvent() {
  const eventData = Analytics.getDataLayerOptions(
    '/es/obtener-respuestas/c/' + categorySlug + '/' + answerID + '/',
    document.title,
    'Virtual Pageview' );
  eventData.category = categoryName;
  Analytics.sendEvent( eventData );
}

if ( analyticsData ) {
  const answerID = analyticsData.getAttribute( 'data-answer-id' );
  const categorySlug = analyticsData.getAttribute( 'data-category-slug' );
  const categoryName = analyticsData.getAttribute( 'data-category-name' );

  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent();
  } else {
    Analytics.addEventListener( 'gtmLoaded', sendEvent );
  }

}
