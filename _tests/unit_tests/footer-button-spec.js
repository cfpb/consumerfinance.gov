'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'The Footer Return to Top Button', function() {

  var $, footerButton;

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    footerButton = require( '../../src/static/js/modules/footer-button.js' );
  } );

  beforeEach( function() {
    // Adding a simplified version of the thing we want to test.
    $( 'body' ).html( $( '<a class="js-return-to-top" href="#">' +
                         'Back to top' +
                       '</a>' ) );
  } );

  it( 'should exist', function() {
    expect( footerButton ).to.be.ok;
    expect( $( '.js-return-to-top' ) ).to.be.ok;
  } );

  it( 'should return to top of the page when clicked', function() {
    $( '.js-return-to-top' ).click();
  } );

} );
