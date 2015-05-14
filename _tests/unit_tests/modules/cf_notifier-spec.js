'use strict';
var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'CFNotifier', function() {
  var $, $form;

  jsdom({
    file: '_tests/unit_tests/fixtures/forms.html',
    console: false
  });

  before( function() {
    $ = require( 'jquery' );
    require( '../../../src/static/js/modules/jquery/cf_notifier.js' ).init();
    $form = $( '#email-subscribe-form' );
    $form.cf_notifier();
  } );

  beforeEach( function() {
  } );

  afterEach( function() {
  } );

  it( 'should create a notification', function() {
    $form.trigger( 'cf_notifier:notify' );
    expect(
      $( '.cf-notification' )
    ).to.have.length( 1 );
  } );

  it( 'should not create an additional notification', function() {
    $form.trigger( 'cf_notifier:notify' );
    expect(
      $( '.cf-notification' )
    ).to.have.length( 2 );
  } );

} );
