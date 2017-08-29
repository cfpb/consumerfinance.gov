'use strict';

var ajax = require( 'xdr' );

var COUNTIES_URL = 'https://s3.amazonaws.com/files.consumerfinance.gov/data/mortgage-performance/meta/state_county_dropdown.json';
var METROS_URL = 'https://s3.amazonaws.com/files.consumerfinance.gov/data/mortgage-performance/meta/state_msa_dropdown.json';
var counties;
var metros;

var utils = {
  showEl: el => {
    el.style.display = '';
    return el;
  },
  hideEl: el => {
    el.style.display = 'none';
    return el;
  },
  getCountyData: cb => {
    if ( counties ) {
      return cb( null, counties );
    }
    return ajax( { url: COUNTIES_URL }, function( resp ) {
      var data = JSON.parse( resp.data );
      counties = data;
      cb( null, data );
    } );
  },
  getMetroData: cb => {
    if ( metros ) {
      return cb( null, metros );
    }
    return ajax( { url: METROS_URL }, function( resp ) {
      var data = JSON.parse( resp.data );
      metros = data;
      cb( null, data );
    } );
  },
  getDate: dateString => {
    var dates = dateString.split( '-' );
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
    return `${ months[parseInt( dates[1], 10 ) - 1] }, ${ dates[0] }`;
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
