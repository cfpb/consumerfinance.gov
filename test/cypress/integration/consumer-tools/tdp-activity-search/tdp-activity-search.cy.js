import { ActivitySearch } from './tdp-activity-search-helpers.cy.js';
const $ = Cypress.$;

const search = new ActivitySearch();

describe( 'Activity Search', () => {
  it( 'should filter results', () => {
    search.open();
    search.toggleFilter( 'National standards' );
    search.selectFilter( 'council_for_economic_education', '1' );
    cy.url().should( 'include', 'council_for_economic_education=1' );

    const resultsFilterText = 'financial-habits-and-norms';
    search.open();
    search.toggleFilter( 'Building block' );
    search.selectFilter( 'building_block', '2' );
    cy.url().should( 'include', 'building_block=2' );

    search.clearFilters().should( 'be.visible' );
    search.resultsFilterTag( resultsFilterText ).should( 'be.visible' );
  } );
  it( 'should clear results filters', () => {
    const resultsFilterText = 'financial-habits-and-norms';
    search.open();
    search.toggleFilter( 'Building block' );
    search.selectFilter( 'building_block', '2' );
    search.resultsFilterTag( resultsFilterText ).should( 'be.visible' );
    search.clearFilters().click();
    search.resultsFilterTag( resultsFilterText ).should( 'not.exist' );
  } );
  it( 'should show no search results when no results', () => {
    search.open();
    search.search( 'notaword' );
    search.resultsCountEmpty().should( 'be.visible' );
  } );
  it( 'should limit results by search query', () => {
    search.open();
    search.search( 'money' );
    cy.url().should( 'include', 'money' );
  } );
  it( 'should place topics filters above school subject', () => {
    search.open();
    cy.window().then( () => {
      const t = $( '[name="topic"]' )[0];
      const ss = $( '[name="school_subject"]' )[0];
      const compared = t.compareDocumentPosition( ss );
      expect( compared & Node.DOCUMENT_POSITION_FOLLOWING ).not.eq( 0 );
    } );
  } );
  it( 'should place Building blocks and standards in Activity characteristics', () => {
    search.open();
    cy.get( '.filter-section__third' ).contains( 'Building block' )
      .should( 'be.visible' ).should( 'have.class', 'o-expandable_target__collapsed' );
    cy.get( '.filter-section__third' ).contains( 'National standards' )
      .should( 'be.visible' ).should( 'have.class', 'o-expandable_target__collapsed' );
  } );
  it( 'should have ordered Activity characteristics', () => {
    search.open();
    cy.get( '.filter-section__third button .h4' ).then( $buttons => {
      const ordering = [
        'Activity duration',
        'Activity type',
        "Bloom's Taxonomy level",
        'Building block',
        'National standards',
        'Teaching strategy'
      ];
      expect( $buttons.length ).to.eq( ordering.length );
      $buttons.each( ( idx, el ) => {
        expect( el.textContent.trim() ).to.eq( ordering[idx] );
      } );
    } );
  } );
} );
