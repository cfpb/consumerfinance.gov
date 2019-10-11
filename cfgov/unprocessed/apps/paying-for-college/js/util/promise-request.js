
/**
	* Promise requests are better.
	*
	*/

const promiseRequest = function( method, url ) {
	const xhr = new XMLHttpRequest();

	return new Promise( function( resolve, reject ) {

		// Completed xhr
		xhr.onreadystatechange = function() {
			// Do not run unless xhr is complete
			if ( xhr.readyState != 4 ) return; 

			if ( xhr.status >= 200 && xhr.status < 300 ) {
				resolve( xhr );
			} else {
				reject ( {
					status: xhr.status,
					statusText: xhr.statusText
				} );
			}
		};

		// Make XHR request
		if ( typeof method === 'undefined' ) {
			method = 'GET';
		}
		xhr.open( method, url, true );

		xhr.send();

	} );
}

export {
	promiseRequest
};
