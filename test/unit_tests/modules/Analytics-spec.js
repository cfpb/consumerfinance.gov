'use strict';

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var sandbox;
var Analytics;
var dataLayerOptions;

describe( 'Analytics', function() {
  jsdom();

  before( function() {
    Analytics = require( BASE_JS_PATH + 'modules/Analytics' );
  } );

  beforeEach( function() {
    sandbox = sinon.sandbox.create();

    function push( object ) {
      if ( object.hasOwnProperty( 'callback' ) ) {
        return object.callback();
      }
      return [].push.call( this, object );
    }
    window.dataLayer = [];
    window.dataLayer.push = push;

    delete window.google_tag_manager;
    Analytics.tagManagerIsLoaded = false;

    dataLayerOptions = {
      event:        'CFGOV Event',
      action:       '',
      label:        '',
      eventTimeout: 500
    };

  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( '.init()', function() {
    it( 'should have a proper state after initialization', function() {
      expect( Analytics.tagManagerIsLoaded === false ).to.be.true;
      window.google_tag_manager = {};
      Analytics.init();
      expect( Analytics.tagManagerIsLoaded === true ).to.be.true;
    } );

    it( 'should properly set the google_tag_manager object', function() {
      var mockGTMObject = { testing: true };
      Analytics.init();
      expect( Analytics.tagManagerIsLoaded === false ).to.be.true;
      window.google_tag_manager = mockGTMObject;
      expect( Analytics.tagManagerIsLoaded === true ).to.be.true;
      expect( window.google_tag_manager ).to.deep.equal( mockGTMObject );
    } );
  } );

  describe( '.sendEvent()', function() {
    it( 'should properly add objects to the dataLayer Array', function() {
      var action = 'inbox:clicked';
      var label = 'text:null';
      var options = Object.assign( {}, dataLayerOptions, {
        action: action,
        label:  label
      } );
      window.google_tag_manager = {};
      Analytics.init();
      Analytics.sendEvent( action, label );
      expect( window.dataLayer.length === 1 ).to.be.true;
      expect( window.dataLayer[0] ).to.deep.equal( options );
    } );

    it( 'shouldn\'t add objects to the dataLayer Array if GTM is undefined',
    function() {
      var action = 'inbox:clicked';
      var label = 'text:null';
      delete window.google_tag_manager;
      Analytics.init();
      Analytics.sendEvent( action, label );
      expect( window.dataLayer.length === 0 ).to.be.true;
    } );

    it( 'should invoke the callback if provided', function() {
      Analytics.init();
      var action = 'inbox:clicked';
      var label = 'text:null';
      var callback = sinon.stub();
      Analytics.sendEvent( action, label, callback );
      expect( callback.called ).to.be.true;
    } );
  } );

  describe( '.sendEvents()', function() {
    it( 'should properly add objects to the dataLayer Array', function() {
      var options1 = Object.assign( {}, dataLayerOptions, {
        action: 'inbox:clicked',
        label:  'text:label_1'
      } );
      var options2 = Object.assign( {}, dataLayerOptions, {
        action: 'checbox:clicked',
        label:  'text:label_2'
      } );
      window.google_tag_manager = {};
      Analytics.init();
      Analytics.sendEvents( [ options1, options2 ] );
      expect( window.dataLayer.length === 2 ).to.be.true;
    } );

    it( 'shouldn\'t add objects to the dataLayer Array if an array isn\'t passed',
    function() {
      var options1 = Object.assign( {}, dataLayerOptions, {
        action: 'inbox:clicked',
        label:  'text:label_1'
      } );
      var options2 = Object.assign( {}, dataLayerOptions, {
        action: 'checbox:clicked',
        label:  'text:label_2'
      } );
      window.google_tag_manager = {};
      Analytics.init();
      Analytics.sendEvents( options1, options2 );
      expect( window.dataLayer.length === 0 ).to.be.true;
    } );
  } );

} );
