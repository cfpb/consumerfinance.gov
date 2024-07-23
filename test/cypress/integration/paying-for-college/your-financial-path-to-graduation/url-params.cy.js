import { PfcFinancialPathToGraduation } from './financial-path-helpers.cy.js';

const page = new PfcFinancialPathToGraduation();

describe('Your Financial Path to Graduation (url parameter functionality)', () => {
  beforeEach(() => {
    cy.visit(
      '/paying-for-college/your-financial-path-to-graduation/?iped=163286&pid=4502-3&houp=onCampus&typp=bachelors&prop=0&lenp=3&ratp=inState&depp=dependent&cobs=n&tuit=10595&hous=12809&diro=13&book=1250&indo=55&tran=44&pelg=11&seog=12&fedg=13&stag=14&schg=15&tuig=16&othg=17&mta=18&gi=19&othm=20&stas=21&schs=22&oths=23&wkst=33&subl=299&unsl=399&insl=599&insr=0.06&insf=0.02&stal=499&star=0.05&staf=0.01&npol=699&npor=0.07&npof=0.03&pers=81&fams=82&529p=83&offj=84&onj=85&eta=86&othf=87&houx=31&fdx=32&clhx=33&trnx=34&hltx=35&entx=36&retx=37&taxx=38&chcx=39&dbtx=40&othx=41&prin=48k-75k',
    );
  });

  it('should set the first page correctly', () => {
    cy.get('#search__school-input').should(
      'have.value',
      'University of Maryland-College Park',
    );
    cy.get('input[name="programType"]:checked').should(
      'have.value',
      'bachelors',
    );
    cy.get('input[name="programLength"]:checked').should('have.value', '3');
    cy.get('input[name="programHousing"]:checked').should(
      'have.value',
      'onCampus',
    );
    cy.get('input[name="programDependency"]:checked').should(
      'have.value',
      'dependent',
    );
    cy.get('#program-select option:checked').should('have.value', '4502-3');
    cy.get('#program-select option:checked').should(
      'contain',
      "Bachelor's degree - Anthropology",
    );
    cy.get('#program-income').should('have.value', '48k-75k');
  });

  it('should have the correct cost values', () => {
    page.nextToSchoolCosts();
    cy.get('span[data-financial-item="total_costOfProgram"]').should(
      'contain',
      '$51,447',
    );

    page.clickLeftNav('review-plan');

    cy.get('p[data-financial-item="total_costs"]').should('contain', '$17,149');
    cy.get('p[data-financial-item="total_funding"]').should('contain', '$842');
    cy.get('p[data-financial-item="debt_totalAtGrad"]').should(
      'contain',
      '$55,239',
    );
    cy.get('p[data-financial-item="debt_tenYearInterest"]').should(
      'contain',
      '$11,026',
    );
    cy.get('p[data-financial-item="debt_tenYearMonthly"]').should(
      'contain',
      '$552',
    );
  });
});
