import ConsumerTools from '../pages/consumer_tools';

let page = new ConsumerTools();

describe('Consumer Tools', () => {
    it('Should have an email sign up', () => {
        // Arrange
        page.open();
        page.stubSubscriptionResponse();
        //Act
        page.signUp('testing@cfpb.gov');
        // Assert
        page.successNotification().should('exist');
        page.successNotification().contains('Your submission was successfully received.')
    });
});