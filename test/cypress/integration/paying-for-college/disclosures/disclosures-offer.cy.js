import { DynamicDisclosures } from './disclosures-helpers.cy.js';

const page = new DynamicDisclosures();
const apiConstants =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/constants/';
const apiSchoolOne =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/school/133465/';
const apiProgramOne =
  '/paying-for-college2/understanding-your-financial-aid-offer/api/program/133465_5287/';

describe('Dynamic Disclosures offer page', () => {
  const urlOne =
    '/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=133465&pid=5287&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&totl=45000&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8&leng=30';

  beforeEach(() => {
    cy.intercept('GET', apiConstants, {
      host: 'localhost',
      fixture: 'paying-for-college/constants.json',
    });
    cy.intercept('GET', apiSchoolOne, {
      host: 'localhost',
      fixture: 'paying-for-college/school-133465.json',
    });
    cy.intercept('GET', apiProgramOne, {
      host: 'localhost',
      fixture: 'paying-for-college/program-133465_5287.json',
    });
    cy.visit(urlOne);
  });

  it('should display the verify offer area and no other sections', () => {
    cy.get('.verify__wrapper').should('be.visible');
    cy.get('.review').should('not.be.visible');
    cy.get('.evaluate').should('not.be.visible');
    cy.get('.get-options').should('not.be.visible');
  });

  it('should display the anticipated total direct cost section if passed in the URL', () => {
    cy.get('#verify_totalDirectCost').should('be.visible');
  });

  it('should hide the anticipated total direct cost section if not passed in the URL', () => {
    cy.visit(
      'http://localhost:8000/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=133465&pid=5287&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8',
    );
    cy.get('#verify_totalDirectCost').should('not.be.visible');
  });

  it('should hide the anticipated total direct cost section if the passed URL value is 0', () => {
    cy.visit(
      'http://localhost:8000/paying-for-college2/understanding-your-financial-aid-offer/offer/?iped=133465&pid=5287&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&totl=0&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8',
    );
    cy.get('#verify_totalDirectCost').should('not.be.visible');
  });

  it('should let a student verify their information and go on to Step 1 of the offer', () => {
    page.confirmVerification();
    // cy.get('.verify_controls').should('not.be.visible');
    cy.get('section[data-section="review"]').should('be.visible');
    cy.get('section[data-section="evaluate"]').should('not.be.visible');
    cy.get('.get-options').should('not.be.visible');
  });

  it('should let a student report incorrect aid offer information', () => {
    page.denyVerification();
    cy.get('section[data-section="review"]').should('not.be.visible');
    cy.get('section[data-section="evaluate"]').should('not.be.visible');
    cy.get('.get-options').should('not.be.visible');
    cy.get('.instructions__content--wrong').should('be.visible');
  });

  it('should let a student edit the tuition and fees', () => {
    page.confirmVerification();
    cy.get('#costs__tuition').should('not.be.disabled');
  });
});
