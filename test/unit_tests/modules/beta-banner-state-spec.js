'use strict';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var StorageMock = require( '../fixtures/StorageMock' );

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';
var betaBanner;
var contentDom;
var contentAnimatedDom;
var targetDom;
var clickEvent;
var webStorageProxy;

describe( 'Beta Banner State', function() {

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

    document.body.innerHTML =
    '<div class="beta-banner m-expandable m-expandable__expanded"' +
    'id="beta-banner">' +
      '<div class="wrapper wrapper__match-content">' +
          '<div class="beta-banner_head">' +
              '<span class="cf-icon cf-icon-error-round beta-banner_icon">' +
              '</span>' +
              'This beta site is a work in progress.' +
          '</div>' +
          '<div class="m-expandable_content" aria-expanded="true">' +
              '<p class="beta-banner_desc  m-expandable_content-animated">' +
                  'We’re prototyping new designs.' +
                  'Things may not work as expected.' +
                  'Our regular site continues to be at' +
                  '<a href="http://www.consumerfinance.gov/">' +
                  'www.consumerfinance.gov</a>.' +
              '</p>' +
          '</div>' +
          '<button class="btn beta-banner_btn m-expandable_target ' +
          'm-expandable_link" id="beta-banner_btn">' +
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

    betaBanner = require( BASE_JS_PATH + 'modules/beta-banner-state.js' );

    window.localStorage = new StorageMock();
    window.sessionStorage = new StorageMock();

  } );

  describe( 'init', function() {
    it( 'should have instantiated an Expandable instance', function() {
      betaBanner.init();
      var isExpandable = contentDom.hasAttribute( 'style' );
      expect( isExpandable ).to.be.true;
    } );

    it( 'should have called the initEvents function', function() {
      var toggleStoredStateSpy = sinon.spy( betaBanner, 'toggleStoredState' );
      betaBanner.init();
      targetDom.dispatchEvent( clickEvent );

      window.setTimeout( function() {
        expect( toggleStoredStateSpy.called ).to.be.true;
      }, 0 );
    } );
  } );

  describe( 'toggleStoredState', function() {
    it( 'should set the localStorage state to collasped', function() {
      expect( webStorageProxy.getItem( 'betaBannerIsExpanded' ) )
       .to.be.undefined;
      betaBanner.init();
      betaBanner.toggleStoredState();
      expect( webStorageProxy.getItem( 'betaBannerIsExpanded' ) === 'true' );
    } );

    it( 'should set the localStorage state to expanded', function() {
      expect( webStorageProxy.getItem( 'betaBannerIsExpanded' ) )
        .to.be.undefined;
      betaBanner.init();
      betaBanner.toggleStoredState();
      betaBanner.toggleStoredState();
      expect( webStorageProxy.getItem( 'betaBannerIsExpanded' ) === 'false' );
    } );
  } );

  describe( 'destroy', function() {
    it( 'should remove event handlers and local storage data', function() {
      betaBanner.toggleStoredState.restore();
      var toggleStoredStateSpy = sinon.spy( betaBanner, 'toggleStoredState' );
      betaBanner.init();
      betaBanner.toggleStoredState();
      expect( webStorageProxy.getItem( 'betaBannerIsExpanded' ) === 'true' );
      betaBanner.destroy();
      expect( webStorageProxy.getItem( 'betaBannerIsExpanded' ) )
       .to.be.undefined;

      targetDom.dispatchEvent( clickEvent );
      window.setTimeout( function() {
        expect( toggleStoredStateSpy.called ).to.be.false;
      }, 0 );

    } );
  } );


} );

