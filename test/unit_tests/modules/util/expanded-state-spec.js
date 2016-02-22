'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var sinon = require( 'sinon' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );

describe( 'Event States', function() {
  var expandedState, sandbox, divExpanded, divClosed, openMenu;

  jsdom();

  before( function() {
    expandedState = require( BASE_JS_PATH + 'modules/util/expanded-state.js' );
    sandbox = sinon.sandbox.create();
  } );

  beforeEach( function() {
    var mockedContent = '<div class="div-expanded" aria-expanded="true" />' +
                        '<div class="div-closed" aria-expanded="false" />';
    document.body.innerHTML = mockedContent;
    divExpanded = document.querySelector( '.div-expanded' );
    divClosed = document.querySelector( '.div-closed' );
    openMenu = document.querySelectorAll( 'div' );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( 'get expanded state', function() {
    it( 'should return true when expanded', function() {
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.true;
    } );

    it( 'should return false when closed', function() {
      expect( expandedState.isThisExpanded( divClosed ) ).to.be.false;
    } );

    it( 'should return true if at least one is expanded', function() {
      var testExpandedDivs = document.querySelectorAll( 'div' );

      expect( expandedState.isOneExpanded( testExpandedDivs ) ).to.be.true;
    } );

    it( 'should return false if at least one isn’t expanded', function() {
      var testClosedDivs = document.querySelectorAll( 'div' );
      for ( var i = 0, len = testClosedDivs.length; i < len; i++ ) {
        expect( expandedState.isOneExpanded( testClosedDivs[i] ) ).to.be.false;
      }
    } );
  } );

  describe( 'set expanded state - default state', function() {
    it( 'should toggle a closed div open', function() {
      expandedState.toggleExpandedState( divClosed );
      expect( expandedState.isThisExpanded( divClosed ) ).to.be.true;
    } );

    it( 'should toggle an open div closed', function() {
      expandedState.toggleExpandedState( divExpanded );
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use null state to toggle an open div closed', function() {
      expandedState.toggleExpandedState( divExpanded, null );
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use false state to close an open div', function() {
      expandedState.toggleExpandedState( divExpanded, 'false' );
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use true state to open a closed div', function() {
      expandedState.toggleExpandedState( divClosed, 'true' );
      expect( expandedState.isThisExpanded( divClosed ) ).to.be.true;
    } );
  } );

  describe( 'set expanded state - open state', function() {
    it( 'should close all open divs', function() {
      for ( var i = 0, len = openMenu.length; i < len; i++ ) {
        expandedState.toggleExpandedState( openMenu[i], 'false' );
        expect( expandedState.isOneExpanded( openMenu[i] ) ).to.be.false;
      }
    } );

    it( 'should fire a callback after toggling', function( done ) {
      for ( var i = 0, len = openMenu.length; i < len; i++ ) {
        expandedState.toggleExpandedState( openMenu[i], null, function() { // eslint-disable-line no-loop-func, no-inline-comments, max-len
          expect( expandedState.isThisExpanded( divClosed ) ).to.be.true;
          done();
        } );
      }
    } );
  } );
} );
