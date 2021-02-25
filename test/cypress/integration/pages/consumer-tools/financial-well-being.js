import {
  FinancialWellBeing
} from '../../../pages/consumer-tools/financial-well-being';

const financialWellBeing = new FinancialWellBeing();

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
