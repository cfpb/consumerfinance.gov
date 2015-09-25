'use strict';

var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'Event States', function() {
  var $, es, sandbox, divExpanded, divClosed, openMenu;

  jsdom();

  before( function() {
    $ = require( 'jquery' );
    es = require( '../../../../cfgov/v1/preprocessed/js/modules/util/expanded-state.js' );
    sandbox = sinon.sandbox.create();
  } );

  beforeEach( function() {
    divExpanded = $( '<div class="div-expanded" aria-expanded="true" />' );
    divClosed = $( '<div class="div-closed" aria-expanded="false" />' );
    openMenu = $( [] ).add( divClosed ).add( divExpanded );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( 'get expanded state', function() {
    it( 'should return true when expanded', function() {
      expect( es.get.isThisExpanded( divExpanded ) ).to.be.true;
    } );

    it( 'should return false when closed', function() {
      expect( es.get.isThisExpanded( divClosed ) ).to.be.false;
    } );

    it( 'should return true if at least one is expanded', function() {
      var testExpandedDivs = $( [] ).add( divClosed ).add( divExpanded );

      expect( es.get.isOneExpanded( testExpandedDivs ) ).to.be.true;
    } );

    it( 'should return false if at least one isn’t expanded', function() {
      var testClosedDivs = $( [] ).add( divClosed ).add( divClosed );

      expect( es.get.isOneExpanded( testClosedDivs ) ).to.be.false;
    } );
  } );


  describe( 'set expanded state - default state', function() {
    it( 'should toggle a closed div open', function() {
      es.set.toggleExpandedState( divClosed );
      expect( es.get.isThisExpanded( divClosed ) ).to.be.true;
    } );

    it( 'should toggle an open div closed', function() {
      es.set.toggleExpandedState( divExpanded );
      expect( es.get.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use null state to toggle an open div closed', function() {
      es.set.toggleExpandedState( divExpanded, null );
      expect( es.get.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use false state to close an open div', function() {
      es.set.toggleExpandedState( divExpanded, 'false' );
      expect( es.get.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use true state to open a closed div', function() {
      es.set.toggleExpandedState( divClosed, 'true' );
      expect( es.get.isThisExpanded( divClosed ) ).to.be.true;
    } );
  } );

  describe( 'set expanded state - open state', function() {
    beforeEach( function() {

    } );

    it( 'should close all open divs', function() {
      es.set.toggleExpandedState( openMenu, 'false' );
      expect( es.get.isOneExpanded( openMenu ) ).to.be.false;
    } );

    it( 'should fire a callback after toggling', function( done ) {
      es.set.toggleExpandedState( openMenu, null, function() { // eslint-disable-line max-nested-callbacks, no-inline-comments, max-len
        expect( es.get.isThisExpanded( divClosed ) ).to.be.true;
        done();
      } );
    } );
  } );
} );
