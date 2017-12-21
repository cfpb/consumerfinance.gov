require( '../on-demand/ask-autocomplete' );
const Analytics = require( '../../modules/Analytics' );

const Expandable = require( '../../organisms/Expandable' );
const getBreakpointState = require( '../../modules/util/breakpoint-state' ).get;
const readMoreContainer = document.querySelector( '.o-expandable__read-more' );
const analyticsData = document.querySelector( '.analytics-data' );

let answerID;
let categorySlug;
let categoryName;


if ( readMoreContainer && getBreakpointState().isBpXS ) {
  const readMoreExpandable = new Expandable( readMoreContainer ).init();
  readMoreExpandable.addEventListener( 'expandEnd', function() {
    readMoreExpandable.destroy();
    readMoreContainer.querySelector( '.o-expandable_content' ).style.height = '';
  } );
}

if ( analyticsData ) {
  answerID = analyticsData.getAttribute( 'data-answer-id' );
  categorySlug = analyticsData.getAttribute( 'data-category-slug' );
  categoryName = analyticsData.getAttribute( 'data-category-name' );

  if ( Analytics.tagManagerIsLoaded ) {
    sendEvent();
  } else {
    Analytics.addEventListener( 'gtmLoaded', sendEvent );
  }
}

function sendEvent() {
  const eventData = Analytics.getDataLayerOptions( '/askcfpb/' + answerID + '/',
    document.title, 'Virtual Pageview' );
  eventData.category = categoryName;
  Analytics.sendEvent( eventData );
}
