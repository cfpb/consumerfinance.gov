// TODO: Remove jquery.
const $ = require( 'jquery' );

const postVerify = {
  csrfToken: null,

  init: function() {
    /* Alternate code. getting token from document.cookie:
       if ( document.cookie && document.cookie != '' ) {
       var cookies = document.cookie.split( ';' );
       for ( var x = 0; x < cookes.length; x++ ) {
       var cookie = $.trim( cookies[ x ] );
       if ( cookie.substring( 0, 10 ) === 'csrftoken=' ) {
       this.csrfToken = cookie.substring( 10 );
       break;
       }
       }
       } */
    this.csrfToken = $( '[name="csrfmiddlewaretoken"]' ).val();
  },

  verify: function( offerID, collegeID, error ) {
    const postdata = {
      csrfmiddlewaretoken: this.csrfToken,
      oid:                 offerID,
      iped:                collegeID,
      errors:              'none',
      URL:                 window.location.href
    };
    const urlPath = '/' + $( 'main' ).attr( 'data-context' ) +
                    '/understanding-your-financial-aid-offer/api/verify/';
    if ( error === true ) {
      postdata.errors =
        'INVALID: student indicated the offer information is wrong';
    }
    $.post( urlPath, postdata );
  }

};

module.exports = postVerify;
