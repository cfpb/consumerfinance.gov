import { PlanningSocialSecurity } from '../../pages/consumer-tools/planning-social-security';

const planningSocialSecurity = new PlanningSocialSecurity();

describe( 'Consumer Tools', () => {
  describe( 'Planning your Social Security', () => {
    it( 'should display esxtimated benefits', () => {
      planningSocialSecurity.open();
      planningSocialSecurity.setBirthDate( '1', '1', '1980' );
      planningSocialSecurity.setHighestAnnualSalary( '115000' );
      planningSocialSecurity.getEstimate();
      planningSocialSecurity.claimGraph().should( 'be.visible' );
    } );
    it( 'should have a spanish view', () => {
      planningSocialSecurity.open();
      planningSocialSecurity.setLanguageToSpanish();
      cy.url().should('include', 'es')
    } );
  } );
} );
