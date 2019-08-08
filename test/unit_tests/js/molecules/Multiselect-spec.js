import Multiselect from '../../../../cfgov/unprocessed/js/molecules/Multiselect';

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
      multiselectDom = document.querySelectorAll( '.o-multiselect' );

      expect( selectDom.length ).toBe( 0 );
      expect( multiselectDom.length ).toBe( 1 );

      expect( multiselect.init() ).toBeInstanceOf( Multiselect );
    } );

    it( 'should autocheck any selected options (form submitted pages)', () => {
      const option = document.querySelector( 'option' );
      option.defaultSelected = true;
      multiselect.init();
      const choices = document.querySelectorAll( '.o-multiselect_choices li' );

      expect( choices.length ).toBe( 1 );
      expect( choices[0].innerHTML ).toContain( 'Debt collection' );
    } );
  } );

  describe( 'public methods', () => {
    it( 'should open when the expand method is called', () => {
      multiselect.init();
      multiselect.expand();
      multiselectDom = document.querySelector( '.o-multiselect' );
      const fieldset = multiselectDom.querySelector(
        '.o-multiselect_fieldset'
      );

      expect( multiselectDom.className ).toBe( 'o-multiselect u-active' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'false' );
    } );

    it( 'should close when the collapse method is called', () => {
      multiselect.init();
      multiselect.expand();
      multiselect.collapse();
      multiselectDom = document.querySelector( '.o-multiselect' );
      const fieldset = multiselectDom.querySelector(
        '.o-multiselect_fieldset'
      );

      expect( multiselectDom.className ).toBe( 'o-multiselect' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'true' );
    } );
  } );

  describe( 'interactions', () => {
    it( 'should highlight the first item when keying down', function() {
      multiselect.init();
      const search = document.querySelector( '#test-select' );
      search.click();
      simulateEvent( 'keydown', search, { keyCode: 40 } );

      expect( document.activeElement.id ).toBe( 'Debt collection' );
    } );

    xit( 'should open when the search input is clicked', function() {
      multiselect.init();
      multiselectDom = document.querySelector( '.o-multiselect' );
      const fieldset = multiselectDom.querySelector(
        '.o-multiselect_fieldset'
      );
      const search = document.querySelector( '#test-select' );
      search.click();

      expect( document.activeElement.id ).toBe( 'test-select' );
      expect( multiselectDom.className ).toBe( 'o-multiselect u-active' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'false' );
    } );

    xit( 'should close when the body is clicked', function() {
      multiselect.init();
      multiselect.expand();
      multiselectDom = document.querySelector( '.o-multiselect' );
      const fieldset = multiselectDom.querySelector(
        '.o-multiselect_fieldset'
      );
      document.click();

      expect( multiselectDom.className ).toBe( 'o-multiselect' );
      expect( fieldset.getAttribute( 'aria-hidden' ) ).toBe( 'true' );
    } );
  } );
} );
