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

var analyticsData = document.querySelector( '.analytics-data' );
if ( analyticsData ) {
  var answerID = analyticsData.getAttribute( 'data-answer-id' );
  var categorySlug = analyticsData.getAttribute( 'data-category-slug' );

  function sendEvent() {
    var eventData = Analytics.getDataLayerOptions( '/askcfpb/' + answerID + '/',
      document.title, 'Virtual Pageview' );
    eventData.category = categorySlug;
    Analytics.sendEvent( eventData );
  }
  
  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent();
  } else {
    Analytics.addEventListener( 'gtmLoaded', sendEvent );
  }
}