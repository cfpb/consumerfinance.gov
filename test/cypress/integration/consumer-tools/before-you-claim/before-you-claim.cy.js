import { BeforeYouClaim } from './before-you-claim-helpers.cy.js';

const claim = new BeforeYouClaim();

//***********************************************************/
//****** Values to iterate through answers w/ multi-answers */
let lsQuestions;
let qOne;
let qTwo;
let qThree;
let qFour;
let qFive;
let qSix;

describe('Planning your Social Security', () => {
  beforeEach(() => {
    claim.open();

    /* Return a fixture for the retirement API for a birthdate of 1/1/1980
    and a highest annual salary of $115,000 */
    claim.interceptRetirementAPIRequests();
  });

  //*******************************************/
  //**********Language Selection***************/
  it('should have a spanish view', () => {
    cy.intercept(
      '/es/herramientas-del-consumidor/jubilacion/antes-de-solicitar/',
    ).as('getSpanish');
    claim.setLanguageToSpanish();
    cy.wait('@getSpanish');
    cy.url().should('contain', '/es');
  });

  it('should display tool tip in step one after clicking svg tip icon', () => {
    cy.get('#claiming-social-security #tooltip-container').should(
      'not.be.visible',
    );
    cy.get(
      '#claiming-social-security #step-one-form .cf-icon-svg--help-round',
    ).click();
    cy.get('#claiming-social-security #tooltip-container').should('be.visible');
  });

  it('should show error if user is over the age of 70', () => {
    claim.enterAgeOver70();
    cy.get(
      '#claiming-social-security #step-one-form .m-notification--warning',
    ).should('be.visible');
  });

  it('should display estimated benefits', () => {
    claim.enterAgeUnder50();
    claim.claimGraph().should('be.visible');
    cy.get('#claiming-social-security #graph-container .learn-how a').should(
      'have.attr',
      'href',
      '/consumer-tools/retirement/before-you-claim/about/',
    );
  });

  //*********************************************************/
  //*** Check to see if each bar is showing on the graph ****/
  it('should display all bars in the graph', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security #claim-canvas .graph--bar').each(
      (elem) => {
        cy.wrap(elem).should('not.have.css', 'height', '0px');
      },
    );
  });

  it('should only display bars >= age 65 in the graph', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security #claim-canvas .graph--bar').each(
      (elem, index) => {
        switch (index) {
          case 0:
          case 1:
          case 2:
            cy.wrap(elem).should('have.css', 'height', '0px');
            break;
          case 3:
          case 4:
          case 5:
          case 6:
          case 7:
          case 8:
            cy.wrap(elem).should('not.have.css', 'height', '0px');
            break;
        }
      },
    );
  });

  //*************************************************/
  // Testing answers to "Are you married" question in step 2
  it('show correct lifestyle response to yes button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-married .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();

    lsQuestions = cy.get(
      '#claiming-social-security .question-married .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne.should('have.attr', 'data-responds-to', 'yes').and('be.visible');

    qTwo = lsQuestions.next();
    qTwo.should('have.attr', 'data-responds-to', 'no').and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'widowed')
      .and('not.be.visible');
  });

  it('show correct lifestyle response to no button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-married .lifestyle-btn.a-btn')
      .contains('No')
      .click();

    lsQuestions = cy.get(
      '#claiming-social-security .question-married .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne.should('have.attr', 'data-responds-to', 'yes').and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo.should('have.attr', 'data-responds-to', 'no').and('be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'widowed')
      .and('not.be.visible');
  });

  it('show correct lifestyle response to widowed button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-married .lifestyle-btn.a-btn')
      .contains('Widowed')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-married .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne.should('have.attr', 'data-responds-to', 'yes').and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo.should('have.attr', 'data-responds-to', 'no').and('not.be.visible');

    qThree = lsQuestions.next();
    qThree.should('have.attr', 'data-responds-to', 'widowed').and('be.visible');
  });

  // //*************************************************/
  // //Testing answers to "Do you plan to continue working" question in step 2 (under 50)
  it('show correct under 50 working age response to yes button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-working .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-working .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct under 50 working age response to no button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-working .lifestyle-btn.a-btn')
      .contains('No')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-working .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct under 50 working age response to not sure button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-working .lifestyle-btn.a-btn')
      .contains('Not Sure')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-working .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  //************************************************************************************/
  // //Testing answers to "Do you plan to continue working" question in step 2 (over 50)
  it('show correct over 50 working age response to yes button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-working .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-working .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct over 50 working age response to no button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-working .lifestyle-btn.a-btn')
      .contains('No')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-working .lifestyle-response',
    );

    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct over 50 working age response to not sure button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-working .lifestyle-btn.a-btn')
      .contains('Not Sure')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-working .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('be.visible');
  });

  //*************************************************/
  //Testing answers to "Will your expenses decrease" question in step 2 (under 50)
  it('show correct under 50 decreased expenses response to yes button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-expenses .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-expenses .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct under 50 decreased expenses response to no button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-expenses .lifestyle-btn.a-btn')
      .contains('No')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-expenses .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct under 50 decreased expenses response to not sure button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-expenses .lifestyle-btn.a-btn')
      .contains('Not Sure')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-expenses .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  // //*************************************************/
  // //Testing answers to "Will your expenses decrease" question in step 2 (over 50)
  it('show correct over 50 decreased expenses response to yes button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-expenses .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-expenses .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct over 50 decreased expenses response to no button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-expenses .lifestyle-btn.a-btn')
      .contains('No')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-expenses .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct over 50 decreased expenses response to not sure button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-expenses .lifestyle-btn.a-btn')
      .contains('Not Sure')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-expenses .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('be.visible');
  });

  //*************************************************/
  // //Testing answers to "...additional sources of retirement income" question in step 2 (under 50)
  it('show correct under 50 additional income response to yes button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-income .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-income .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct under 50 additional income response to no button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-income .lifestyle-btn.a-btn')
      .contains('No')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-income .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct under 50 additional income response to not sure button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-income .lifestyle-btn.a-btn')
      .contains('Not Sure')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-income .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  // //*************************************************/
  // //Testing answers to "...additional sources of retirement income" question in step 2 (over 50)
  it('show correct over 50 additional income response to yes button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-income .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-income .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct over 50 additional income response to no button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-income .lifestyle-btn.a-btn')
      .contains('No')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-income .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('not.be.visible');
  });

  it('show correct over 50 additional income response to not sure button', () => {
    claim.enterAgeOver50();
    cy.get('#claiming-social-security .question-income .lifestyle-btn.a-btn')
      .contains('Not Sure')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-income .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne
      .should('have.attr', 'data-responds-to', 'yes-under50')
      .and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo
      .should('have.attr', 'data-responds-to', 'yes-over50')
      .and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'no-under50')
      .and('not.be.visible');

    qFour = lsQuestions.next();
    qFour
      .should('have.attr', 'data-responds-to', 'no-over50')
      .and('not.be.visible');

    qFive = lsQuestions.next();
    qFive
      .should('have.attr', 'data-responds-to', 'notsure-under50')
      .and('not.be.visible');

    qSix = lsQuestions.next();
    qSix
      .should('have.attr', 'data-responds-to', 'notsure-over50')
      .and('be.visible');
  });

  //***********************************************************/
  //Testing answers to "...live a long life" question in step 2
  it('show correct longevity response to yes button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-longevity .lifestyle-btn.a-btn')
      .contains('Yes')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-longevity .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne.should('have.attr', 'data-responds-to', 'yes').and('be.visible');

    qTwo = lsQuestions.next();
    qTwo.should('have.attr', 'data-responds-to', 'no').and('not.be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'notsure')
      .and('not.be.visible');
  });

  it('show correct longevity response to no button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-longevity .lifestyle-btn.a-btn')
      .contains('No')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-longevity .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne.should('have.attr', 'data-responds-to', 'yes').and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo.should('have.attr', 'data-responds-to', 'no').and('be.visible');

    qThree = lsQuestions.next();
    qThree
      .should('have.attr', 'data-responds-to', 'notsure')
      .and('not.be.visible');
  });

  it('show correct longevity response to not sure button', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security .question-longevity .lifestyle-btn.a-btn')
      .contains('Not Sure')
      .click();
    lsQuestions = cy.get(
      '#claiming-social-security .question-longevity .lifestyle-response',
    );
    qOne = lsQuestions.first();
    qOne.should('have.attr', 'data-responds-to', 'yes').and('not.be.visible');

    qTwo = lsQuestions.next();
    qTwo.should('have.attr', 'data-responds-to', 'no').and('not.be.visible');

    qThree = lsQuestions.next();
    qThree.should('have.attr', 'data-responds-to', 'notsure').and('be.visible');
  });

  //*************************************************************/
  //Step 3: Learn your next steps - Retirement age qualifications
  it('should have correct dropdown values', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security #retirement-age-selector').select('70');
    cy.get('#claiming-social-security .age-response-value').should(
      'contain',
      '70',
    );
  });

  it('should have correct max retirement qualification', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security #retirement-age-selector').select('70');
    cy.get('#claiming-social-security .next-steps_max').should(
      'contain',
      'which is your maximum',
    );
  });

  it('should have correct late retirement qualification', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security #retirement-age-selector').select('68');
    cy.get('#claiming-social-security .next-steps_over').should(
      'contain',
      'which is later',
    );
  });

  it('should have correct exact retirement qualification', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security #retirement-age-selector').select('67');
    cy.get('#claiming-social-security .next-steps_equal').should(
      'contain',
      'which is your',
    );
  });

  it('should have correct early retirement qualification', () => {
    claim.enterAgeUnder50();
    cy.get('#claiming-social-security #retirement-age-selector').select('66');
    cy.get('#claiming-social-security .next-steps_under').should(
      'contain',
      'which is earlier',
    );
  });

  it('should contain link to the external SSA website', () => {
    claim.enterAgeUnder50();
    cy.get(
      '#claiming-social-security #age-selector-response li.next-step-one a',
    ).should('have.attr', 'href', 'https://www.ssa.gov/myaccount/');
  });
});
