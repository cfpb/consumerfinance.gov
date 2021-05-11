# Other Front-end Testing

## Performance testing

To audit if the site complies with performance best practices and guidelines,
[Google's Lighthouse](https://github.com/GoogleChrome/lighthouse) can be run
from Google Chrome by opening the developer console and going to the Lighthouse
tab to run a performance audit.

## Accessibility testing

Run the acceptance tests with an `--a11y` flag (i.e. `gulp test:acceptance --a11y`)
to check every webpage for WCAG and Section 508 compliancy using Protractor's
[accessibility plugin](https://github.com/angular/protractor-accessibility-plugin).

## Source code linting

The default test task includes linting of the JavaScript source, build,
and test files.
Use the `gulp lint` command from the command-line to run the ESLint linter,
which checks the JavaScript against the rules configured in `.eslintrc`.
[See the ESLint docs](https://eslint.org/docs/rules/)
for detailed rule descriptions.

There are a number of options to the command:

 - `gulp lint:build`: Lint only the gulp build scripts.
 - `gulp lint:test`: Lint only the test scripts.
 - `gulp lint:scripts`: Lint only the project source scripts.
 - `--fix`: Add this flag (like `gulp lint --fix` or `gulp lint:build --fix`).
   to auto-fix some errors, where ESLint has support to do so.
 - `--path`: Add this flag to specify a file to lint,
   rather than all files. Path is relative to the project root,
   such as `gulp lint --path=cfgov/unprocessed/js/modules/Analytics.js`.
