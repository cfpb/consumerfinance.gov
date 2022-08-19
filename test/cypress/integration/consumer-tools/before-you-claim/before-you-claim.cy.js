import { BeforeYouClaim } from './before-you-claim-helpers.cy.js';

const claim = new BeforeYouClaim();

describe( 'Planning your Social Security', () => {
  beforeEach( () => {
    claim.open();
  } );

  it( 'should display estimated benefits', () => {
    claim.setBirthDate( '1', '1', '1980' );
    claim.setHighestAnnualSalary( '115000' );
    claim.getEstimate();
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
