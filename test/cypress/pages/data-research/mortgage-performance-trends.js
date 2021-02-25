export class MortgagePerformanceTrends {

  open() {
    cy.visit(
      '/data-research/mortgage-performance-trends/' +
      'mortgages-30-89-days-delinquent/'
    );
  }

  selectLocationType( location ) {
    const id = `#mp-line-chart_geo-${ location.split( ' ' ).slice( 0, 1 ).join( '' ) }`.toLowerCase();
    cy.get( id ).click( { force: true } );
  }

  selectStateForDelinquencyTrends( state ) {
    cy.get( '#mp-line-chart-state' ).select( state );
  }

  selectStateForDelinquencyRatesPerMonth( state ) {
    cy.get( '#mp-map-state' ).select( state );
  }

  selectMonth( month ) {
    cy.get( '#mp-map-month' ).select( month );
  }

  selectYear( year ) {
    cy.get( '#mp-map-year' ).select( year );
  }

  mapTitle() {
    return cy.get( '#mp-map-title' );
  }

}
