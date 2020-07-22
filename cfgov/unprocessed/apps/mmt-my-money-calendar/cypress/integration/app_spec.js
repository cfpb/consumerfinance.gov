describe('myMoneyCalendar E2E testing', () => {
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

  it('Steps through the get started wizard', () => {
    cy.visit('http://localhost:8000/mmt-my-money-calendar')

    cy.get('.a-btn')
      .contains('Get Started')
      .click()
    
    cy.url()
      .should('include', '/money-on-hand/sources')

    cy.contains('Money on Hand')

    cy.get('.a-label')
      .contains('Checking Account')
      
    cy.contains('Checking Account')
      .click()

    cy.get('.a-btn')
      .contains('Next')
      .click()
  })
})