'use strict';
var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'The Footer Return-to-Top Button', function() {

  var $;

  jsdom();

  before( function() {
    $ = require( 'jquery' );

  } );

  beforeEach( function() {
    // Adding a simplified version of the thing we want to test.
    // Then calling the jQuery to test after
    $( 'body' ).html( $( '<a class="js-return-to-top"' +
                            'href="http://www.google.com/">' +
                            'Back to top' +
                          '</a>' ) );
    require( '../../src/static/js/modules/footer-button.js' ).init();
  } );

  it( 'should trigger animate function when clicked', function() {
    $( 'body' ).scrollTop( 500 );
    var animateSpy = sinon.spy( $.prototype, 'animate' );

    $( '.js-return-to-top' ).trigger( 'click' );
    expect( animateSpy ).called;
  } );

  it( 'should not navigate away from the page', function() {
    $( '.js-return-to-top' ).trigger( 'click' );
    expect( window.location.href ).to.not.equal( 'http://www.google.com/' );
  } );

} );
