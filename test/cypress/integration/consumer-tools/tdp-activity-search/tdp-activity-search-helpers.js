export class ActivitySearch {

  open() {
    cy.visit( '/consumer-tools/educator-tools/youth-financial-education/teach/activities/' );
  }

  toggleFilter( label ) {
    cy.get( '.content_sidebar' ).within( () => {
      cy.contains( label ).click();
    } );
  }

  selectFilter( name, value ) {
    cy.get( `input[name="${ name }"][value="${ value }"]` ).check( { force: true } );
  }

  clearFilters() {
    return cy.get( '.results_filters-clear' );
  }

  resultsFilterTag( filterName ) {
    return cy.get( `[data-value="#building-block--${ filterName }"]` );
  }

  resultsCountEmpty() {
    return cy.get( '.results_count__empty' );
  }

  search( term ) {
    cy.get( '#search-text' ).type( term );
    cy.get( 'form[action="."]' ).within( () => {
      cy.get( 'button' ).first().click();
    } );
  }

}
