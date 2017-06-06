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
    url: language === 'es' ? URLS[language] : URLS['en'],
    onSubmit: function( event, selected ) {
        var link = selected.querySelector( 'a' );
        if ( link ) {
          document.location = link.pathname;
        }
    } ,
    renderItem: function( item ) {
      var li = document.createElement( 'li' );
      li.setAttribute( 'data-val', item.question );
      var link = document.createElement( 'a' );
      link.setAttribute( 'href', item.url );
      link.innerText = item.question;
      li.appendChild( link );
      return li;
    }
  } ).init();
}