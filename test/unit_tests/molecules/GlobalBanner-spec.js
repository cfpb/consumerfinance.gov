'use strict';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var StorageMock = require( '../fixtures/StorageMock' );

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';
var globalBanner;
var clickEvent;
var contentDom;
var contentAnimatedDom;
var GlobalBanner;
var targetDom;
var toggleStoredStateSpy;
var webStorageProxy;

describe( 'Global Banner State', function() {

  jsdom( {
    created: function( error, win ) {
      if ( error ) console.log( error );
      win.Modernizr = {};
    }
  } );

  before( function() {
    webStorageProxy =
      require( BASE_JS_PATH + 'modules/util/web-storage-proxy.js' );
  } );

  beforeEach( function() {

    // TODO: Investigate importing the HTML directly from the atomic template.
    document.body.innerHTML =
    '<div class="m-global-banner">' +
        '<div class="wrapper ' +
                    'wrapper__match-content ' +
                    'm-expandable ' +
                    'm-expandable__expanded">' +
            '<div class="m-global-banner_head">' +
                '<span class="cf-icon ' +
                             'cf-icon-error-round ' +
                             'm-global-banner_icon"></span>' +
                'This beta site is a work in progress.' +
            '</div>' +
            '<div class="m-expandable_content" aria-expanded="true" style="height: 22px;">' +
                '<p class="m-global-banner_desc  m-expandable_content-animated">' +
                    'We’re prototyping new designs. Things may not work as expected. ' +
                    'Our regular site continues to be at ' +
                    '<a href="http://www.consumerfinance.gov/">www.consumerfinance.gov</a>.' +
                '</p>' +
            '</div>' +
            '<button class="btn ' +
                           'm-global-banner_btn ' +
                           'm-expandable_target ' +
                           'm-expandable_link" id="m-global-banner_btn" aria-pressed="true">' +
                '<span class="m-expandable_cue m-expandable_cue-close">' +
                    'Collapse <span class="cf-icon cf-icon-up"></span>' +
                '</span>' +
                '<span class="m-expandable_cue m-expandable_cue-open">' +
                    'More info <span class="cf-icon cf-icon-down"></span>' +
                '</span>' +
            '</button>' +
        '</div>' +
    '</div>';

    contentDom = document.querySelector( '.m-expandable_content' );
    contentAnimatedDom =
      document.querySelector( '.m-expandable_content-animated' );
    contentAnimatedDom.offsetHeight = 300;
    targetDom = document.querySelector( '.m-expandable_target' );

    clickEvent = document.createEvent( 'Event' );
    clickEvent.initEvent( 'click', true, true );

    GlobalBanner = require( BASE_JS_PATH + 'molecules/GlobalBanner' );
    globalBanner = new GlobalBanner( document.querySelector( '.m-global-banner' ) );

    window.localStorage = new StorageMock();
    window.sessionStorage = new StorageMock();

    toggleStoredStateSpy = sinon.spy( globalBanner, 'toggleStoredState' );
  } );

  afterEach( function() {
    // Removed spy from method.
    globalBanner.toggleStoredState.restore();
  } );

  describe( 'init', function() {
    it( 'should have instantiated an Expandable instance', function() {
      globalBanner.init();
      var isExpandable = contentDom.hasAttribute( 'style' );
      expect( isExpandable ).to.be.true;
    } );

    it( 'should have called the initEvents function', function() {
      globalBanner.init();
      targetDom.dispatchEvent( clickEvent );

      window.setTimeout( function() {
        expect( toggleStoredStateSpy.called ).to.be.true;
      }, 0 );
    } );
  } );

  describe( 'toggleStoredState', function() {
    it( 'should set the localStorage state to collasped', function() {
      expect( webStorageProxy.getItem( 'globalBannerIsExpanded' ) )
       .to.be.undefined;
      globalBanner.init();
      globalBanner.toggleStoredState();
      expect( webStorageProxy.getItem( 'globalBannerIsExpanded' ) ).to.equal( 'false' );
    } );

    it( 'should set the localStorage state to expanded', function() {
      expect( webStorageProxy.getItem( 'globalBannerIsExpanded' ) )
        .to.be.undefined;
      globalBanner.init();
      globalBanner.toggleStoredState();
      globalBanner.toggleStoredState();
      expect( webStorageProxy.getItem( 'globalBannerIsExpanded' ) ).to.equal( 'true' );
    } );
  } );

  describe( 'destroy', function() {
    it( 'should remove event handlers and local storage data', function() {
      globalBanner.init();
      globalBanner.toggleStoredState();
      expect( webStorageProxy.getItem( 'globalBannerIsExpanded' ) ).to.equal( 'false' );
      globalBanner.destroy();
      expect( webStorageProxy.getItem( 'globalBannerIsExpanded' ) )
       .to.be.undefined;

      targetDom.dispatchEvent( clickEvent );
      window.setTimeout( function() {
        expect( toggleStoredStateSpy.called ).to.be.false;
      }, 0 );

    } );
  } );


} );

