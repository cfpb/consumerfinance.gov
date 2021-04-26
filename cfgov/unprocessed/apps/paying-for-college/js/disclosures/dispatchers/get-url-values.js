const queryHandler = require( '../utils/query-handler' );

const getUrlValues = {

  /**
   * Check to see if the URL contains an offer
   * @returns {boolean} URL contains an offer, true/false
   */
  urlOfferExists: function() {
    return location.search !== '';
  },

  /**
   * Create object with URL offer data
   * @returns {object} URL values as key-value pairs
   */
  urlValues: function() {
    const urlValues = queryHandler( location.search );
    return urlValues;
  }
};

module.exports = getUrlValues;
