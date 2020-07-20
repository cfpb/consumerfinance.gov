import EmailSignup from '../../components/email-signup';

const page = new EmailSignup();

describe( 'Email Sign Up', () => { // Component
  it( 'Should Accept a valid email and return a success message', () => { // Test
    // Arrange
    page.open();
    // Act
    page.signUp( 'testing@cfpb.gov' );
    // Assert
    page.successNotification().should( 'exist' );
    page.successNotification().contains( 'Your submission was successfully received.' );
  } );
} );
