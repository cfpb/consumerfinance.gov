'use strict';

function shouldShouldnt( should ) {

  return should === 'should' ? true : false;
}

function toCamelCase( string ) {

  return string.replace( /\s(\w)/g, function( matches, letter ) {

    return letter.toUpperCase();
  } );
}

module.exports = {
  shouldShouldnt: shouldShouldnt,
  toCamelCase:    toCamelCase
};
