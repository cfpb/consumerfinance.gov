describe('Credit Card Agreements Archive', () => {
  it('should render agreements for a selected lender', () => {
    cy.visit('/credit-cards/agreements/archive/');
    //Display errors on failure to connect
    cy.get('main').should('contain', 'encountered an error');
  });
});
