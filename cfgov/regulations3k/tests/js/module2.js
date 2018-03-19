
var chai = require('chai');
var expect = require('chai').expect;

var module = require( '../../js/module2.js' );

describe( 'Some other module that does somthing', function() {

  it( 'should not throw any errors on init', function() {
    expect( () => module.init() ).to.not.throw();
  });

});
