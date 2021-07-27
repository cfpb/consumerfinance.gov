/* ==========================================================================
   Scripts for Ask Autocomplete.
   ========================================================================== */

import Autocomplete from '../../molecules/Autocomplete';

const URLS = {
  en: '/ask-cfpb/api/autocomplete/?term=',
  es: '/es/obtener-respuestas/api/autocomplete/?term='
};

const autocompleteContainer = document.querySelector( '.m-autocomplete' );
const errorMessage = document.querySelector( '#o-search-bar-error_message' );

function handleMaxCharacters() {
  console.log( event );
}

if ( autocompleteContainer ) {
  const language = autocompleteContainer.getAttribute( 'data-language' );

  const autocomplete = new Autocomplete( autocompleteContainer, {
    url: language === 'es' ? URLS.es : URLS.en,
    errorMessage: errorMessage,
    onSubmit: function( event, selected ) {
      const link = selected.querySelector( 'a' );
      const href = link.getAttribute( 'href' );
      if ( link && href ) {
        document.location = href;
      }
    },
    renderItem: function( item ) {
      const li = document.createElement( 'li' );
      li.setAttribute( 'data-val', item.question );
      const link = document.createElement( 'a' );
      link.setAttribute( 'href', item.url );
      link.innerHTML = item.question;
      li.appendChild( link );
      return li;
    }
  } );
  autocomplete.addEventListener( 'maxCharacterChange', handleMaxCharacters );
  autocomplete.init();
}
