'use strict';
var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'Get Event States', function() {
  var $, navPrimary, sandbox;

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    navPrimary = require( '../../../src/static/js/modules/nav-primary.js' );
    sandbox = sinon.sandbox.create();
  } );

  beforeEach( function() {
    //  Adding a simplified version of the thing we want to test.
    //  Then calling the jQuery to test after
    $( 'body' ).html(
      '<div class="js-primary-nav">' +
        '<div class="js-primary-nav_trigger"></div>' +
        '<div class="nav-item-1">' +
          '<a class="nav-link-1 js-primary-nav_link" ' +
             'href="http:// github.com">Link</a>' +
          '<div class="sub-nav-1 js-sub-nav" aria-expanded="false">' +
            '<button class="sub-nav-back-1 js-sub-nav_back">Back</button>' +
          '</div>' +
        '</div>' +
        '<div class="nav-item-2">' +
          '<a class="nav-link-2 js-primary-nav_link" ' +
             'href="http:// github.com">Link</a>' +
          '<div class="sub-nav-2 js-sub-nav" aria-expanded="false">' +
            '<button class="js-sub-nav_back">Back</button>' +
          '</div>' +
        '</div>' +
      '</div>'
    );
    navPrimary.init();
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( 'Primary Nav Link Events - Default state', function() {

    it( 'should not navigate away from the page', function() {
      $( '.nav-link-1' ).trigger( 'click' );

      expect( window.location.href ).to.not.equal( 'http:// www.google.com/' );
    } );

    it( 'should toggle the sibling sub nav', function() {
      $( '.nav-link-1' ).trigger( 'click' );

      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'true' );
    } );

    it( 'should not toggle a non-sibling sub nav', function() {
      $( '.nav-link-2' ).trigger( 'click' );

      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'false' );
    } );
  } );

  describe( 'Primary Nav Link Events - One expanded', function() {
    it( 'should close itself', function() {
      $( '.sub-nav-1' ).attr( 'aria-expanded', 'true' );
      $( '.nav-link-1' ).trigger( 'click' );

      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'false' );
    } );

    it( 'should close others, then open sibling sub nav', function() {
      $( '.sub-nav-1' ).attr( 'aria-expanded', 'true' );
      $( '.nav-link-2' ).trigger( 'click' );

      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'false' );

      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( $( '.sub-nav-2' ).attr( 'aria-expanded' ) ).to.equal( 'true' );
      }, 500 );
    } );
  } );

  describe( 'Primary Nav Trigger Events', function() {
    it( 'should toggle the primary nav', function() {
      $( '.js-primary-nav_trigger' ).trigger( 'click' );

      expect( $( '.js-primary-nav' ).attr( 'aria-expanded' ) )
        .to.equal( 'true' );
    } );
  } );

  describe( 'Sub Nav Back Events', function() {
    it( 'should close the sub nav', function() {
      $( '.sub-nav-1' ).attr( 'aria-expanded', 'true' );
      $( '.sub-nav-back-1' ).trigger( 'click' );

      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'false' );
    } );
  } );
} );
