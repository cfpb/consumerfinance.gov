require( '../on-demand/ask-autocomplete' );
const Analytics = require( '../../modules/Analytics' );

const Expandable = require( '../../organisms/Expandable' );
const getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;

const readMoreContainer = document.querySelector( '.o-expandable__read-more' );
if ( readMoreContainer && getBreakpointState().isBpXS ) {
  const readMoreExpandable = new Expandable( readMoreContainer ).init();
  readMoreExpandable.addEventListener( 'expandEnd', function() {
    readMoreExpandable.destroy();
    readMoreContainer.querySelector( '.o-expandable_content' ).style.height = '';
  } );
}

const analyticsData = document.querySelector( '.analytics-data' );
if ( analyticsData ) {
  const answerID = analyticsData.getAttribute( 'data-answer-id' );
  const categorySlug = analyticsData.getAttribute( 'data-category-slug' );
  const categoryName = analyticsData.getAttribute( 'data-category-name' );

  function sendEvent() {
    const eventData = Analytics.getDataLayerOptions( '/askcfpb/' + answerID + '/',
      document.title, 'Virtual Pageview' );
    eventData.category = categoryName;
    Analytics.sendEvent( eventData );
  }

  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent();
  } else {
    Analytics.addEventListener( 'gtmLoaded', sendEvent );
  }
}
