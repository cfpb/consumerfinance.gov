/**
 * Get the search form field's values.
 *
 * @param {HTMLNode} searchEl HTML input of the search field.
 * @param {HTMLNode} filterEls HTML inputs of the search filters.
 * @returns {Array} Array of objects of form field names and values.
 */
function getSearchValues( searchEl, filterEls ) {
  const fields = [];
  let field = {};
  field[searchEl.name] = searchEl.value;
  fields.push( field );
  // IE doesn't support forEach w/ node lists so convert it to an array.
  filterEls = Array.prototype.slice.call( filterEls );
  filterEls.forEach( input => {
    field = {};
    field[input.name] = input.value;
    fields.push( field );
  } );
  return fields;
}

/**
 * Serializes form fields into GET-friendly string.
 *
 * @param {Array} fields Array of objects of form field key-value pairs.
 * @returns {String} Serialized form fields.
 */
function serializeFormFields( fields ) {
  fields = fields.map( field => {
    for ( const key in field ) {
      field = `${ key }=${ field[key] }`;
    }
    return field;
  } );
  return fields.join( '&' );
}

/**
 * Creates search results URL to be fetched.
 *
 * @param {String} base URL's base.
 * @param {String} params URL's GET parameters.
 * @param {Object} opts Object of additional options for the URL.
 * @returns {String} Encoded URL.
 */
function buildSearchResultsURL( base, params, opts ) {
  // Currently the only option is for a partial search results template
  opts = opts && opts.partial ? '&partial' : '';
  return `${ base }?${ params }${ opts }`;
}

/**
 * Modifies element to indicate it's loading.
 *
 * @param {HTMLNode} el Element to show loading.
 * @returns {HTMLNode} Above element.
 */
function showLoading( el ) {
  el.style.opacity = 0.5;
  return el;
}

/**
 * Modifies element to indicate it's not loading.
 *
 * @param {HTMLNode} el Element to stop loading.
 * @returns {HTMLNode} Above element.
 */
function hideLoading( el ) {
  el.style.opacity = 1;
  return el;
}

/**
 * Uncheck checkbox.
 *
 * @param {HTMLNode} el Input element to uncheck.
 * @returns {HTMLNode} Input element.
 */
function clearCheckbox( el ) {
  el.checked = false;
  return el;
}

/**
 * Update the page's URL via replaceState
 *
 * @param {String} base URL's base.
 * @param {String} params URL's GET parameters.
 * @returns {String} New URL.
 */
function updateUrl( base, params ) {
  const url = `${ base }?${ params }`;
  window.history.replaceState( null, null, url );
  return url;
}

/**
 * Check error and do something with it
 *
 * @param {String} code Error code
 * @returns {Object} Error object to be handled by DOM.
 */
function handleError( code ) {
  const error = {
    message: null,
    code: code || 0
  };
  switch ( code ) {
    case 'no-results':
      error.msg = 'Your query returned zero results.';
      break;
    case 0:
      error.msg = 'Search request was cancelled.';
      break;
    default:
      error.msg = 'Sorry, our search engine is temporarily down.';
      break;
  }
  return error;
}

module.exports = {
  getSearchValues: getSearchValues,
  serializeFormFields: serializeFormFields,
  buildSearchResultsURL: buildSearchResultsURL,
  showLoading: showLoading,
  hideLoading: hideLoading,
  clearCheckbox: clearCheckbox,
  handleError: handleError,
  updateUrl: updateUrl
};
