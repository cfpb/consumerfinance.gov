'use strict';

function shouldShouldnt( value ) {

  return value === 'should' ? true : false;
}

function toCamelCase( value ) {

  return value.replace( /\s(\w)/g, function( matches, letter ) {

    return letter.toUpperCase();
  } );
}

module.exports = {
  shouldShouldnt: shouldShouldnt,
  toCamelCase:    toCamelCase
};
