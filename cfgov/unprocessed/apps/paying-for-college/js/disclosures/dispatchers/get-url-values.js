import queryHandler from '../utils/query-handler.js';

/**
 * Check to see if the URL contains an offer
 * @returns {boolean} URL contains an offer, true/false
 */
const getUrlOfferExists = () => location.search !== '';

/**
 * Create object with URL offer data
 * @returns {object} URL values as key-value pairs
 */
function getUrlValues() {
  const urlValues = queryHandler(location.search);
  return urlValues;
}

export { getUrlOfferExists, getUrlValues };
