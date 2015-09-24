'use strict';

var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'The focusTarget function', function() {
  var $, focusTarget, sandbox;

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    focusTarget = require( '../../../cfgov/v1/preprocessed/js/modules/focus-target.js' );
    sandbox = sinon.sandbox.create();
  } );

  beforeEach( function() {
    // Adding a simplified version of the thing we want to test.
    // Then calling the jQuery to test after
    $( 'body' ).html( $( '<a id="skip-nav"' +
                            'href="#main">' +
                            'Skip to Main Content' +
                          '</a>' +
                          '<div id="#main"> </div>' ) );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  it( 'should not trigger an attr change before an init', function() {
    var attrSpy = sandbox.spy( $.prototype, 'attr' );

    $( '#skip-nav' ).trigger( 'click' );
    expect( attrSpy.called ).to.not.be.ok;
  } );

  it( 'should trigger attr function when clicked', function() {
    focusTarget.init();
    var attrSpy = sandbox.spy( $.prototype, 'attr' );

    $( '#skip-nav' ).trigger( 'click' );
    expect( attrSpy.called ).to.be.ok;
  } );

} );
