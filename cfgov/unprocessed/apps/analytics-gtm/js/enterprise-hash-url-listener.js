import { track } from './util/analytics-util';

const HashURLListener = ( function() {
  let action = window.location.pathname +
               window.location.search +
               window.location.hash;
  action = action.replace( '#', 'GA_HASHTAG' );
  const label = document.title;

  track( 'Virtual Pageview', action, label );
} )();
