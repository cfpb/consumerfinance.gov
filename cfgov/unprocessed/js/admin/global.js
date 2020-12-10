const env = location.hostname.split( '.' )[0];

const body = document.querySelector( 'body' );
body.setAttribute( 'data-env', env );
