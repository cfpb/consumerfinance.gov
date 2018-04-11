const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const Multiselect = require( BASE_JS_PATH + 'molecules/Multiselect' );

import { simulateEvent } from '../../../util/simulate-event';

let multiselect;
let selectDom;
let multiselectDom;

const HTML_SNIPPET = `
  <select name="test-select" id="test-select" multiple>
    <option value="Debt collection">Debt collection</option>
    <option value="consumers-responses">Consumer&#39;s Responses</option>
    <option value="Mortgage disclosure">Mortgage disclosure</option>
    <optgroup label="All other topics">
  </select>
`;

describe( 'Multiselect', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;

    selectDom = document.querySelector( 'select[multiple]' );
    multiselect = new Multiselect( selectDom );
  } );

  describe( 'init()', () => {
    it( 'should initialize the Multiselect', () => {
      multiselect.init();
      selectDom = document.querySelectorAll( 'select[multiple]' );
      multiselectDom = document.querySelectorAll( '.cf-multi-select' );

      expect( selectDom.length ).toBe( 0 );
      expect( multiselectDom.length ).toBe( 1 );
    } );

    it( 'should autocheck any selected options (form submitted pages)', () => {
      const option = document.querySelector( 'option' );
      option.defaultSelected = true;
      multiselect.init();
      const choices =
          document.querySelectorAll( '.cf-multi-select_choices li' );

      expect( choices.length ).toBe( 1 );
      expect( choices[0].innerHTML ).toContain( 'Debt collection' );
    }
    );

    it( 'should log a helpful tip if passed a bad option value', () => {

      /* TODO: Remove console.log in favor of throwing an error. */
      const consoleSpy = jest.spyOn( window.console, 'log' );
      const option = document.querySelector( 'option' );
      option.value = 'Foo\'';
      multiselect.init();
      selectDom = document.querySelectorAll( 'select[multiple]' );
      multiselectDom = document.querySelectorAll( '.cf-multi-select' );

      expect( selectDom.length ).toBe( 1 );
      expect( multiselectDom.length ).toBe( 0 );
      expect( consoleSpy ).toHaveBeenCalledTimes( 1 );
      expect( consoleSpy ).toHaveBeenCalledWith( '\'Foo\'\' is not a valid value' );
    } );
  } );

  describe( 'public methods', () => {
    it( 'should open when the expand method is called', () => {
      multiselect.init();
      multiselect.expand();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      const fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );

      expect( multiselectDom.className ).toBe( 'cf-multi-select active' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'false' );
    } );

    it( 'should close when the collapse method is called', () => {
      multiselect.init();
      multiselect.expand();
      multiselect.collapse();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      const fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );

      expect( multiselectDom.className ).toBe( 'cf-multi-select' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'true' );
    } );
  } );

  describe( 'interactions', () => {
    xit( 'should open when the search input is clicked', function() {
      multiselect.init();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      const fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );
      const search = document.querySelector( '#test-select' );
      search.click();

      expect( document.activeElement.id ).toBe( 'test-select' );
      expect( multiselectDom.className ).toBe( 'cf-multi-select active' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'false' );
    } );

    xit( 'should highlight the first item when keying down', function() {
      multiselect.init();
      const search = document.querySelector( '#test-select' );
      search.click();
      simulateEvent( 'keydown', search, { keyCode: 40 } );

      expect( document.activeElement.id ).toBe( 'Debt collection' );
    } );

    xit( 'should close when the body is clicked', function() {
      multiselect.init();
      multiselect.expand();
      multiselectDom = document.querySelector( '.cf-multi-select' );
      const fieldset =
        multiselectDom.querySelector( '.cf-multi-select_fieldset' );
      document.click();

      expect( multiselectDom.className ).toBe( 'cf-multi-select' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'true' );
    } );
  } );
} );
