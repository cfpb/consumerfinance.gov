const turbolinks = require( 'turbolinks' );

const Expandable = require( '../../../js/organisms/Expandable.js' );

const expandableDom = document.querySelectorAll( '.block .o-expandable' );
let expandable;

if ( expandableDom ) {
    for ( let i = 0, len = expandableDom.length; i < len; i++ ) {
        expandable = new Expandable( expandableDom[i] );
        expandable.init();
    }
}

turbolinks.start();

if ( 'serviceWorker' in navigator ) {
  /* Delay registration until after the page has loaded, to ensure that our
     precaching requests don't degrade the first visit experience.
     See https://developers.google.com/web/fundamentals/instant-and-offline/service-worker/registration */
  window.addEventListener( 'load', () => {
    /* Your service-worker.js *must* be located at the top-level directory relative to your site.
       It won't be able to control pages unless it's located at the same level or higher than them.
       *Don't* register service worker file in, e.g., a scripts/ sub-directory!
       See https://github.com/slightlyoff/ServiceWorker/issues/468 */
    navigator.serviceWorker.register( '/eregs-service-worker.js' ).catch( err => {
      console.error( 'Error during service worker registration:', err );
    } );
  } );
}
