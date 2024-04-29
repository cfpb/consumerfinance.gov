import htmx from 'htmx.org';

import orderingDropdown from './ordering';
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
      event.detail.history.path = event.detail.history.path.replaceAll(
        /(&htmx=|(?<=\?)htmx=)true/g,
        '',
      );
    }
  },
});

/**
 * htmx extension that adds an `aria-busy=true` HTML attribute
 * to the htmx target container to indicate to screenreaders
 * that a request is in-flight. Removes the attribute after the
 * request completes.
 * See https://htmx.org/extensions/
 * See https://htmx.org/events/#htmx:beforeRequest
 * See https://htmx.org/events/#htmx:afterRequest
 */
htmx.defineExtension('htmx-aria-busy', {
  onEvent: function (name, event) {
    if (name === 'htmx:beforeRequest') {
      event.detail.target.setAttribute('aria-busy', 'true');
    }
    if (name === 'htmx:afterRequest') {
      event.detail.target.setAttribute('aria-busy', 'false');
    }
  },
});

/**
 * htmx extension that saves a snapshot of the TCCP ordering dropdown
 * immediately before rendering new card results and injects it
 * into the page immediately after rendering the results.
 *
 * We query the DOM every time because A) the container is blown away
 * after every htmx request and B) we want a copy of the dropdown that
 * includes the most recently selected value.
 *
 * See https://htmx.org/extensions/
 * See https://htmx.org/events/#htmx:beforeSwap
 * See https://htmx.org/events/#htmx:afterSwap
 */
htmx.defineExtension('move-tccp-ordering', {
  onEvent: function (name) {
    if (name === 'htmx:beforeSwap') {
      orderingDropdown.el = document.querySelector('#tccp-ordering');
    }
    if (name === 'htmx:afterSwap') {
      orderingDropdown.container = document.querySelector(
        '#tccp-ordering-container',
      );
      orderingDropdown.move();
    }
  },
});

/**
 * htmx extension that stores the page's path in web
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

// Store the path on page load before htmx has started up
webStorageProxy.setItem(
  'tccp-filter-path',
  window.location.pathname + window.location.search,
);

// Disable htmx localStorage cache. We've found CFPB pages are
// large enough that htmx hits the localStorage limit pretty
// quickly and throws harmless-but-annoying `historyCacheError`
// console errors.
// See https://htmx.org/attributes/hx-history/
// See https://htmx.org/events/#htmx:historyCacheError
document.body.setAttribute('hx-history', 'false');

// Add htmx extensions to the dom and initialize them
document.body.setAttribute(
  'hx-ext',
  'htmx-url-param, store-tccp-filter-path, move-tccp-ordering, htmx-aria-busy',
);
htmx.process(document.body);
