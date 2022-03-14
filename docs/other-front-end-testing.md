# Other Front-end Testing

## Performance testing

To audit if the site complies with performance best practices and guidelines,
[Google's Lighthouse](https://github.com/GoogleChrome/lighthouse) can be run
from Google Chrome by opening the developer console and going to the Lighthouse
tab to run a performance audit.

We also have an automated task that generates a lighthouse report every night at
https://cfpb.github.io/cfgov-lighthouse/
([repository](https://cfpb.github.io/cfgov-lighthouse/)).

## Source code linting

The default test task includes linting of the JavaScript source, build,
and test files.
Use the `yarn run lint` command from the command-line to run the ESLint linter,
which checks the JavaScript against the rules configured in `.eslintrc`.
[See the ESLint docs](https://eslint.org/docs/rules/)
for detailed rule descriptions.

There are a number of options to the command:

 - `--fix`: Add this flag (like `yarn run lint --fix`)
   to auto-fix some errors, where ESLint has support to do so.
 - [Other options available in the docs](https://eslint.org/docs/user-guide/command-line-interface)

## Cross browser testing


### Sauce Labs
We use https://saucelabs.com to test the site across browsers.
After logging in, the production site URLs can be tested via
`Live` > `Cross Browser` in the sidebar.

To test changes from `localhost` before they make it to production,
the Sauce Connect Proxy can be used. See more info on the
[Sauce Labs documentation site](https://docs.saucelabs.com/secure-connections/sauce-connect/installation/).


### iOS Simulator
While it's possible to check iOS devices in Sauce Labs,
the JavaScript developer console will not be available. Therefore, it may be
helpful to instead use the iOS Simulator included inside Xcode.
To use the simulator with a developer console, perform the following:

1. Find the Xcode application on your computer.
2. Right-click on the application and select `Show Package Contents`.
3. Find and open the iOS Simulator at
   `Contents` > `Developer` > `Applications` > `Simulator`.
4. Open mobile Safari and navigate to the page you want to test out.
2. Now, outside of the iOS Simulator,
   navigate to and open the desktop Safari application.
2. Ensure the developer menu is shown by checking the box at
   `Safari` > `Preferences…` > `Advanced` > `Show Develop menu in menu bar`.
3. Open the `Develop` menu in desktop Safari and
   there should be a `Simulator` option that when opened will show any
   JavaScript console output that's coming from the page you're visiting in the
   iOS Simulator.
