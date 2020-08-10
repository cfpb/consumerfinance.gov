/* ==========================================================================
   Scripts for Ask analytics.
   ========================================================================== */

import Analytics from '../../modules/Analytics';

const noResults = document.querySelectorAll( '[data-gtm_ask-no-results="true"]' ).length > 0;

if ( noResults ) {
  const search = document.getElementById( 'o-search-bar_query' ).value;
  const eventData = Analytics.getDataLayerOptions( 'noSearchResults', search + ':0', 'Ask Search' );
  Analytics.sendEvent( eventData );
}
