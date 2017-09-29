'use strict';

const ajax = require( 'xdr' );

const COUNTIES_URL = '/data-research/mortgages/api/v1/metadata/state_county_meta';
const METROS_URL = '/data-research/mortgages/api/v1/metadata/state_msa_meta';
const NON_METROS_URL = '/data-research/mortgages/api/v1/metadata/non_msa_fips';
let counties, metros, nonMetros;
let globalZoomLevel = 10;

var utils = {
  showEl: el => {
    el.style.display = '';
    return el;
  },
  hideEl: el => {
    el.style.display = 'none';
    return el;
  },
  disableEl: el => {
    el.disabled = true;
    return el;
  },
  enableEl: el => {
    el.disabled = false;
    return el;
  },
  addOption: ( { document, value, text, selected = false } ) => {
    const option = document.createElement( 'option' );
    option.value = value;
    option.text = text;
    return option;
  },
  getCountyData: cb => {
    if ( counties ) {
      return cb( counties );
    }
    return ajax( { url: COUNTIES_URL }, function( resp ) {
      var data = JSON.parse( resp.data );
      cb( data );
    } );
  },
  getMetroData: cb => {
    if ( metros ) {
      return cb( metros );
    }
    return ajax( { url: METROS_URL }, function( resp ) {
      var data = JSON.parse( resp.data );
      cb( data );
    } );
  },
  getNonMetroData: cb => {
    if ( nonMetros ) {
      return cb( nonMetros );
    }
    return ajax( { url: NON_METROS_URL }, function( resp ) {
      var data = JSON.parse( resp.data );
      cb( data );
    } );
  },
  getDate: dateString => {
    var dates = dateString.split( '-' );
    if ( dates.length < 2 ) {
      return dateString;
    }
    var months = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ];
    return `${ months[parseInt( dates[1], 10 ) - 1] } ${ dates[0] }`;
  },
  // Non-metro areas have FIPS that include "-non"
  isNonMetro: fips => fips.indexOf( '-non' ) > -1,
  getZoomLevel: zoomLevel => {
    const level = zoomLevel / globalZoomLevel;
    globalZoomLevel = zoomLevel;
    return level;
  },
  setZoomLevel: zoomLevel => {
    globalZoomLevel = zoomLevel;
    return zoomLevel;
  },
  // Centroid of every state on the map organized by FIPS code
  stateCentroids: {
    AL: [ 6614, -5006.5 ],
    AK: [ 357, -3476.5 ],
    AZ: [ 1129.5, -5601 ],
    AR: [ 5353, -5486.5 ],
    CA: [ -169.5, -6770.5 ],
    CO: [ 2599, -6679 ],
    CT: [ 9038, -7795.5 ],
    DE: [ 8669, -7063 ],
    DC: [ 8363, -6930.5 ],
    FL: [ 7381, -3947.5 ],
    GA: [ 7331.5, -5141.5 ],
    HI: [ 2488.5, -3036.95 ],
    ID: [ 1130, -8589 ],
    IL: [ 5851, -6820 ],
    IN: [ 6492, -6872 ],
    IA: [ 5047.5, -7352.5 ],
    KS: [ 4061.5, -6458 ],
    KY: [ 6660.5, -6353.5 ],
    LA: [ 5561.5, -4534.5 ],
    ME: [ 9465, -8891 ],
    MD: [ 8307, -6973.5 ],
    MA: [ 9201, -8040 ],
    MI: [ 6341, -8191 ],
    MN: [ 5000.5, -8503.5 ],
    MS: [ 5894.5, -4964 ],
    MO: [ 5283.5, -6413.5 ],
    MT: [ 2093, -8873 ],
    NE: [ 3823, -7249 ],
    NV: [ 410, -6945.5 ],
    NH: [ 9135, -8472.5 ],
    NJ: [ 8748, -7351.5 ],
    NM: [ 2360.5, -5499 ],
    NY: [ 8446.5, -8057 ],
    NC: [ 7943, -5998 ],
    ND: [ 3762, -8803 ],
    OH: [ 7153.5, -7106 ],
    OK: [ 3979, -5642 ],
    OR: [ -14, -8514.5 ],
    PA: [ 8134.5, -7407 ],
    RI: [ 9258, -7890 ],
    SC: [ 7775.5, -5432.5 ],
    SD: [ 3736, -7957.5 ],
    TN: [ 6647, -5875 ],
    TX: [ 3643, -4555 ],
    UT: [ 1404, -6966 ],
    VT: [ 8870, -8408 ],
    VA: [ 7940.5, -6574 ],
    WA: [ 233, -9336.5 ],
    WV: [ 7734, -6797 ],
    WI: [ 5661, -8084 ],
    WY: [ 2328, -7755 ]
  },
  thunkMiddleware: store => next => action => {
    if ( typeof action === 'function' ) {
      return action( store.dispatch, store.getState );
    }
    return next( action );
  },
  loggerMiddleware: store => next => action => {
    if ( !window.MP_DEBUG ) {
      return next( action );
    }
    console.groupCollapsed( action.type );
    console.group( 'action:' );
    console.log( JSON.stringify( action, '', '\t' ) );
    console.groupEnd();
    console.groupCollapsed( 'previous state:' );
    console.log( JSON.stringify( store.getState(), '', '\t' ) );
    console.groupEnd();
    var result = next( action ); // eslint-disable-line
    console.groupCollapsed( 'state:' );
    console.log( JSON.stringify( store.getState(), '', '\t' ) );
    console.groupEnd();
    console.groupEnd();
    return result;
  }
};

module.exports = utils;
