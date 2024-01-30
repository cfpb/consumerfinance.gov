const statesByCode = {
  AZ: 'Arizona',
  AL: 'Alabama',
  AK: 'Alaska',
  AR: 'Arkansas',
  CA: 'California',
  CO: 'Colorado',
  CT: 'Connecticut',
  DC: 'District of Columbia',
  DE: 'Delaware',
  FL: 'Florida',
  GA: 'Georgia',
  HI: 'Hawaii',
  ID: 'Idaho',
  IL: 'Illinois',
  IN: 'Indiana',
  IA: 'Iowa',
  KS: 'Kansas',
  KY: 'Kentucky',
  LA: 'Louisiana',
  ME: 'Maine',
  MD: 'Maryland',
  MA: 'Massachusetts',
  MI: 'Michigan',
  MN: 'Minnesota',
  MS: 'Mississippi',
  MO: 'Missouri',
  MT: 'Montana',
  NE: 'Nebraska',
  NV: 'Nevada',
  NH: 'New Hampshire',
  NJ: 'New Jersey',
  NM: 'New Mexico',
  NY: 'New York',
  NC: 'North Carolina',
  ND: 'North Dakota',
  OH: 'Ohio',
  OK: 'Oklahoma',
  OR: 'Oregon',
  PA: 'Pennsylvania',
  RI: 'Rhode Island',
  SC: 'South Carolina',
  SD: 'South Dakota',
  TN: 'Tennessee',
  TX: 'Texas',
  UT: 'Utah',
  VT: 'Vermont',
  VA: 'Virginia',
  WA: 'Washington',
  WV: 'West Virginia',
  WI: 'Wisconsin',
  WY: 'Wyoming',
};

/**
 * @param {string} code - An abbreviated state name.
 * @returns {string} A full state name, spelled out.
 */
function getStateByCode(code) {
  if ({}.hasOwnProperty.call(statesByCode, code)) {
    return statesByCode[code];
  }

  return '';
}

/**
 * Search for support of the matches() method by looking at
 * browser prefixes.
 * @param {HTMLElement} el - The element to check for support
 *   of matches() method.
 * @returns {Function} The appropriate matches() method of elem.
 */
function _getMatchesMethod(el) {
  return (
    el.matches ||
    el.webkitMatchesSelector ||
    el.mozMatchesSelector ||
    el.msMatchesSelector
  );
}

/**
 * Determine whether element matches a selector.
 * @param {HTMLElement} el - DOM element to check.
 * @param {string} selector - a selector string.
 * @returns {boolean} True if element matches selector, false otherwise.
 */
function selectorMatches(el, selector) {
  const matchesMethod = _getMatchesMethod(el);
  return matchesMethod.call(el, selector);
}

export { getStateByCode, selectorMatches };
