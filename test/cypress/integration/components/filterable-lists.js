import { FilterableList } from '../../components/filterable-lists';

const filterableList = new FilterableList();

describe( 'Filterable List', () => {
  it( 'should display filters when opened', () => {
    filterableList.open();
    filterableList.showFilters();
    filterableList.filterForm().should( 'be.visible' );
  } );
  it( 'should apply filters to the results', () => {
    filterableList.selectFilter( 'Consumer complaint' );
    filterableList.applyFilters();
    filterableList.filterNotification().should( 'be.visible' );
    filterableList.clearFilters();
  } );
  it( 'should filter by date-range', () => {
    filterableList.open();
    filterableList.showFilters();
    filterableList.filterForm().should( 'be.visible' );
    filterableList.setFromDate( '2010-01-01' );
    filterableList.setToDate( '2020-01-01' );
    filterableList.applyFilters();
    filterableList.filterNotification().should( 'be.visible' );
  } );
  it( 'should filter by topics', () => {
    filterableList.open();
    filterableList.showFilters();
    filterableList.selectTopic( 'Open government' );
    filterableList.selectedTopics().should( 'be.visible' );
    filterableList.applyFilters();
    filterableList.filterNotification().should( 'be.visible' );
  } );
} );
