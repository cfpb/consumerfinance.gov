const stringToNum = require( './handle-string-input.js' );

/**
 * Handles URL questy string to turn key-value pairs into an object.
 * @param  {string} queryString - The query string of a url (location.search)
 * @returns {object} - An object containing key-value pairs from the query
 */
function queryHandler( queryString ) {
  const valuePairs = {
    tuitionFees: 0,
    roomBoard: 0,
    books: 0,
    transportation: 0,
    otherExpenses: 0,
    urlProgramLength: 0
  };
  const parameters = {};
  const numericKeys = [
    'iped', 'tuit', 'hous', 'book', 'leng', 'tran', 'othr',
    'pelg', 'schg', 'stag', 'othg', 'mta', 'gib', 'fam', 'wkst', 'parl',
    'perl', 'subl', 'unsl', 'ppl', 'gpl', 'prvl', 'prvi', 'prvf', 'insl',
    'insi', 'sav', 'totl'
  ];
  const keyMaps = {
    iped: 'collegeID',
    pid:  'programID',
    oid:  'offerID',
    leng: 'urlProgramLength',
    tuit: 'tuitionFees',
    hous: 'roomBoard',
    book: 'books',
    tran: 'transportation',
    othr: 'otherExpenses',
    pelg: 'pell',
    schg: 'schoolGrants',
    stag: 'stateGrants',
    othg: 'otherScholarships',
    mta:  'militaryTuitionAssistance',
    gib:  'GIBill',
    fam:  'family',
    wkst: 'workstudy',
    parl: 'parentLoan',
    perl: 'perkins',
    subl: 'directSubsidized',
    unsl: 'directUnsubsidized',
    ppl:  'parentPlus',
    gpl:  'gradPlus',
    prvl: 'privateLoan',
    prvi: 'privateLoanRate',
    prvf: 'privateLoanFee',
    insl: 'tuitionRepay',
    insi: 'tuitionRepayRate',
    inst: 'tuitionRepayTerm',
    totl: 'totalCost'
  };

  /**
   * Helper function for checking that expected numeric values are indeed
   * numeric
   * @param {string} key - The key to be checked
   * @param {string|number} value - The value of the key
   * @returns {string|number} newValue - The corrected value of the key
   */
  function checkValue( key, value ) {
    let newValue = value;

    if ( numericKeys.indexOf( key ) !== -1 ) {
      newValue = stringToNum( value );
    }

    return newValue;
  }

  /**
   * Helper function which decodes key-value pairs from the URL
   * Has no parameters, but relies on the queryString passed to its parent
   * function
   */
  function getPairs() {
    let pair;
    const regex = /[?&]?([^=]+)=([^&]*)/g;

    queryString.split( '+' ).join( ' ' );

    while ( pair = regex.exec( queryString ) ) { // eslint-disable-line no-cond-assign
      const key = decodeURIComponent( pair[1] );
      let value = decodeURIComponent( pair[2] );

      value = checkValue( key, value );
      parameters[key] = value || 0;
    }
  }

  /**
   * Helper function which maps the parameters object using the keyMaps
   */
  function remapKeys() {
    for ( const key in parameters ) {
      if ( keyMaps.hasOwnProperty( key ) ) {
        const newKey = keyMaps[key];
        valuePairs[newKey] = parameters[key];
      }
    }
  }

  /**
   * Helper function that makes sure program lengths are divisible by 6,
   * so they can be displayed and handled as half-year multiples.
   * Both here and in the API, we round up to the next higher 6-month value,
   * so 14 months would round up to 18, which is displayed as 1 ½ years.
   */
  function adjustProgramLength() {

    const lengthValue = valuePairs.urlProgramLength;
    if ( lengthValue % 6 !== 0 ) {
      valuePairs.urlProgramLength = lengthValue + ( 6 - ( lengthValue % 6 ) );
    }
  }

  getPairs();
  remapKeys();
  adjustProgramLength();

  // move private loan properties to privateLoanMulti
  valuePairs.privateLoanMulti = [
    { amount: valuePairs.privateLoan || 0,
      rate:   valuePairs.privateLoanRate / 100 || 0.079,
      fees:   valuePairs.privateLoanFee / 100 || 0,
      deferPeriod: 6 }
  ];
  delete valuePairs.privateLoan;
  delete valuePairs.privateLoanRate;
  delete valuePairs.privateLoanFee;

  // family contributions = parent loan
  valuePairs.family = valuePairs.parentLoan;
  valuePairs.tuitionRepayRate /= 100;

  return valuePairs;
}

module.exports = queryHandler;
