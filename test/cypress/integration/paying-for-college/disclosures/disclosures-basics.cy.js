import { DynamicDisclosures } from './disclosures-helpers.cy.js';

const page = new DynamicDisclosures();
const apiConstants = '/paying-for-college2/understanding-your-financial-aid-offer/api/constants/';
const apiSchoolOne = '/paying-for-college2/understanding-your-financial-aid-offer/api/school/133465/';
const apiProgramOne = '/paying-for-college2/understanding-your-financial-aid-offer/api/program/133465_5287/'
const apiSchoolTwo = '/paying-for-college2/understanding-your-financial-aid-offer/api/school/224776/';
const apiProgramTwo = '/paying-for-college2/understanding-your-financial-aid-offer/api/program/224776_444/';

describe('Dynamic Disclosures', () => {
  const urlOne = '/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=133465&pid=5287&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&totl=45000&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8&leng=30';
  const urlTwo = '/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=224776&pid=444&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&totl=45000&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8&leng=30';
  
  beforeEach(() => {
    cy.intercept( 'GET', apiConstants, {host: 'localhost', fixture: 'paying-for-college/constants.json'}).as('intConstants');
    cy.intercept( 'GET', apiSchoolOne, {host: 'localhost', fixture: 'paying-for-college/school-133465.json'}).as('intSchoolOne');
    cy.intercept( 'GET', apiSchoolTwo, {host: 'localhost', fixture: 'paying-for-college/school-224776.json'}).as('intSchoolTwo');
    cy.intercept( 'GET', apiProgramOne, {host: 'localhost', fixture: 'paying-for-college/program-133465_5287.json'}).as('intProgramOne');
    cy.intercept( 'GET', apiProgramTwo, {host: 'localhost', fixture: 'paying-for-college/program-224776_444.json'}).as('intProgramTwo');
    cy.visit( urlOne );
  });


  it( 'should properly update when the tuition and fees are modified', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    page.setText('costs__tuition','40000');
    cy.get('#summary_total-cost').should(
      'contain',
      '34,550'
    );
  });

  it( 'should properly update when any costs fields are modified', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    // Initial check
    cy.get('#summary_cost-of-attendance').should(
      'contain',
      '43,626'
    );
    cy.get('#summary_total-cost').should(
      'contain',
      '33,526'
    );
    // Change all values
    page.setText('costs__room-and-board','5000');
    page.setText('costs__books','1234');
    page.setText('costs__transportation','2300');
    page.setText('costs__other','999');
    cy.get('#summary_cost-of-attendance').should(
      'contain',
      '48,509'
    );
    cy.get('#summary_total-cost').should(
      'contain',
      '38,409'
    );
  });

  it( 'should properly update when any grants fields are modified', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    // Initial check
    cy.get('#summary_cost-of-attendance').should(
      'contain',
      '43,626'
    );
    cy.get('#summary_total-cost').should(
      'contain',
      '33,526'
    );
    // Change all values
    page.setText('grants__school','3000');
    page.setText('grants__state','3001');
    page.setText('grants__scholarships','103');
    page.setText('grants__military','123');
    page.setText('grants__gi','999');
    // Check new values
    cy.get('#summary_cost-of-attendance').should(
      'contain',
      '43,626'
    );
    cy.get('#summary_total-grants-scholarships').should(
      'contain',
      '7,226'
    );
    cy.get('#summary_total-cost').should(
      'contain',
      '36,400'
    );
  });

  it( 'should properly calculate borrowing totals', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    cy.get('#summary_total-loans').should('contain', '7,200');
  });

  it( 'should properly re-calculate borrowing totals when editted', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    page.setText('contrib__unsubsidized','4000');
    page.setText('contrib__direct-plus','4000');
    page.setText('contrib__private-loan_0','2000');
    page.setText('contrib__payment-plan','2500');
    cy.get('#summary_total-loans').should('contain','11,000');
  });

  it( 'should properly update when the cash a student will personally provide is modified', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    page.setText('contrib__savings','2500');
    cy.get('#summary_total-contributions').should('contain','20,500');
  });

  it( 'should properly update when the cash a student\'s family will provide is modified', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    page.setText('contrib__family','9999');
    cy.get('#summary_total-contributions').should('contain','13,999');
  });

  it( 'should properly update when the Parent PLUS loan is modified', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    page.setText('contrib__parent-plus','4000');
    cy.get('#summary_total-contributions').should('contain','21,000');
  });

  it( 'should properly update when the work study earnings are modified', () => {
    cy.wait(['@intConstants', '@intSchoolOne', '@intProgramOne']);
    page.confirmVerification();
    page.stepTwo();
    page.setText('contrib__workstudy','1250');
    cy.get('#summary_total-contributions').should('contain','16,250');
  });
});
