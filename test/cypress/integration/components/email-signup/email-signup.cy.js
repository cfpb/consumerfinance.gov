import EmailSignup from './email-signup-helpers.cy.js';

const page = new EmailSignup();

describe( 'Email Sign Up', () => {
  it( 'Should Accept a valid email and return a success message', () => {
    // Arrange
    page.open();
    // Act
    page.signUp( 'testing@cfpb.gov' );
    // Let the request process
    cy.wait( 500 );
    // Assert
    page.successNotification().should( 'exist' );
    page.successNotification().contains( 'Your submission was successfully received.' );
  } );
} );
