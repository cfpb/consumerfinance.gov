require( '../../on-demand/feedback-form' );
require( '../../on-demand/ask-autocomplete' );
const Analytics = require( '../../../modules/Analytics' );

const analyticsDataEl = document.querySelector( '.analytics-data' );

/**
 * Send an event to Google Analytics.
 * @param  {string} categorySlug The URL slug.
 * @param  {string} categoryName The category name.
 * @param  {string} answerID The answer ID in the URL.
 */
function sendEvent( categorySlug, categoryName, answerID ) {
  const eventData = Analytics.getDataLayerOptions(
    '/es/obtener-respuestas/c/' + categorySlug + '/' + answerID + '/',
    document.title,
    'Virtual Pageview'
  );
  eventData.category = categoryName;
  Analytics.sendEvent( eventData );
}

if ( analyticsDataEl ) {
  const answerID = analyticsDataEl.getAttribute( 'data-answer-id' );
  const categorySlug = analyticsDataEl.getAttribute( 'data-category-slug' );
  const categoryName = analyticsDataEl.getAttribute( 'data-category-name' );

  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent( categorySlug, categoryName, answerID );
  } else {
    Analytics.addEventListener(
      'gtmLoaded',
      () => sendEvent( categorySlug, categoryName, answerID )
    );
  }
}
