'use strict';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

var clickEvent;
var link;
var span;
var shouldRedirectURLArray = [
  'http://www.consumerfinance.net/',
  'http://www.google.com/',
  'https://www.facebook.com/dialog/share?app_id=210516218981921' +
  '&display=page&href=http%3A//test.demo.gov/' +
  'the-bureau/about-deputy-director/&redirect_uri=http%3A//test.' +
  'demo.gov/the-bureau/about-deputy-director/',
  'https://www.linkedin.com/company/consumer-financial-protection-bureau'
];
var shouldNotRedirectURLArray = [
  'http://localhost:8000/blog/',
  'http://beta.consumerfinance.gov/careers/working-at-cfpb/',
  'https://test.demo.gov/',
  'http://www.federalreserve.gov/oig/default.html',
  'http://beta.consumerfinance.gov/offices/open-government/'
];

var EXTERNAL_SITE_PATH = '/external-site/?ext_url=';
var SITE_URL = 'www.example.com';

describe( 'External Site', function() {

  jsdom( {
    created: function( error, window ) {
      if ( error ) console.log( error );
      var _href;

      delete window.location;
      window.location = {};

      Object.defineProperty( window.location, 'href', {
        get: function() {
          return _href;
        },
        set: function( url ) {
          _href = url;
        },
        enumerable: true,
        configurable: true
      } );
    }
  } );

  beforeEach( function() {
    span = document.createElement( 'span' );
    span.textContent = 'let slip the dogs of war';
    link = document.createElement( 'a' );
    link.appendChild( span );

    document.body.id = 'main';
    document.body.appendChild( link );

    clickEvent = document.createEvent( 'Event' );
    clickEvent.initEvent( 'click', true, true );
    window.location.href = SITE_URL;

    require( '../../../cfgov/unprocessed/js/modules/external-site-redirect.js' )
      .init();
  } );

  describe( 'Redirect', function() {

    it( 'should redirect external links', function() {
      shouldRedirectURLArray.forEach( function( url ) {
        link.href = url;
        link.dispatchEvent( clickEvent );
        expect( window.location.href ).to
          .equal( EXTERNAL_SITE_PATH + encodeURIComponent( url ) );
      } );
    } );

    it( 'should not redirect internal links', function() {
      shouldNotRedirectURLArray.forEach( function( url ) {
        link.href = url;
        link.dispatchEvent( clickEvent );
        expect( window.location.href ).to.equal( SITE_URL );
      } );
    } );

    it( 'should handle click events when anchor links have spans', function() {
      shouldNotRedirectURLArray.forEach( function( url ) {
        link.href = url;
        span.dispatchEvent( clickEvent );
        expect( window.location.href ).to.equal( SITE_URL );
      } );
    } );

    it( 'should do nothing when a click event is fired on non-anchor elements',
    function() {
      document.body.dispatchEvent( clickEvent );
      expect( window.location.href ).to.equal( SITE_URL );
    } );

  } );

} );
