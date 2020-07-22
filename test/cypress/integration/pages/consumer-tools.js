import { PlanningSocialSecurity } from '../../pages/consumer-tools/planning-social-security';
import { FinancialWellBeing } from '../../pages/consumer-tools/financial-well-being';

const planningSocialSecurity = new PlanningSocialSecurity();
const financialWellBeing = new FinancialWellBeing();

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
      cy.url().should( 'include', 'es' );
    } );
  } );
  describe( 'Financial Well Being', () => {
    it( 'should provide a survey', () => {
      financialWellBeing.open();
      financialWellBeing.selectQuestion( 1, 'Completely' );
      financialWellBeing.selectQuestion( 2, 'Very Well' );
      financialWellBeing.selectQuestion( 3, 'Somewhat' );
      financialWellBeing.selectQuestion( 4, 'Very Little' );
      financialWellBeing.selectQuestion( 5, 'Not At All' );
      financialWellBeing.selectQuestion( 6, 'Completely' );
      financialWellBeing.selectQuestion( 7, 'Often' );
      financialWellBeing.selectQuestion( 8, 'Sometimes' );
      financialWellBeing.selectQuestion( 9, 'Rarely' );
      financialWellBeing.selectQuestion( 10, 'Never' );
      financialWellBeing.selectAge();
      financialWellBeing.submitButton().should( 'be.enabled' );
      financialWellBeing.submit();
      financialWellBeing.score().should( 'be.visible' );
    } );
  } );
} );
