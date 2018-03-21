const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const expandedState = require( BASE_JS_PATH + 'modules/util/expanded-state.js' );
let divExpanded;
let divClosed;
let openMenu;

const HTML_SNIPPET = `
  <div class="div-expanded" aria-expanded="true" />
  <div class="div-closed" aria-expanded="false" />
`;

describe( 'Event States', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    divExpanded = document.querySelector( '.div-expanded' );
    divClosed = document.querySelector( '.div-closed' );
    openMenu = document.querySelectorAll( 'div' );
  } );

  describe( 'get expanded state', () => {
    it( 'should return true when expanded', () => {
      expect( expandedState.isThisExpanded( divExpanded ) ).toBe( true );
    } );

    it( 'should return false when closed', () => {
      expect( expandedState.isThisExpanded( divClosed ) ).toBe( false );
    } );

    it( 'should return true if at least one is expanded', () => {
      const testExpandedDivs = document.querySelectorAll( 'div' );

      expect( expandedState.isOneExpanded( testExpandedDivs ) ).toBe( true );
    } );

    it( 'should return false if at least one isn’t expanded', () => {
      const testClosedDivs = document.querySelectorAll( 'div' );
      for ( let i = 0, len = testClosedDivs.length; i < len; i++ ) {
        expect( expandedState.isOneExpanded( testClosedDivs[i] ) )
          .toBe( false );
      }
    } );
  } );

  describe( 'set expanded state - default state', () => {
    it( 'should toggle a closed div open', () => {
      expandedState.toggleExpandedState( divClosed );
      expect( expandedState.isThisExpanded( divClosed ) ).toBe( true );
    } );

    it( 'should toggle an open div closed', () => {
      expandedState.toggleExpandedState( divExpanded );
      expect( expandedState.isThisExpanded( divExpanded ) ).toBe( false );
    } );

    it( 'should use null state to toggle an open div closed', () => {
      expandedState.toggleExpandedState( divExpanded, null );
      expect( expandedState.isThisExpanded( divExpanded ) ).toBe( false );
    } );

    it( 'should use false state to close an open div', () => {
      expandedState.toggleExpandedState( divExpanded, 'false' );
      expect( expandedState.isThisExpanded( divExpanded ) ).toBe( false );
    } );

    it( 'should use true state to open a closed div', () => {
      expandedState.toggleExpandedState( divClosed, 'true' );
      expect( expandedState.isThisExpanded( divClosed ) ).toBe( true );
    } );
  } );

  describe( 'set expanded state - open state', () => {
    it( 'should close all open divs', () => {
      for ( let i = 0, len = openMenu.length; i < len; i++ ) {
        expandedState.toggleExpandedState( openMenu[i], 'false' );
        expect( expandedState.isOneExpanded( openMenu[i] ) ).toBe( false );
      }
    } );

    it( 'should fire a callback after toggling', done => {
      for ( let i = 0, len = openMenu.length; i < len; i++ ) {
        expandedState.toggleExpandedState( openMenu[i], null, () => { // eslint-disable-line no-loop-func, no-inline-comments, max-len
          expect( expandedState.isThisExpanded( divClosed ) ).toBe( true );
          done();
        } );
      }
    } );
  } );
} );
