import subscriptionSuccessResponse from '../../../fixtures/subscription.json';

export class EmailSignup {
  open() {
    cy.visit('/about-us/blog/');
  }

  signUp(email) {
    cy.get('.o-email-signup form').within(() => {
      cy.get('input:first').type(email);
      cy.get('button:first').click();
    });
  }

  interceptGovDeliveryAPIRequests() {
    cy.intercept(
      {
        url: '/subscriptions/new/',
      },
      (request) => {
        request.reply(subscriptionSuccessResponse);
      },
    ).as('subscriptionSuccess');
  }

  successNotification() {
    return cy.get('.m-notification__message');
  }
}
