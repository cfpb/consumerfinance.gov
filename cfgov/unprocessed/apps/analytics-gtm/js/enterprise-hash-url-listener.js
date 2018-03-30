const HashURLListener = ( function() {
  let action = window.location.pathname + window.location.search + window.location.hash;
  action = action.replace( '#', 'GA_HASHTAG' );
  const label = document.title;

  window.dataLayer.push( {
    event: 'Virtual Pageview',
    action: action,
    label: label
  } );

} )();
