require( '../on-demand/ask-autocomplete' );
var Analytics = require( '../../modules/Analytics' );

var Expandable = require( '../../organisms/Expandable' );
var getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;

var readMoreContainer = document.querySelector( '.o-expandable__read-more' );
if ( readMoreContainer && getBreakpointState().isBpXS ) {
  var readMoreExpandable = new Expandable( readMoreContainer ).init();
  readMoreExpandable.addEventListener( 'expandEnd', function () {
    readMoreExpandable.destroy();
    readMoreContainer.querySelector( '.o-expandable_content' ).style.height = '';
  } );
}

if ( window.answerID && window.categorySlug ) {
  function sendEvent() {
    var eventData = Analytics.getDataLayerOptions( '/askcfpb/' + window.answerID + '/',
      document.title, 'Virtual Pageview' );
    eventData.category = window.categorySlug;
    Analytics.sendEvent( eventData );
  }
  
  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent();
  } else {
    Analytics.addEventListener( 'gtmLoaded', sendEvent );
  }
}