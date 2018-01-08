/* ==========================================================================
   Scripts for Ask Autocomplete.
   ========================================================================== */

const Autocomplete = require( '../../molecules/Autocomplete' );

const URLS = {
  en: '/ask-cfpb/api/autocomplete/?term=',
  es: '/es/obtener-respuestas/api/autocomplete/?term='
};

const autocompleteContainer = document.querySelector( '.m-autocomplete' );

if ( autocompleteContainer ) {
  const language = autocompleteContainer.getAttribute( 'data-language' );

  const autocomplete = new Autocomplete( autocompleteContainer, {
    url: language === 'es' ? URLS.es : URLS.en,
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
  } ).init();
}
