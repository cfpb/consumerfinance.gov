import { ajaxRequest as xhr } from '../../../js/modules/util/ajax-request';

/**
 * Get the search form field's values.
 *
 * @param {HTMLNode} searchEl HTML input of the search field.
 * @param {HTMLNode} filterEls HTML inputs of the search filters.
 * @returns {Array} Array of objects of form field names and values.
 */
function getSearchValues( searchEl, filterEls ) {
  const fields = [];
  const field = {};
  field[searchEl.name] = searchEl.value;
  fields.push( field );
  filterEls.forEach( input => {
    const field = {};
    field[input.name] = input.value;
    fields.push( field );
  } );
  return fields;
}

/**
 * Serializes form fields into GET-friendly string.
 *
 * @param {Array} fields Array of objects of form field
 * key-value pairs.
 * @returns {String} xhr
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
 * @returns {String} Encoded URL.
 */
function buildSearchResultsURL( base, params ) {
  return `${ base }?${ params }&partial`;
}

/**
 * Fetches search results partial
 *
 * @param {String} url URL's of search results.
 * @param {Function} cb Function called with the HTML search results partial.
 * @returns {String} Encoded URL.
 */
function fetchSearchResults( url, cb ) {
  return xhr( 'GET', url, {
    success: data => cb( null, data ),
    fail: err => cb( err )
  } );
}

module.exports = {
  getSearchValues: getSearchValues,
  serializeFormFields: serializeFormFields,
  buildSearchResultsURL: buildSearchResultsURL,
  fetchSearchResults: fetchSearchResults
};
