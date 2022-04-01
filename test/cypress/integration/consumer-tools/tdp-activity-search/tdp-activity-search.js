import { expect } from 'chai';
import { ActivitySearch } from './tdp-activity-search-helpers';
const $ = Cypress.$;

const search = new ActivitySearch();

describe( 'Activity Search', () => {
  it( 'should filter results', () => {
    const resultsFilterText = 'financial-habits-and-norms';
    search.open();
    search.selectFilter( 'Financial habits and norms' );
    search.clearFilters().should( 'be.visible' );
    search.resultsFilterTag( resultsFilterText ).should( 'be.visible' );
  } );
  it( 'should clear results filters', () => {
    const resultsFilterText = 'financial-habits-and-norms';
    search.open();
    search.selectFilter( 'Financial habits and norms' );
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
  it( 'should have ordered National standards', () => {
    search.open();
    cy.get( 'input[name="council_for_economic_education"]' ).then( $inputs => {
      // Intentionally allowing up to 10 standards as long as they're ordered
      const ordering = [
        'I.',
        'II.',
        'III.',
        'IV.',
        'V.',
        'VI.',
        'VII.',
        'VIII.',
        'IX.',
        'X.'
      ];
      $inputs.each( ( idx, el ) => {
        expect( el.getAttribute( 'aria-label' ) ).to.contain( ordering[idx] );
      } );
    } );
  } );
} );
