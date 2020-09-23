import { clientsClaim, skipWaiting } from 'workbox-core';
import { ExpirationPlugin } from 'workbox-expiration';
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
import { NavigationRoute, registerRoute } from 'workbox-routing';
import { createHandlerBoundToURL, precacheAndRoute } from 'workbox-precaching';
import { CacheFirst, NetworkFirst, StaleWhileRevalidate } from 'workbox-strategies';

skipWaiting();
clientsClaim();

const minutes = num => num * 60;
const days = num => minutes( num ) * 60 * 24;

// Precache compiled Webpack assets:
precacheAndRoute( self.__WB_MANIFEST );

// Precache app landing page:
precacheAndRoute( [ '/mmt-my-money-calendar', '/mmt-my-money-calendar/calendar', '/mmt-my-money-calendar/add/income' ] );

// All navigation routes hit the single-page-app landing page:
const rootHandler = createHandlerBoundToURL( '/mmt-my-money-calendar' );
const navRoute = new NavigationRoute( rootHandler, {
  allowList: [
    /mmt-my-money-calendar/
  ]
} );
registerRoute( navRoute );

/*
workbox.routing.registerNavigationRoute(workbox.precaching.getCacheKeyForURL('/mmt-my-money-calendar'), {
  whitelist: [/mmt-my-money-calendar/],
});
*/

// Cache Google fonts long term:
registerRoute(
  /^https:\/\/fonts\.google\.com/,
  new StaleWhileRevalidate( {
    cacheName: 'googleFonts'
  } )
);

registerRoute(
  /^https:\/\/fonts\.gstatic\.com/,
  new CacheFirst( {
    cacheName: 'googleFonts',
    plugins: [
      new CacheableResponsePlugin( {
        statuses: [ 0, 200 ]
      } ),
      new ExpirationPlugin( {
        maxAgeSeconds: days( 365 ),
        maxEntries: 20
      } )
    ]
  } )
);

// Cache images w/ cache-first strategy
registerRoute(
  /\.(png|gif|jpe?g|svg)$/,
  new CacheFirst( {
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin( {
        maxAgeSeconds: days( 30 ),
        maxEntries: 60
      } )
    ]
  } )
);

// Cache main CFPB stylesheet and our app's overrides
registerRoute(
  /main\.css$/,
  new StaleWhileRevalidate( {
    cacheName: 'styles'
  } )
);

// Cache static JS collected by Django
registerRoute(
  /static\/apps\/mmt-my-money-calendar/,
  new StaleWhileRevalidate( {
    cacheName: 'appAssets'
  } )
);

self.addEventListener( 'message', ( { data, ports: [ port ] } ) => {
  console.log( 'Receive message from window: %O', data );
  port.postMessage( data );
} );
