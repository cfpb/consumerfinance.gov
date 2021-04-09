export class CCTCharts {
  open() {
    cy.visit( '/data-research/consumer-credit-trends/auto-loans/origination-activity/' );
  }

  getFirstButton( range ) {
    return cy.get( `g[aria-label="Select range ${ range }"]` ).first();
  }
}
