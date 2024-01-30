/**
 * Get the search form field's values.
 * @param {HTMLElement} searchEl - HTML input of the search field.
 * @param {HTMLElement} filterEls - HTML inputs of the search filters.
 * @returns {Array} Array of objects of form field names and values.
 */
function getSearchValues(searchEl, filterEls) {
  // IE doesn't support forEach w/ node lists so convert it to an array.
  filterEls = Array.prototype.slice.call(filterEls);
  const fields = [];
  const field = {};
  field[searchEl.name] = searchEl.value;
  fields.push(field);
  filterEls.forEach((input) => {
    const field = {};
    field[input.name] = input.value;
    fields.push(field);
  });
  return fields;
}

/**
 * Serializes form fields into GET-friendly string.
 * @param {Array} fields - Array of objects of form field key-value pairs.
 * @returns {string} Serialized form fields.
 */
function serializeFormFields(fields) {
  fields = fields.map((field) => {
    let key;
    for (key in field) {
      field = `${key}=${field[key]}`;
    }
    return field;
  });
  return fields.join('&');
}

/**
 * Creates search results URL to be fetched.
 * @param {string} base - URL's base.
 * @param {string} params - URL's GET parameters.
 * @param {object} opts - Object of additional options for the URL.
 * @returns {string} Encoded URL.
 */
function buildSearchResultsURL(base, params, opts) {
  // Currently the only option is for a partial search results template
  opts = opts && opts.partial ? '&partial' : '';
  return `${base}?${params}${opts}`;
}

/**
 * Modifies element to indicate it's loading.
 * @param {HTMLElement} el - Element to show loading.
 * @returns {HTMLElement} Above element.
 */
function showLoading(el) {
  el.style.opacity = 0.5;
  el.className += ' is-loading';
  return el;
}

/**
 * Modifies element to indicate it's not loading.
 * @param {HTMLElement} el - Element to stop loading.
 * @returns {HTMLElement} Above element.
 */
function hideLoading(el) {
  el.style.opacity = 1;
  el.className = el.className.replace(' is-loading', '');
  return el;
}

/**
 * Update the page's URL via replaceState
 * @param {string} base - URL's base.
 * @param {string} params - URL's GET parameters.
 * @returns {string} New URL.
 */
function updateUrl(base, params) {
  const url = `${base}?${params}`;
  window.history.replaceState(null, null, url);
  return url;
}

/**
 * Check error and do something with it
 * @param {string} code - Error code
 * @returns {object} Error object to be handled by DOM.
 */
function handleError(code) {
  const error = {
    message: null,
    code: code || 0,
  };
  switch (code) {
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

export {
  getSearchValues,
  serializeFormFields,
  buildSearchResultsURL,
  showLoading,
  hideLoading,
  handleError,
  updateUrl,
};
