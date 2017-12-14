const BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const sinon = require( 'sinon' );
const ClearableInput = require( BASE_JS_PATH + 'modules/ClearableInput' );
let sandbox;
let baseDom;
let clearBtnDom;
let inputDom;

const HTML_SNIPPET =
  `<div class="o-form__input-w-btn_input-container">
       <div class="m-btn-inside-input
                   input-contains-label">
           <label for="query" class="input-contains-label_before
                                     input-contains-label_before__search">
           </label>
           <label for="query" class="input-contains-label_after
                                     input-contains-label_after__clear">
           </label>
           <input type="text"
                  title="Search the CFPB"
                  class="a-text-input"
                  value=""
                  placeholder="Search the CFPB">
       </div>
   </div>`;

function triggerEvent( target, eventType, eventOption ) {
  const event = document.createEvent( 'Event' );
  if ( eventType === 'keyup' ) {
    event.keyCode = eventOption || '';
  }
  event.initEvent( eventType, true, true );
  target.dispatchEvent( event );
}

describe( 'ClearableInput', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )( HTML_SNIPPET );
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    baseDom = document.querySelector( '.o-form__input-w-btn_input-container' );
    inputDom = baseDom.querySelector( 'input' );
    clearBtnDom = baseDom.querySelector( '.input-contains-label_after__clear' );
  } );

  afterEach( () => {
    sandbox.restore();
  } );

  describe( 'init function', () => {
    it( 'should hide the clear button when a value is empty', () => {
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( true );
    } );

    it( 'should display the clear button when a value is present', () => {
      inputDom.value = 'testing init function';
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
    } );
  } );

  describe( 'on clear button click', () => {
    it( 'should hide itself', () => {
      inputDom.value = 'testing clear button';
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
      triggerEvent( clearBtnDom, 'mousedown' );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( true );
    } );

    it( 'should clear the input value', () => {
      inputDom.value = 'testing clear button';
      new ClearableInput( baseDom ).init();
      triggerEvent( clearBtnDom, 'mousedown' );
      expect( inputDom.value ).to.equal( '' );
    } );
  } );

  describe( 'on input keystroke', () => {
    it( 'should show the clear button, if value present', () => {
      new ClearableInput( baseDom ).init();

      // Event code 65 is the `a` character.
      triggerEvent( inputDom, 'keyup', 65 );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
    } );

    it( 'should hide the clear button, if value not present', () => {
      new ClearableInput( baseDom ).init();

      // Event code 8 is backspace.
      triggerEvent( inputDom, 'keyup', 65 );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( false );
      triggerEvent( inputDom, 'keyup', 8 );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).to.equal( true );
    } );
  } );

} );
