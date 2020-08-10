export class CCTCharts {
  open() {
    cy.visit( '/data-research/consumer-credit-trends/auto-loans/origination-activity/' );
  }

  selectTimeRange( range ) {
    cy.get( `g[aria-label="Select range ${ range }"]` ).first().click();
  }

  currentTimeRange() {
    return cy.get( '.highcharts-button-pressed' ).first().find( 'text' );
  }
}
