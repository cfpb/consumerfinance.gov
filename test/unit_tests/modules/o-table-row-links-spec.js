'use strict';

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';
var simpleTableRowLinks =
  require( BASE_JS_PATH + 'modules/o-table-row-links' );

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var sandbox;
var tableDom;
var linkDom;
var linkRowCellDom;
var nonLinkRowCellDom;

var HTML_SNIPPET =
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
  var event = document.createEvent( 'Event' );
  event.initEvent( 'click', true, true );
  target.dispatchEvent( event );
}


describe( 'o-table-row-links', function() {
  jsdom();
  beforeEach( function() {
    var windowLocation;
    sandbox = sinon.sandbox.create();

    document.body.innerHTML = HTML_SNIPPET;
    tableDom = document.querySelector( '.o-table__row-links' );
    linkDom = tableDom.querySelector( 'a' );
    linkRowCellDom = tableDom.querySelector( '.linkRowCell' );
    nonLinkRowCellDom = tableDom.querySelector( '.nonLinkRowCell' );

    Object.defineProperty( window, 'location', {
      get: function() { return windowLocation; },
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

  afterEach( function() {
    sandbox.restore();
  } );

  it( 'should navigate to new location when link row cell clicked', function() {
    triggerClickEvent( linkRowCellDom );
    expect( window.location ).to.equal( 'http://www.example.info' );
  } );

  it( 'should bubble click events to the parent element when a link is clicked',
  function() {
    triggerClickEvent( linkDom );
    expect( window.location ).to.equal( 'http://www.example.info' );
  } );

  it( 'should not navigate to new location when non link row cell clicked',
  function() {
    triggerClickEvent( nonLinkRowCellDom );
    expect( window.location ).to.equal( 'http://www.example.com' );
  } );
} );
