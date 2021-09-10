import { Feedback } from './feedback-helpers';

const feedback = new Feedback();

describe( 'Feedback', () => {
  it( 'Should submit feedback', () => {
    feedback.open();
    feedback.submitComment( 'This is a test comment' );
    feedback.successNotification().should( 'be.visible' );
  } );
} );
