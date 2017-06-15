/* ==========================================================================
   Scripts for Ask Autocomplete.
   ========================================================================== */

var Autocomplete = require( '../../molecules/Autocomplete' );

var URLS = {
  'en': '/ask-cfpb/api/autocomplete/?term=',
  'es': '/es/obtener-respuestas/api/autocomplete/?term='
}

var autocompleteContainer = document.querySelector( '.m-autocomplete' );

if ( autocompleteContainer ) {
  var language = autocompleteContainer.getAttribute( 'data-language' );

  var autocomplete = new Autocomplete( autocompleteContainer, { 
    url: language === 'es' ? URLS['es'] : URLS['en'],
    onSubmit: function( event, selected ) {
        var link = selected.querySelector( 'a' );
        var href = link.getAttribute("href");
        if ( link && href ) {
          document.location = href;
        }
    },
    renderItem: function( item ) {
      var li = document.createElement( 'li' );
      li.setAttribute( 'data-val', item.question );
      var link = document.createElement( 'a' );
      link.setAttribute( 'href', item.url );
      link.innerHTML = item.question;
      li.appendChild( link );
      return li;
    }
  } ).init();
}