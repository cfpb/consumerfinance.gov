const BASE_JS_PATH = '../../../cfgov/unprocessed/js/';
const simpleTableRowLinks =
  require( BASE_JS_PATH + 'modules/o-table-row-links' );

const chai = require( 'chai' );
const expect = chai.expect;
const sinon = require( 'sinon' );
let sandbox;
let tableDom;
let linkDom;
let linkRowCellDom;
let nonLinkRowCellDom;

const HTML_SNIPPET =
  '<table class="o-table__row-links">' +
  '<tbody>' +
    '<tr>' +
      '<th>cell1</th>' +
      '<th class="nonLinkRowCell">cell2</th>' +
      '<th>cell3</th>' +
      '<th>cell4</th>' +
    '</tr>' +
    '<tr>' +
      '<td><a href="http://www.example.info">linkCell5</a></td>' +
      '<td class="linkRowCell">cell6</td>' +
      '<td>cell7</td>' +
      '<td>cell8</td>' +
    '</tr>' +
  '</tbody>' +
  '</table>';

function triggerClickEvent( target ) {
  const event = document.createEvent( 'Event' );
  event.initEvent( 'click', true, true );
  target.dispatchEvent( event );
}

describe( 'o-table-row-links', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )( HTML_SNIPPET );
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    let windowLocation;
    sandbox = sinon.sandbox.create();

    document.body.innerHTML = HTML_SNIPPET;
    tableDom = document.querySelector( '.o-table__row-links' );
    linkDom = tableDom.querySelector( 'a' );
    linkRowCellDom = tableDom.querySelector( '.linkRowCell' );
    nonLinkRowCellDom = tableDom.querySelector( '.nonLinkRowCell' );

    Object.defineProperty( window, 'location', {
      get: () => windowLocation,
      set: function( location ) {
        windowLocation = location;
      },
      enumerable: true,
      configurable: true
    } );

    document.body.addEventListener( 'click', function handleClick( event ) {
      if ( event.target.tagName === 'A' ) {
        window.location = event.target.getAttribute( 'href' );
      }
    } );

    window.location = 'http://www.example.com';

    simpleTableRowLinks.init();
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  it( 'should navigate to new location when link row cell clicked', () => {
    triggerClickEvent( linkRowCellDom );
    expect( window.location ).to.equal( 'http://www.example.info' );
  } );

  it( 'should bubble click events to the parent element when a link is clicked',
    () => {
      triggerClickEvent( linkDom );
      expect( window.location ).to.equal( 'http://www.example.info' );
    }
  );

  it( 'should not navigate to new location when non link row cell clicked',
    () => {
      triggerClickEvent( nonLinkRowCellDom );
      expect( window.location ).to.equal( 'http://www.example.com' );
    }
  );
} );
