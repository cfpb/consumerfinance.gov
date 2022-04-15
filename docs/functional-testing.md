# Functional Testing with Cypress

We use [Cypress](https://www.cypress.io) for functional testing. Our functional tests make sure that common elements and critical pages are working correctly on the front end by simulating interactions with consumerfinance.gov in a browser. They're particularly useful in giving us confidence that our code is working as intended through dependency upgrades.

## Installing Cypress

We have included Cypress as a dependency of this project. The only installation step is doing a fresh `yarn` if you haven't already.

## Running Cypress tests

### Cypress app

To run the desktop Cypress app execute `yarn cypress open` from the command line. From the app, you can select the tests you want to run and the browser you want to run them in.

### Command line

You can run functional tests from the command line with `yarn cypress run`. That will run all tests in the `test/cypress/integration/` directory with the default test configuration: headless, in Cypress's default Electron browser, and against `localhost:8000`. You might want to modify the test run with some common arguments:

* `--spec test/cypress/integration/{path/to/test.js}` runs a single test suite
* `--browser chrome` runs the tests in Chrome, which is what we use to run tests in our continuous integration pipeline
* `--headed` shows the browser and Cypress output as the tests run, handy for watching what's happening during the tests
* `--no-exit` will keep the browser and Cypress output open after the tests complete, handy to inspect any errors
* `--config baseUrl={url}` will run the tests against a server other than `localhost:8000`

Cypress's [command line documentation](https://docs.cypress.io/guides/guides/command-line.html#Options) has the list of all the options you can set.

## Writing Cypress tests

When developing new tests for Cypress, it is important to consider what the test is trying to accomplish. We want to ensure that we are not polluting our Cypress tests with things that can be tested at another level, like in unit tests.

When adding a test it is often helpful to separate the arrange/act code from the actual assertions in order to improve the readability of our testing code. To do this we have adopted the page model of testing, where we define a page within the application and the methods of interacting with the page separate from the test file itself where we define the assertions. We call these files "helpers" and label them as such (example: `megamenu-helpers.js`), and we include them alongside the test files themselves in the `test/cypress/integration/` directory. (They are ignored when running tests thanks to the configuration of `cypress.json`.)

For example consider the `ConsumerTools` page "helper":

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
import ConsumerTools from './consumer-tools-helpers';

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

## Creating test data

Wagtail pages can be created programmatically by adding function calls to cfgov/v1/tests/wagtail_pages/create_test_data.py
To run this file locally, run the following commands on a bash shell within
the python container from the root folder:

`./cfgov/manage.py shell`
`from v1.tests.wagtail_pages import create_test_data`

Currently supported page types:
- blog_page
- browse_filterable_page
- browse_page
- landing_page
- learn_page
- sublanding_filterable_page
- sublanding_page

To import "create a page" functions, import from:
- v1.tests.wagtail_pages.helpers

"Create a page" functions return a path to the created page or None if no page was created

When adding tags or categories, they should be passed as a set:
`MY_TAGS = {"a tag", "another tag"}`

The first three arguments of any "create a page" function are title, slug, and parent path (optional, defaults to root)

Do not include new functions that only add test data in a pull request. When you are done running the test data creation
script, remove your created functions and only leave the documentation.
