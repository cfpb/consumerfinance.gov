globalThis.addEventListener('install', () => {
  // Force the waiting service worker to become the active service worker immediately
  globalThis.skipWaiting();
});

globalThis.addEventListener('activate', () => {
  // Unregister itself from the browser
  globalThis.registration
    .unregister()
    .then(() => {
      // Clear all caches associated with this domain
      return caches.keys();
    })
    .then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => caches.delete(cacheName)),
      );
    })
    .then(() => {
      // Force all open tabs/clients to reload to apply changes immediately
      return globalThis.clients.matchAll({ type: 'window' });
    })
    .then((clients) => {
      clients.forEach((client) => {
        if (client.url && 'navigate' in client) {
          client.navigate(client.url);
        }
      });
    });
});
