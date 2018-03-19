
var chai = require('chai');
var expect = require('chai').expect;

var app = require( '../../js/index.js' );

describe( 'The app', function() {

  it( 'should not throw any errors on init', function() {
    expect( () => app ).to.not.throw();
  });

});
