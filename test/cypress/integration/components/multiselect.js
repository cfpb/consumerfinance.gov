import { Multiselect } from '../../components/multiselect';

let multiselect;

describe( 'I should be able to select using the multiselect', () => {
  beforeEach( () => {
    cy.visit( '/about-us/blog/' );
    multiselect = new Multiselect( 'Topic' );
  } );
  it( 'State on page load', () => {
    // Then the multiselect should be rendered
    multiselect.isRendered();
    // But no tags should be selected
    multiselect.displayedTag().should( 'have.length', 0 );
    // And the multiselect dropdown shouldn't be visible
    multiselect.fieldSet().should( 'not.be.visible' );
  } );
  it( 'Search input click', () => {
    // When I click on the multiselect search input
    multiselect.clickSearchInput();
    // Then the multiselect dropdown should be visible
    multiselect.fieldSet().should( 'be.visible' );
  } );
  it( 'Search input focus', () => {
    // When I focus on the multiselect search input
    multiselect.searchInput().focus();
    // Then the multiselect dropdown should be visible
    multiselect.fieldSet().should( 'be.visible' );
  } );
  it( 'Search input blur', () => {
    // When I focus on the multiselect search input
    multiselect.searchInput().focus();
    // And I click away from the search input
    multiselect.clickAway();
    // Then the multiselect dropdown shouldn't be visible
    multiselect.fieldSet().should( 'not.be.visible' );
    // And the multiselect dropdown length should be 0
    multiselect.dropDown().should( 'have.length', 0 );
  } );
  it( 'Typing in search input, returning matched results', () => {
    // When I enter "students" in the search input
    multiselect.enterSearchInput( 'students' );
    // Then the multiselect dropdown should display "students"
    multiselect.dropDownHasValue( 'students' );
    // And the multiselect dropdown length should be 1
    multiselect.dropDown().should( 'have.length', 1 );
  } );
  it( 'Typing in search input, not returning unmatched results', () => {
    // When I enter "students" in the search input
    multiselect.enterSearchInput( 'students' );
    // Then the multiselect dropdown shouldn't display "mortgages"
    multiselect.dropDownValue( 'mortgages' ).should( 'have.length', 0 );
    // And the multiselect dropdown length should be 1
    multiselect.dropDown().should( 'have.length', 1 );
  } );
  it( 'Typing in search input, clearing the input and closing results', () => {
    // When I enter "students" in the search input
    multiselect.searchInput().type( 'students' );
    // And I hit the escape button on the search input
    multiselect.searchInput().type( '{esc}' );
    // Then the multiselect dropdown shouldn't be visible
    multiselect.fieldSet().should( 'not.be.visible' );
    // And the multiselect dropdown length should be 0
    multiselect.dropDown().should( 'have.length', 0 );
    // And the options field shouldn't contain the class "filtered"
    multiselect.optionsField().should( 'not.have.class', 'filtered' );
  } );
  it( 'Typing in search input, highlighting the first item', () => {
    // When I click on the multiselect search input
    multiselect.clickSearchInput();
    // And I hit the down arrow on the multiselect
    multiselect.enterSearchInput( '{downarrow}' );
    // Then the first option should be highlighted
    multiselect.dropDownLabel().first().should( 'be.visible' );
  } );
  it( 'Interacting with options list, adding option to choices', () => {
    // When I click on the multiselect search input
    multiselect.clickSearchInput();
    // And I click on the first option in the dropdown
    multiselect.dropDownLabelClick();
    // Then the choices element should contain the first option
    multiselect.firstChoicesElement();
    // And the choices element length should be 1
    multiselect.choicesElement().should( 'have.length', 1 );
  } );
  it( 'Interacting with choices list, remove an option from choices', () => {
    // When I click on the multiselect search input
    multiselect.clickSearchInput();
    // And I click on the first option in the dropdown
    multiselect.dropDownLabelClick();
    // And I click on the first choices element
    multiselect.choicesElementClick();
    // Then the choices element length should be 0
    multiselect.choicesElement().should( 'have.length', 0 );
  } );
  it( 'Interacting with options list, removing option from choices', () => {
    // When I click on the multiselect search input
    multiselect.clickSearchInput();
    // And I click on the first option in the dropdown
    multiselect.dropDownLabelClick();
    // And I click on the first option in the dropdown again
    multiselect.dropDownLabelClick();
    // Then the choices element length should be 0
    multiselect.choicesElement().should( 'have.length', 0 );
  } );
} );
