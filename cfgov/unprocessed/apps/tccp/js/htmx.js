import htmx from 'htmx.org';

import webStorageProxy from '../../../js/modules/util/web-storage-proxy';

/**
 * htmx extension that adds an `htmx=true` query parameter
 * to URLs immediately before htmx makes a request and then
 * removes it before pushing it to the browser's history.
 * This allows endpoints fetched by htmx via AJAX to have
 * a URL that is different from their host page's URL,
 * reducing CDN caching mistaken identity bugs.
 *
 * There are other ways to handle htmx cache busting,
 * including a `getCacheBusterParam` config option and
 * using a `Vary: HX-Request` HTTP header, but we've
 * found them to be unreliable with our infrastructure.
 *
 * See https://htmx.org/docs/#caching
 * See https://htmx.org/extensions/
 * See https://htmx.org/events/#htmx:configRequest
 * See https://htmx.org/events/#htmx:beforeHistoryUpdate
 */
htmx.defineExtension('htmx-url-param', {
  onEvent: function (name, event) {
    if (name === 'htmx:configRequest') {
      event.detail.parameters.htmx = 'true';
    }
    if (name === 'htmx:beforeHistoryUpdate') {
      event.detail.history.path = event.detail.history.path.replace(
        /&?htmx=true/,
        '',
      );
    }
  },
});

/**
 * htmx extension that stores the page's pathname in web
 * storage whenever it's updated
 * See https://htmx.org/extensions/
 * See https://htmx.org/events/#htmx:replacedInHistory
 */
htmx.defineExtension('store-tccp-filter-path', {
  onEvent: function (name, event) {
    if (name === 'htmx:replacedInHistory') {
      webStorageProxy.setItem('tccp-filter-path', event.detail.path);
    }
  },
});

// Add htmx extensions to the dom and initialize them
document.body.setAttribute('hx-ext', 'htmx-url-param, store-tccp-filter-path');
htmx.process(document.body);
