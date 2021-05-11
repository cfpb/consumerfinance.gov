import ClearableInput from '../../../../cfgov/unprocessed/js/modules/ClearableInput.js';
import { simulateEvent } from '../../../util/simulate-event.js';

let baseDom;
let clearBtnDom;
let inputDom;

const HTML_SNIPPET = `
<div class="o-form__input-w-btn_input-container">
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
</div>
`;

describe( 'ClearableInput', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    baseDom = document.querySelector( '.o-form__input-w-btn_input-container' );
    inputDom = baseDom.querySelector( 'input' );
    clearBtnDom = baseDom.querySelector( '.input-contains-label_after__clear' );
  } );

  describe( 'init function', () => {
    it( 'should hide the clear button when a value is empty', () => {
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).toStrictEqual( true );
    } );

    it( 'should display the clear button when a value is present', () => {
      inputDom.value = 'testing init function';
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).toStrictEqual( false );
    } );
  } );

  describe( 'on clear button click', () => {
    it( 'should hide itself', () => {
      inputDom.value = 'testing clear button';
      new ClearableInput( baseDom ).init();
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).toStrictEqual( false );
      simulateEvent( 'mousedown', clearBtnDom );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).toStrictEqual( true );
    } );

    it( 'should clear the input value', () => {
      inputDom.value = 'testing clear button';
      new ClearableInput( baseDom ).init();
      simulateEvent( 'mousedown', clearBtnDom );
      expect( inputDom.value ).toStrictEqual( '' );
    } );
  } );

  describe( 'on input keystroke', () => {
    it( 'should show the clear button, if value present', () => {
      new ClearableInput( baseDom ).init();

      // Event code 65 is the `a` character.
      simulateEvent( 'keyup', inputDom, { keyCode: 65 } );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).toStrictEqual( false );
    } );

    it( 'should hide the clear button, if value not present', () => {
      new ClearableInput( baseDom ).init();

      // Event code 8 is backspace.
      simulateEvent( 'keyup', inputDom, { keyCode: 65 } );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).toStrictEqual( false );
      simulateEvent( 'keyup', inputDom, { keyCode: 8 } );
      expect( clearBtnDom.classList.contains( 'u-hidden' ) ).toStrictEqual( true );
    } );
  } );

} );
