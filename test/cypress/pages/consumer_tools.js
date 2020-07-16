export default class ConsumerTools {
    
    constructor() {}
    
    open() {
        cy.visit('/consumer-tools/');
    }

    signUp(email) {
        cy.get('.o-form__email-signup').within(() => {
            cy.get('input:first').type(email);
            cy.get('button:first').click();
        });
    }

    stubSubscriptionResponse() {
        cy.server()           // enable response stubbing
        cy.route({
            method: 'POST',      
            url: '/subscriptions/new/',
            response: 'fixtures:subscription.json'
        });
    }

    successNotification() {
        return cy.get('.m-notification_message');
    }
}