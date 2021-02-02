import { FilterableListControl } from '../../components/filterable-list-control';
import { Filter } from '../../components/filter';

const filterableList = new FilterableListControl();
const filter = new Filter();

describe( 'Filterable Page shows all results when no filter selected', () => {
  it( 'Sublanding filterable page', () => {
    // When I goto a sublanding filterable page
    cy.visit( '/about-us/blog/' );
    // But I do not select a filter
    cy.url().should( 'not.include', '?' );
    // Then I should not see filtered results
    filterableList.notification().should( 'not.be.visible' );
    // Then I should see the (first|last) page result
    filterableList.firstResult().should( 'be.visible' );
    filterableList.lastResult().should( 'be.visible' );
    // And I should see page results
    filterableList.results().its( 'length' ).should( 'be.gt', 0 );
  } );
  it( 'Browse filterable page', () => {
    // When I goto a browse filterable page
    cy.visit( '/rules-policy/final-rules/' );
    // But I do not select a filter
    cy.url().should( 'not.include', '?' );
    // Then I should not see filtered results
    filterableList.notification().should( 'not.be.visible' );
    // And I open the filterable list control
    filterableList.open();
    // When I select the first checkbox in the Category list
    filter.checkCategoryId( 'interim-final-rule' );
    // When I select a checkbox in the Topic list
    filter.clickTopic( 'Rulemaking' );
    // When I enter "01/01/2017" in the From date entry field
    filterableList.filterFromDate( '2017-01-01' );
    // And I enter "01/01/2018" in the To date entry field
    filterableList.filterToDate( '2018-01-01' );
    // And I apply filters
    filterableList.applyFilters();
    // Then I should see filtered results
    filterableList.notification().should( 'be.visible' );
    // Then I should see the (first|last) page result
    filterableList.firstResult().should( 'be.visible' );
    filterableList.lastResult().should( 'be.visible' );
    // And I should see page results
    filterableList.results().should( 'contain', 'rule');
    filterableList.results().its( 'length' ).should( 'be.gt', 0 );
  } );
} );
