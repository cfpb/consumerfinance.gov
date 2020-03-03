workbox.setConfig({ debug: true });
workbox.core.skipWaiting();
workbox.core.clientsClaim();

const { Plugin: ExpirationPlugin } = workbox.expiration;
const { Plugin: CacheableResponsePlugin } = workbox.cacheableResponse;
const minutes = (num) => num * 60;
const days = (num) => minutes(num) * 60 * 24;

// Precache compiled Webpack assets:
workbox.precaching.precacheAndRoute(self.__precacheManifest);

// Precache app landing page:
workbox.precaching.precacheAndRoute(['/mmt-my-money-calendar']);

// All navigation routes hit the single-page-app landing page:
workbox.routing.registerNavigationRoute(workbox.precaching.getCacheKeyForURL('/mmt-my-money-calendar'), {
  whitelist: [/mmt-my-money-calendar/],
});

// Cache Google fonts long term:
workbox.routing.registerRoute(
  /^https:\/\/fonts\.google\.com/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'googleFonts',
  })
);

workbox.routing.registerRoute(
  /^https:\/\/fonts\.gstatic\.com/,
  new workbox.strategies.CacheFirst({
    cacheName: 'googleFonts',
    plugins: [
      new CacheableResponsePlugin({
        statuses: [0, 200],
      }),
      new ExpirationPlugin({
        maxAgeSeconds: days(365),
        maxEntries: 20,
      }),
    ],
  })
);

// Cache images w/ cache-first strategy
workbox.routing.registerRoute(
  /\.(png|gif|jpe?g|svg)$/,
  new workbox.strategies.CacheFirst({
    cacheName: 'images',
    plugins: [
      new ExpirationPlugin({
        maxAgeSeconds: days(30),
        maxEntries: 60,
      }),
    ],
  })
);

// Cache main CFPB stylesheet and our app's overrides
workbox.routing.registerRoute(
  /main\.css$/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'styles',
  })
);

self.addEventListener('message', ({ data, ports: [port] }) => {
  console.log('Receive message from window: %O', data);
  port.postMessage(data);
});
