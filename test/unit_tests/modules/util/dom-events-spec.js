'use strict';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
var domEvents = require( BASE_JS_PATH + 'modules/util/dom-events' );
var input;
var clicked;

describe( 'Dom Events bindEvent', function() {
  jsdom();

  beforeEach( function() {
    input = document.createElement( 'input' );
    input.type = 'checkbox';
    input.value = 'test-bind-event';
    clicked = false;
  } );

  it( 'should not update the var until event is triggered', function() {
    domEvents.bindEvent( input, {
      click: function() { clicked = true; }
    } );
    expect( clicked ).to.be.false;
  } );

  it( 'should not update the var if another event is triggered',
    function() {
      domEvents.bindEvent( input, {
        click: function() { clicked = true; }
      } );
      input.focus();
      expect( clicked ).to.be.false;
    }
  );

  it( 'should update the var when the event is triggered',
    function() {
      domEvents.bindEvent( input, {
        click: function() { clicked = true; }
      } );
      input.click();
      expect( clicked ).to.be.true;
    }
  );
} );
