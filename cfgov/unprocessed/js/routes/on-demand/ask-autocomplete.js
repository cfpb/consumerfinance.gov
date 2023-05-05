/* ==========================================================================
   Scripts for Ask Autocomplete.
   ========================================================================== */

import Autocomplete from '../../molecules/Autocomplete';
import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

const URLS = {
  en: '/ask-cfpb/api/autocomplete/?term=',
  es: '/es/obtener-respuestas/api/autocomplete/?term=',
};

const autocompleteContainer = document.querySelector('.m-autocomplete');
const errorMessage = document.querySelector('#o-search-bar_error-message');
const submitButton = document.querySelector(
  '.o-search-bar button[type="submit"]'
);

/**
 * Disable the submit button if the query character limit is reached
 * @param {object} event - The maxCharacterChange event object dispatched from
 *   the autocomplete.
 */
function handleMaxCharacters(event) {
  if (event.maxLengthExceeded) {
    submitButton.setAttribute('disabled', 'true');
    errorMessage.classList.remove('u-hidden');
    analyticsSendEvent({
      action: 'maxLimitReached',
      label: event.searchTerm,
      event: 'Ask Search',
    });
  } else {
    submitButton.removeAttribute('disabled');
    errorMessage.classList.add('u-hidden');
  }
}

if (autocompleteContainer) {
  const language = autocompleteContainer.getAttribute('data-language');

  const autocomplete = new Autocomplete(autocompleteContainer, {
    url: language === 'es' ? URLS.es : URLS.en,
    onSubmit: function (event, selected) {
      const link = selected.querySelector('a');
      const href = link.getAttribute('href');
      if (link && href) {
        document.location = href;
      }
    },
    renderItem: function (item) {
      const li = document.createElement('li');
      li.setAttribute('data-val', item.question);
      const link = document.createElement('a');
      link.setAttribute('href', item.url);
      link.innerHTML = item.question;
      li.appendChild(link);
      return li;
    },
  });
  autocomplete.addEventListener('maxCharacterChange', handleMaxCharacters);
  autocomplete.init();
}
