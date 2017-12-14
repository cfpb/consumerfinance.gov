const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const sinon = require( 'sinon' );
const expect = chai.expect;

describe( 'Event States', () => {
  let expandedState;
  let sandbox;
  let divExpanded;
  let divClosed;
  let openMenu;

  before( () => {
    this.jsdom = require( 'jsdom-global' )();
    expandedState = require( BASE_JS_PATH + 'modules/util/expanded-state.js' );
    sandbox = sinon.sandbox.create();
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    const mockedContent = '<div class="div-expanded" aria-expanded="true" />' +
                          '<div class="div-closed" aria-expanded="false" />';
    document.body.innerHTML = mockedContent;
    divExpanded = document.querySelector( '.div-expanded' );
    divClosed = document.querySelector( '.div-closed' );
    openMenu = document.querySelectorAll( 'div' );
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  describe( 'get expanded state', () => {
    it( 'should return true when expanded', () => {
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.true;
    } );

    it( 'should return false when closed', () => {
      expect( expandedState.isThisExpanded( divClosed ) ).to.be.false;
    } );

    it( 'should return true if at least one is expanded', () => {
      const testExpandedDivs = document.querySelectorAll( 'div' );

      expect( expandedState.isOneExpanded( testExpandedDivs ) ).to.be.true;
    } );

    it( 'should return false if at least one isn’t expanded', () => {
      const testClosedDivs = document.querySelectorAll( 'div' );
      for ( let i = 0, len = testClosedDivs.length; i < len; i++ ) {
        expect( expandedState.isOneExpanded( testClosedDivs[i] ) ).to.be.false;
      }
    } );
  } );

  describe( 'set expanded state - default state', () => {
    it( 'should toggle a closed div open', () => {
      expandedState.toggleExpandedState( divClosed );
      expect( expandedState.isThisExpanded( divClosed ) ).to.be.true;
    } );

    it( 'should toggle an open div closed', () => {
      expandedState.toggleExpandedState( divExpanded );
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use null state to toggle an open div closed', () => {
      expandedState.toggleExpandedState( divExpanded, null );
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use false state to close an open div', () => {
      expandedState.toggleExpandedState( divExpanded, 'false' );
      expect( expandedState.isThisExpanded( divExpanded ) ).to.be.false;
    } );

    it( 'should use true state to open a closed div', () => {
      expandedState.toggleExpandedState( divClosed, 'true' );
      expect( expandedState.isThisExpanded( divClosed ) ).to.be.true;
    } );
  } );

  describe( 'set expanded state - open state', () => {
    it( 'should close all open divs', () => {
      for ( let i = 0, len = openMenu.length; i < len; i++ ) {
        expandedState.toggleExpandedState( openMenu[i], 'false' );
        expect( expandedState.isOneExpanded( openMenu[i] ) ).to.be.false;
      }
    } );

    it( 'should fire a callback after toggling', done => {
      for ( let i = 0, len = openMenu.length; i < len; i++ ) {
        expandedState.toggleExpandedState( openMenu[i], null, () => { // eslint-disable-line no-loop-func, no-inline-comments, max-len
          expect( expandedState.isThisExpanded( divClosed ) ).to.be.true;
          done();
        } );
      }
    } );
  } );
} );
