require( '../../on-demand/feedback-form' );
require( '../../on-demand/ask-autocomplete' );
var Analytics = require( '../../../modules/Analytics' );

if ( window.answerID && window.categorySlug ) {
  function sendEvent() {
    var eventData = Analytics.getDataLayerOptions( 
      '/es/obtener-respuestas/c/'+ window.categorySlug + '/' + window.answerID + '/',
      document.title, 
      'Virtual Pageview' );
    eventData.category = window.categorySlug;
    Analytics.sendEvent( eventData );
  }
  
  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent();
  } else {
    Analytics.addEventListener( 'gtmLoaded', sendEvent );
  }
}