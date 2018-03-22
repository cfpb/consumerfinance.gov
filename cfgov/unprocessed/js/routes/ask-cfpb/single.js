require( '../../modules/util/add-email-popup' );
require( '../on-demand/ask-autocomplete' );
require( '../on-demand/read-more' );
const Analytics = require( '../../modules/Analytics' );

const analyticsData = document.querySelector( '.analytics-data' );

let answerID;
let categoryName;

if ( analyticsData ) {
  answerID = analyticsData.getAttribute( 'data-answer-id' );
  categoryName = analyticsData.getAttribute( 'data-category-name' );

  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent();
  } else {
    Analytics.addEventListener( 'gtmLoaded', sendEvent );
  }
}

function sendEvent() {
  const eventData = Analytics.getDataLayerOptions(
    '/askcfpb/' + answerID + '/', document.title, 'Virtual Pageview'
  );
  eventData.category = categoryName;
  Analytics.sendEvent( eventData );
}
