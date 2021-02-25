import { BeforeYouClaim } from '../../../pages/consumer-tools/before-you-claim';

const claim = new BeforeYouClaim();

describe( 'Planning your Social Security', () => {
  it( 'should display esxtimated benefits', () => {
    claim.open();
    claim.setBirthDate( '1', '1', '1980' );
    claim.setHighestAnnualSalary( '115000' );
    claim.getEstimate();
    claim.claimGraph().should( 'be.visible' );
  } );
  it( 'should have a spanish view', () => {
    claim.open();
    claim.setLanguageToSpanish();
    cy.url().should( 'include', 'es' );
  } );
} );
