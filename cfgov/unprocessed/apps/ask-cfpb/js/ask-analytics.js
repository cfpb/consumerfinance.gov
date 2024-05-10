/* ==========================================================================
   Scripts for Ask analytics.
   ========================================================================== */

import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

const noResults =
  document.querySelectorAll('[data-gtm_ask-no-results="true"]').length > 0;

if (noResults) {
  const search = document.getElementById('o-search-bar_query').value;
  analyticsSendEvent({
    action: 'noSearchResults',
    label: search + ':0',
    event: 'Ask Search',
  });
}
