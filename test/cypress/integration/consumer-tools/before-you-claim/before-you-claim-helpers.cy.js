import retirementAPIResponseUnder50 from '../../../fixtures/retirement-api-under50.json';
import retirementAPIResponseOver50 from '../../../fixtures/retirement-api-over50.json';
import retirementAPIResponseOver70 from '../../../fixtures/retirement-api-over70.json';

export class BeforeYouClaim {
  open() {
    cy.visit('/consumer-tools/retirement/before-you-claim/');
  }

  setBirthDate(month, day, year) {
    cy.get('#bd-month').type(month);
    cy.get('#bd-day').type(day);
    cy.get('#bd-year').type(year);
  }

  setHighestAnnualSalary(salary) {
    cy.get('#salary-input').type(salary);
  }

  enterAge(age) {
    const year = 2024;
    this.setBirthDate('1', '1', String(year - age));
    this.setHighestAnnualSalary('115000');
    this.getEstimate();
  }

  enterAgeUnder50() {
    this.enterAge(43);
  }

  enterAgeOver50() {
    this.enterAge(65);
  }

  enterAgeOver70() {
    this.enterAge(71);
  }

  interceptRetirementAPIRequests() {
    cy.intercept(
      {
        url: '/consumer-tools/retirement/retirement-api/estimator/1-1-1981/**',
      },
      (request) => {
        request.reply(retirementAPIResponseUnder50);
      },
    ).as('retirementAPIResponseUnder50');

    cy.intercept(
      {
        url: '/consumer-tools/retirement/retirement-api/estimator/1-1-1959/**',
      },
      (request) => {
        request.reply(retirementAPIResponseOver50);
      },
    ).as('retirementAPIResponseOver50');

    cy.intercept(
      {
        url: '/consumer-tools/retirement/retirement-api/estimator/1-1-1953/**',
      },
      (request) => {
        request.reply(retirementAPIResponseOver70);
      },
    ).as('retirementAPIResponseOver70');
  }

  getEstimate() {
    cy.get('#get-your-estimates').click();
  }

  claimGraph() {
    return cy.get('#claim-canvas');
  }

  setLanguageToSpanish() {
    return cy
      .get('.content-l')
      .first()
      .within(() => {
        cy.get('a').first().click();
      });
  }
}
