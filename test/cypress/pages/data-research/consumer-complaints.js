export class ConsumerComplaints {

  click( name ) {
    cy.get( '.btn' ).contains( name ).click();
  }

  clickTab( name ) {
    cy.get( `.${name}` ).click();
  }

  clickDateRange( name ) {
    cy.get( `.range-${name}` ).click();
  }

  clickButton( name ) {
    cy.get( '.a-btn' ).contains( name ).click();
  }

  chartSize( height, width) {
    cy.get( '.cfpb-chart' ).should( 'be.visible' )
      .and(chart => {
        expect(chart.height()).to.be.equal(height);
        expect(chart.width()).to.be.equal(width);
    });
  }

  clickTile( name ) {
    const tile = name.toUpperCase();
    return cy.get( `.tile-${tile}` ).click();
  }

  checkState( name ) {
    return cy.get( `.highcharts-name-${name}`.toLowerCase() );
  }

  checkChart( name ) {
    return cy.get( '.highcharts-tracker' ).should( 'contain', name );
  }

  checkLegend( name ) {
    return cy.get( `.highcharts-legend-${name}` );
  }

  enter( term ) {
    cy.get( '#searchText.a-text-input' ).type( term );
  }

  search() {
    cy.get( '.a-btn.flex-fixed' ).click();
  }

  searchSummary() {
    return cy.get( '#search-summary' );
  }

}
