'use strict';
var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'The Footer Return-to-Top Button', function() {
  var $, footerButton, sandbox;

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    footerButton = require( '../../../src/static/js/modules/footer-button.js' );
    sandbox = sinon.sandbox.create();
  } );

  beforeEach( function() {
    // Adding a simplified version of the thing we want to test.
    // Then calling the jQuery to test after
    $( 'body' ).html( $( '<a class="js-return-to-top"' +
                            'href="http://www.google.com/">' +
                            'Back to top' +
                          '</a>' ) );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  it( 'should not trigger an animate before an init', function() {
    $( 'body' ).scrollTop( 500 );
    var AnimateSpy = sandbox.spy( $.prototype, 'animate' );

    $( '.js-return-to-top' ).trigger( 'click' );
    expect( AnimateSpy.called ).to.not.be.ok;
  } );

  it( 'should trigger animate function when clicked', function() {
    footerButton.init();
    $( 'body' ).scrollTop( 500 );
    var animateSpy = sandbox.spy( $.prototype, 'animate' );

    $( '.js-return-to-top' ).trigger( 'click' );
    expect( animateSpy.called ).to.be.ok;
  } );

  it( 'should not navigate away from the page', function() {
    $( '.js-return-to-top' ).trigger( 'click' );
    expect( window.location.href ).to.not.equal( 'http://www.google.com/' );
  } );

  it( 'should remove handlers when item is removed', function() {
    var animateSpy = sinon.spy( $.prototype, 'animate' );
    $( '.js-return-to-top' ).remove();
    $( '.js-return-to-top' ).trigger( 'click' );
    expect( animateSpy.called ).to.not.be.ok;
  } );

} );
