describe('myMoneyCalendar E2E testing', () => {

  beforeEach(() => {
    cy.clearLocalStorage()
    indexedDB.deleteDatabase('myMoneyCalendar')
  })

  it('Arrives at landing page', () => {
    cy.visit('http://localhost:8000/mmt-my-money-calendar')

    cy.url()
      .should('include', '/money-on-hand')

    cy.get('.m-hero_image')
      .find('img')
      .should('have.attr', 'src')
      .should('include', 'mmt-my-money-calendar')

    cy.contains('Get Started')
  })

  it('Can move back between screens', () => {
    cy.visit('http://localhost:8000/mmt-my-money-calendar')

    cy.get('.a-btn')
      .contains('Get Started')
      .click()
    
    cy.url()
      .should('include', '/money-on-hand/sources')

    cy.contains('Money on Hand')
      
    cy.contains('Checking Account')
      .click()

    cy.get('.a-btn')
      .contains('Next')
      .click()

    cy.url()
      .should('include', '/balances/checking')

    cy.get('.a-btn')
      .contains('Back')
      .click()

    cy.url()
      .should('include', '/money-on-hand/sources')
  })

  it('Steps through the get started wizard', () => {
    cy.visit('http://localhost:8000/mmt-my-money-calendar')

    cy.get('.a-btn')
      .contains('Get Started')
      .click()
    
    cy.url()
      .should('include', '/money-on-hand/sources')

    cy.contains('Money on Hand')
      
    cy.contains('Checking Account')
      .click()

    cy.get('.a-btn')
      .contains('Next')
      .click()

    cy.url()
      .should('include', '/balances/checking')

    cy.get('#checking')
      .type('40000')
      .should('have.value', '400.00')

    cy.get('.a-btn')
      .contains('Next')
      .click()

    cy.url()
      .should('include', '/money-on-hand/summary')

    cy.get('.funding-source__name')
      .contains('Checking Account')

    cy.get('.funding-source__balance')
      .contains('$400.00')

    cy.get('p')
      .contains('Total Starting Balance: $400.00')

    cy.get('.a-btn')
      .contains('Go to Calendar')
      .click()

    cy.url()
      .should('include', '/calendar')
  })
})