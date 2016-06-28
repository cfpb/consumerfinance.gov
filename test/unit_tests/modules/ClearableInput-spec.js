'use strict';
var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var ClearableInput = require( BASE_JS_PATH + 'modules/ClearableInput' );
var sandbox;
var baseDom;
var clearBtnDom;
var inputDom;

var HTML_SNIPPET =
  '<div class="input-with-btn_input input-contains-label">' +
    '<label for="query" class="input-contains-label_before ' +
            'input-contains-label_before__search">' +
    '</label>' +
    '<label for="query" class="input-contains-label_after ' +
            'input-contains-label_after__clear">' +
    '</label>' +
    '<input type="text" id="query" name="query" value=""' +
    'placeholder="Search the CFPB">' +
  '</div>';

function triggerEvent( target, eventType, eventOption ) {
  var event = document.createEvent( 'Event' );
  if ( eventType === 'keyup' ) {
    event.keyCode = eventOption || '';
  }
  event.initEvent( eventType, true, true );
  target.dispatchEvent( event );
}


describe( 'ClearableInput', function() {
  jsdom();

  beforeEach( function() {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    baseDom = document.querySelector( '.input-with-btn_input' );
    inputDom = baseDom.querySelector( 'input' );
    clearBtnDom = baseDom.querySelector( '.input-contains-label_after__clear' );
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  describe( 'init function', function() {
    it( 'should hide the clear button when a value is empty', function() {
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( true );
    } );

    it( 'should display the clear button when a value is present', function() {
      inputDom.value = 'testing init function';
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
    } );
  } );

  describe( 'on clear button click', function() {
    it( 'should hide itself', function() {
      inputDom.value = 'testing clear button';
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
      triggerEvent( clearBtnDom, 'mousedown' );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( true );
    } );

    it( 'should clear the input value', function() {
      inputDom.value = 'testing clear button';
      new ClearableInput( baseDom ).init();
      triggerEvent( clearBtnDom, 'mousedown' );
      expect( inputDom.value ).to.equal( '' );
    } );
  } );

  describe( 'on input keystroke', function() {
    it( 'should show the clear button, if value present', function() {
      new ClearableInput( baseDom ).init();

      // Event code 65 is the `a` character.
      triggerEvent( inputDom, 'keyup', 65 );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
    } );

    it( 'should hide the clear button, if value not present', function() {
      new ClearableInput( baseDom ).init();

      // Event code 8 is backspace.
      triggerEvent( inputDom, 'keyup', 65 );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
      triggerEvent( inputDom, 'keyup', 8 );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( true );
    } );
  } );

} );
