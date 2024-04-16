import { DynamicDisclosures } from './disclosures-helpers.cy.js';

const page = new DynamicDisclosures();
const apiConstants =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/constants/';
const apiSchoolOne =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/school/133465/';
const apiProgramOne =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/program/133465_5287/';
const apiSchoolTwo =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/school/224776/';
const apiProgramTwo =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/program/224776_444/';

describe('Dynamic Disclosures', () => {
  const urlOne =
    '/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=133465&pid=5287&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&totl=45000&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8&leng=30';
  const urlTwo =
    '/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=224776&pid=444&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&totl=45000&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8&leng=30';

  beforeEach(() => {
    cy.intercept('GET', apiConstants, (req) => {
      req.reply({
        fixture: 'paying-for-college/constants.json',
      });
    });
    cy.intercept('GET', apiSchoolOne, (req) => {
      req.reply({
        fixture: 'paying-for-college/school-133465.json',
      });
    });
    cy.intercept('GET', apiSchoolTwo, (req) => {
      req.reply({
        fixture: 'paying-for-college/school-224776.json',
      });
    });
    cy.intercept('GET', apiProgramOne, (req) => {
      req.reply({
        fixture: 'paying-for-college/program-133465_5287.json',
      });
    });
    cy.intercept('GET', apiProgramTwo, (req) => {
      req.reply({
        fixture: 'paying-for-college/program-224776_444.json',
      });
    });
    cy.visit(urlOne);
  });

  it("should automatically populate the program length if it's available", () => {
    cy.get('#estimated-years-attending option:checked').should(
      'have.value',
      '2.5',
    );
  });

  /* Note: this item was removed from the settlement version of the code, and thus
      it may no longer be relevant */
  it("should dynamically display the completion rate if it's available", () => {
    page.confirmVerification();
    page.stepTwo();
    cy.get('[data-metric="gradRate"]').should((elem) => {
      expect(elem).to.contain('17%');
    });
  });

  it("should dynamically display the expected monthly salary if it's available", () => {
    page.confirmVerification();
    page.stepTwo();
    cy.get('.estimated-expenses [data-financial="monthlySalary"]').should(
      'be.visible',
    );
    cy.get('.estimated-expenses [data-financial="monthlySalary"]').should(
      'contain',
      '2,783',
    );
  });

  it("should dynamically display the job rate if it's available", () => {
    cy.visit(urlTwo);

    page.confirmVerification();
    page.stepTwo();
    cy.get('#criteria_job-placement-rate').should('contain', '91');
  });

  /* Currently, grad cohort (completionCohort) display is not available in the app.
     Here is a test for it, in case that ever changes */
  // xit('should dynamically display the graduation cohort content if it\'s available', () => {
  //   page.confirmVerification();
  //   page.stepTwo();
  //   cy.get('.content__grad-cohort').should('be.visible');
  // })

  it("should dynamically hide the graduation cohort content if it's not available", () => {
    page.confirmVerification();
    page.stepTwo();
    cy.get('.content__grad-cohort').should('not.be.visible');
  });
});
