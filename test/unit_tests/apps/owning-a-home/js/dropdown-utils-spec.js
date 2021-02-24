import
dropDownUtils
  from '../../../../../cfgov/unprocessed/apps/owning-a-home/js/dropdown-utils.js';

const HTML_SNIPPET = `
<div class="foo">
  <select id="foo">
    <option value="baz"></option>
  </select>
</div>
`;

let dropDownDom;
let containerDom;

/**
 * @param {HTMLNode} dropDown - The select HTML element to search for options.
 * @returns {NodeList} All the options inside the drop-down select menu.
 */
function getOptions( dropDown ) {
  return dropDown.querySelectorAll( 'option' );
}

/**
 * @param {HTMLNode} dropDown - The select HTML element to search for options.
 * @returns {NodeList} All the disabled options inside the drop-down select menu.
 */
function getOptionsDisabled( dropDown ) {
  return dropDown.querySelectorAll( 'option:disabled' );
}

/**
 * @param {HTMLNode} divDom - The HTML element to query.
 * @returns {Array} List of classes on 'foo' div.
 */
function getDivClassList( divDom ) {
  return divDom.classList;
}

describe( 'Dropdown utils', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    containerDom = document.querySelector( '.foo' );
    dropDownDom = containerDom.querySelector( '#foo' );
  } );

  it( 'should complain if you don\'t specify a target', () => {
    expect( dropDownUtils ).toThrow();
  } );

  it( 'should disable dropdowns', () => {
    dropDownUtils( 'foo' ).disable();
    expect( dropDownDom.getAttribute( 'disabled' ) ).toBe( 'disabled' );
  } );

  it( 'should enable dropdowns', () => {
    dropDownUtils( 'foo' ).disable();
    dropDownUtils( 'foo' ).enable();
    expect( dropDownDom.getAttribute( 'disabled' ) ).toBeNull();
  } );

  it( 'should add options to dropdowns', () => {
    dropDownUtils( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    dropDownUtils( 'foo' ).addOption( { label: 'foo1', value: 'bar1' } );
    dropDownUtils( 'foo' ).addOption( { label: 'foo2', value: 'bar2' } );
    expect( getOptions( dropDownDom ).length ).toBe( 4 );
  } );

  it( 'should not add options with same values', () => {
    dropDownUtils( 'foo' ).addOption( { label: 'first', value: 'bar' } );
    dropDownUtils( 'foo' ).addOption( { label: 'second', value: 'bar' } );
    expect( getOptions( dropDownDom ).length ).toBe( 2 );
  } );

  it( 'should select the option when values.select is true', () => {
    dropDownUtils( 'foo' ).addOption(
      { label: 'Foo', value: 'BAR', select: 1 }
    );
    expect( dropDownDom.selectedIndex ).toBe( 1 );
  } );

  it( 'should create option with value/name of ""', () => {
    dropDownUtils( 'foo' ).addOption( null );
    dropDownDom[0].selectedIndex = 1;
    expect( dropDownDom[dropDownDom[0].selectedIndex].value ).toBe( '' );
  } );

  it( 'should disable all given options', () => {
    dropDownUtils( 'foo' ).addOption( { value: 'value1', label: 'label1' } );
    dropDownUtils( 'foo' ).addOption( { value: 'value2', label: 'label2' } );
    expect( getOptionsDisabled( dropDownDom ).length ).toBe( 0 );
    dropDownUtils( 'foo' ).disable( [ 'value1', 'value2' ] );
    expect( getOptionsDisabled( dropDownDom ).length ).toBe( 2 );
  } );

  it( 'should select several select elements', () => {
    document.body.innerHTML += '<select id="foo1"><option value="baz1"></option></select>';
    document.body.innerHTML += '<select id="foo2"><option value="baz1"></option></select>';
    dropDownUtils( [ 'foo', 'foo2' ] ).disable();
    expect( document.querySelectorAll( 'select :disabled' ).length ).toBe( 2 );
    dropDownUtils( [ 'foo', 'foo1', 'foo2' ] ).enable();
    expect( document.querySelectorAll( 'select :enabled' ).length ).toBe( 3 );
    expect( document.querySelectorAll( 'select :disabled' ).length ).toBe( 0 );
  } );

  it( 'should let methods be chainable', () => {
    dropDownUtils( 'foo' ).addOption(
      { label: 'foo', value: 'bar' }
    ).addOption(
      { label: 'foo1', value: 'bar1' }
    ).addOption(
      { label: 'foo2', value: 'bar2' }
    );
    expect( getOptions( dropDownDom ).length ).toBe( 4 );
  } );

  it( 'should remove options from dropdowns', () => {
    dropDownUtils( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    dropDownUtils( 'foo' ).addOption( { label: 'foo1', value: 'bar1' } );
    dropDownUtils( 'foo' ).removeOption( 'bar1' );
    expect( getOptions( dropDownDom ).length ).toBe( 2 );
  } );

  it( 'should complain if you try to remove ' +
      'an option without specifying a value', () => {
    expect( dropDownUtils( 'foo' ).removeOption ).toThrow();
  } );

  it( 'should complain if you try to check ' +
      'an option without specifying a value', () => {
    expect( dropDownUtils( 'foo' ).hasOption ).toThrow();
  } );

  it( 'should report if a dropdown has an option', () => {
    dropDownUtils( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    expect( dropDownUtils( 'foo' ).hasOption( 'bar' ) ).toBe( true );
  } );

  it( 'should reset a dropdown', () => {
    dropDownUtils( 'foo' ).addOption( { label: 'foo', value: 'bar' } );
    dropDownDom.selectedIndex = 1;
    dropDownUtils( 'foo' ).reset();
    expect( dropDownDom.selectedIndex ).not.toBe( 1 );
  } );

  it( 'should hide a dropdown', () => {
    dropDownUtils( 'foo' ).hide();
    expect( getDivClassList( containerDom ).contains( 'u-hidden' ) )
      .toBe( true );
  } );

  it( 'should show a dropdown', () => {
    dropDownUtils( 'foo' ).hide();
    dropDownUtils( 'foo' ).show();
    expect( getDivClassList( containerDom ).contains( 'u-hidden' ) )
      .toBe( false );
  } );

  it( 'should show loading', () => {
    dropDownUtils( 'foo' ).showLoadingAnimation();
    expect( getDivClassList( containerDom ).contains( 'loading' ) )
      .toBe( true );
  } );

  it( 'should hide loading', () => {
    dropDownUtils( 'foo' ).showLoadingAnimation();
    dropDownUtils( 'foo' ).hideLoadingAnimation();
    expect( getDivClassList( containerDom ).contains( 'loading' ) )
      .toBe( false );
  } );

  it( 'should highlight the dropdown', () => {
    dropDownUtils( 'foo' ).showHighlight();
    expect( getDivClassList( containerDom ).contains( 'highlight-dropdown' ) )
      .toBe( true );
  } );

  it( 'should unhighlight the dropdown', () => {
    dropDownUtils( 'foo' ).showHighlight();
    dropDownUtils( 'foo' ).hideHighlight();
    expect( getDivClassList( containerDom ).contains( 'highlight-dropdown' ) )
      .toBe( false );
  } );
} );
