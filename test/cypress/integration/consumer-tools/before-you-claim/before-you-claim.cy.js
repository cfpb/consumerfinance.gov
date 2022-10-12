import { BeforeYouClaim } from './before-you-claim-helpers.cy.js';

const claim = new BeforeYouClaim();

describe( 'Planning your Social Security', () => {
  beforeEach( () => {
    claim.open();

    /* Return a fixture for the retirement API for a birthdate of 1/1/1980
    and a highest annual salary of $115,000 */
    claim.interceptRetirementAPIRequests();
  } );

  it( 'should display estimated benefits', () => {
    claim.setBirthDate( '1', '1', '1980' );
    claim.setHighestAnnualSalary( '115000' );
    claim.getEstimate();
    cy.wait( '@retirementAPIResponse' );
    claim.claimGraph().should( 'be.visible' );
  } );

  it( 'should have a spanish view', () => {
    cy.intercept( '/consumer-tools/retirement/before-you-claim/es' )
      .as( 'getSpanish' );
    claim.setLanguageToSpanish();
    cy.wait( '@getSpanish' );
    cy.url().should( 'contain', '/es' );
  } );
} );
