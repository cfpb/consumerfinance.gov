'use strict';

var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'Get Event States', function() {
  var $, navPrimary, sandbox, $link;

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    navPrimary = require( '../../../cfgov/v1/preprocessed/js/modules/nav-primary.js' );
    sandbox = sinon.sandbox.create();
  } );

  beforeEach( function() {
    //  Adding a simplified version of the thing we want to test.
    //  Then calling jQuery to test after.
    $( 'body' ).html(
      '<div class="js-primary-nav">' +
        '<div class="js-primary-nav_trigger"></div>' +
        '<div class="nav-item-1 js-primary-nav_item">' +
          '<a class="nav-link-1 js-primary-nav_link" ' +
             'href="http:// github.com">Link</a>' +
          '<div class="sub-nav-1 js-sub-nav" aria-expanded="false">' +
            '<button class="sub-nav-back-1 js-sub-nav_back">Back</button>' +
            '<a href="some-url">First Link</a>' +
          '</div>' +
        '</div>' +
        '<div class="nav-item-2 js-primary-nav_item">' +
          '<a class="nav-link-2 js-primary-nav_link" ' +
             'href="http:// github.com">Link</a>' +
          '<div class="sub-nav-2 js-sub-nav" aria-expanded="false">' +
            '<button class="js-sub-nav_back">Back</button>' +
            '<a href="some-url">First Link</a>' +
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
    beforeEach( function() {
      $link = $( $( '.sub-nav-1' ).find( 'a' )[0] );

      $( '.nav-link-1' ).trigger( 'click' );
    } );

    it( 'should not navigate away from the page', function() {
      expect( window.location.href ).to.not.equal( 'http:// www.google.com/' );
    } );

    it( 'should toggle the sibling sub nav', function() {
      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'true' );
    } );

    it( 'should not toggle a non-sibling sub nav', function() {
      expect( $( '.sub-nav-2' ).attr( 'aria-expanded' ) ).to.equal( 'false' );
    } );

    it( 'should focus the first link in the sibling sub nav', function( done ) {
      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( $link.is( ':focus' ) ).to.be.true;
        done();
      }, 500 );
    } );

    it( 'should not focus the first link in a non-sibling sub nav',
      function( done ) {
        var $nextlink = $( $( '.sub-nav-2' ).find( 'a' )[0] );

        setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
          expect( $nextlink.is( ':focus' ) ).to.be.false;
          done();
        }, 500 );
      } );
  } );

  describe( 'Primary Nav Link Events - One expanded', function() {
    beforeEach( function() {
      $link = $( $( '.sub-nav-2' ).find( 'a' )[0] );

      $( '.sub-nav-1' ).attr( 'aria-expanded', 'true' );
      $( '.nav-link-2' ).trigger( 'click' );
    } );

    it( 'should close others', function() {
      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'false' );
    } );

    it( 'should open the sibling sub nav', function( done ) {
      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( $( '.sub-nav-2' ).attr( 'aria-expanded' ) ).to.equal( 'true' );
        done();
      }, 500 );
    } );

    it( 'should focus the first link in sibling sub nav', function( done ) {
      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( $link.is( ':focus' ) ).to.be.true;
        done();
      }, 500 );
    } );

    it( 'should close itself', function( done ) {
      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        $( '.nav-link-2' ).trigger( 'click' );

        expect( $( '.sub-nav-2' ).attr( 'aria-expanded' ) ).to.equal( 'false' );
        done();
      }, 500 );
    } );

    it( 'should focus the primary link after closing', function( done ) {
      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        $( '.nav-link-2' ).trigger( 'click' );

        setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
          expect( $( '.nav-link-2' ).is( ':focus' ) ).to.be.true;
          done();
        }, 500 );
      }, 500 );
    } );
  } );

  describe( 'Primary Nav Trigger Events', function() {
    beforeEach( function() {
      $link = $( '.nav-link-1' );

      $( '.js-primary-nav_trigger' ).trigger( 'click' );
    } );

    it( 'should open the primary nav', function() {
      expect( $( '.js-primary-nav' ).attr( 'aria-expanded' ) )
        .to.equal( 'true' );
    } );

    it( 'should focus the first primary link', function( done ) {
      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( $link.is( ':focus' ) ).to.be.true;
        done();
      }, 500 );
    } );

    it( 'should close the open primary nav', function() {
      $( '.js-primary-nav_trigger' ).trigger( 'click' );

      expect( $( '.js-primary-nav' ).attr( 'aria-expanded' ) )
        .to.equal( 'false' );
    } );

    it( 'should focus the trigger after closing', function( done ) {
      $( '.js-primary-nav_trigger' ).trigger( 'click' );

      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( $( '.js-primary-nav_trigger' ).is( ':focus' ) ).to.be.true;
        done();
      }, 500 );
    } );
  } );

  describe( 'Sub Nav Back Events', function() {
    beforeEach( function() {
      $link = $( '.nav-link-1' );

      $( '.sub-nav-1' ).attr( 'aria-expanded', 'true' );
      $( '.sub-nav-back-1' ).trigger( 'click' );
    } );

    it( 'should close the sub nav', function() {
      expect( $( '.sub-nav-1' ).attr( 'aria-expanded' ) ).to.equal( 'false' );
    } );

    it( 'should focus the primary link after closing', function( done ) {
      setTimeout( function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( $link.is( ':focus' ) ).to.be.true;
        done();
      }, 500 );
    } );
  } );
} );
