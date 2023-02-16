import { EmailSignup } from './email-signup-helpers.cy.js';

const page = new EmailSignup();

describe('Email Sign Up', () => {
  it('Should Accept a valid email and return a success message', () => {
    // Arrange
    page.open();
    page.interceptGovDeliveryAPIRequests();
    // Act
    page.signUp('testing@cfpb.gov');
    cy.wait('@subscriptionSuccess');
    // Assert
    page
      .successNotification()
      .should('exist')
      .and('include.text', 'Your submission was successfully received.');
  });
});
