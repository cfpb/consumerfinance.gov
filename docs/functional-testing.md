# Functional Testing with Cypress

In order to ensure that as we upgrade our wagtail/django dependencies our backend python code is still functional from a frontend perspective we are integrating a new browser testing tool [Cypress](https://www.cypress.io). The goal is to implement and maintain a testing suite that enables confidence in dependency upgrades. 

## Installing Cypress

We have included Cypress as a dependency of this project, and so the only steps that need to be taken are doing a fresh `yarn` if you haven't already.

## Running Cypress

We support both a headless docker container to execute our cypress tests as well as the already installed desktop application that comes packaged with cypress. The test files are located in the `test/cypress/integration/` directory.

* To run the docker container execute `docker-compose -f docker-compose.e2e.yml run e2e`
  - If you have not previously set up a local Docker network, you will need to stop any running consumerfinance.gov Docker containers, run `docker network create cfgov`, start the containers again, and then run the above command.

* To run the desktop cypress aplication execute `yarn run cypress open` and select your test file to execute.

* To run the tests from the commandline you can also invoke them via `yarn run cypress run`. You can read more about different command line arguments in the [Command-Line Documentation](https://docs.cypress.io/guides/guides/command-line.html#Options) provided by Cypress.

* To run the tests against a server other than `http://localhost:8000`, you can pass in an override for the `baseUrl` config value; for example:`yarn run cypress open --config baseUrl=http://staging_url`.

## Writing Cypress Tests

When developing new tests for Cypress it is important to consider what the test is trying to accomplish. We want to ensure that we are not polluting our cypress tests with things that can be tested at another level, we are seeking to only test the integration aspect of our UI hosted via Wagtail/Django and custom python code within our backend.

When adding a test it is often helpful to separate the arrange/act code from the actual assertions in order to improve the readability of our testing code. To do this we have adopted the page model of testing, where we define a page within the application and the methods of interacting with the page separate from the test file itself where we define the assertions. 

For example consider the ConsumerTools Page:

```javascript
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
    successNotification() {
        return cy.get('.m-notification_message');
    }
}
```

Notice how this class defines functions to retrieve and modify elements on the page but in a more human readable manner. This allows our test file for consumer tools to look like:

```javascript
import ConsumerTools from '../pages/consumer_tools';

let page = new ConsumerTools();

describe('Consumer Tools', () => {
    it('Should have an email sign up', () => {
        // Arrange
        page.open();
        // Act
        page.signUp('testing@cfpb.gov');
        // Assert
        page.successNotification().should('exist');
        page.successNotification().contains('Your submission was successfully received.')
    });
});
```

Overall it lets our tests show what is intended to be happening on a page without showing the more technical side of how we reference and interact with elements.
