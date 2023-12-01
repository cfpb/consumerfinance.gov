const postVerify = {
  csrfToken: null,

  init: function () {
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
    const csrfElem = document.querySelector('[name="csrfmiddlewaretoken"]');
    if (csrfElem !== null) {
      this.csrfToken = csrfElem.value;
    }
  },

  verify: function (offerID, collegeID, error) {
    const postdata = {
      csrfmiddlewaretoken: this.csrfToken,
      oid: offerID,
      iped: collegeID,
      errors: 'none',
      URL: window.location.href,
    };
    const urlBase = document.querySelector('main').getAttribute('data-context');
    const urlPath = `/${urlBase}/understanding-your-financial-aid-offer/api/verify/`;
    if (error === true) {
      postdata.errors =
        'INVALID: student indicated the offer information is wrong';
    }

    fetch(urlPath, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postdata),
    });
  },
};

export default postVerify;
