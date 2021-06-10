import { Filter } from '../../components/filter';
import { FilterableListControl } from '../../components/filterable-list-control';

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
    filterableList.firstResultContent().should( 'be.visible' );
    filterableList.lastResultContent().should( 'be.visible' );
    // And I should see page results
    filterableList.resultsContent().its( 'length' ).should( 'be.gt', 0 );
  } );
  it( 'Browse filterable page', () => {
    // When I goto a browse filterable page
    cy.visit( '/rules-policy/final-rules/' );
    // But I do not select a filter
    cy.url().should( 'not.include', '?' );
    // Then open the filterable list controls.
    filterableList.open();
    // Then I should not see filtered results
    filterableList.notification().should( 'not.be.visible' );
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
    filterableList.firstResultContent().should( 'be.visible' );
    filterableList.lastResultContent().should( 'be.visible' );
    // And I should see page results
    filterableList.resultsContent().should( 'contain', 'rule' );
    filterableList.resultsContent().its( 'length' ).should( 'be.gt', 0 );
  } );
} );
