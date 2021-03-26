# Guidance on how to contribute

> All contributions to this project will be released under the CC0 public domain
> dedication. By submitting a pull request or filing a bug, issue, or
> feature request, you are agreeing to comply with this waiver of copyright interest.
> Details can be found in our [TERMS](TERMS.md) and [LICENCE](LICENSE).

There are two primary ways to help:
 - Using the issue tracker, and…
 - Changing the codebase.


## Using the issue tracker

Use the issue tracker to suggest feature requests, report bugs, and ask questions.
This is also a great way to connect with the developers of the project as well
as others who are interested in this solution.

Use the issue tracker to find ways to contribute.
Find a bug or a feature, mention in the issue that you will take on that effort,
then follow the _Changing the codebase_ guidance below.


## Changing the codebase

If you are a contributor from outside of CFPB, you should fork this repository,
make changes in your own fork, and then submit a pull request.

If you are a contributor within CFPB, you may also fork, or follow our
[documentation for branching](https://cfpb.github.io/consumerfinance.gov/branching-merging/).

For timely code reviews of pull requests, please tag @cfpb/cfgov-backends and
@cfpb/cfgov-frontends as appropriate for your changes.

All new code should have associated unit tests and/or functional tests that
validate implemented features and the presence or lack of defects.
The overall test coverage of the codebase should not decrease.

Python code is expected to follow
[PEP8](https://www.python.org/dev/peps/pep-0008/) and
[not commit atrocities](https://www.youtube.com/watch?v=wf-BqAjZb8M).
JavaScript, CSS/Less, and markup should follow our
[front-end standards](https://github.com/cfpb/development).
When in doubt, mimic the styles and patterns in the existing codebase.

### Browser support

We configure [Autoprefixer](#autoprefixer) and [Babel](#babel) to support the
following list of browsers.

- Latest 2 releases of all browsers including:
    - Chrome
    - Firefox
    - Safari
    - Internet Explorer
    - Edge
    - Opera
    - iOS Safari
    - Opera Mini
    - Android Browser
    - BlackBerry Browser
    - Opera Mobile
    - Chrome for Android
    - Firefox for Android
    - Samsung Internet

https://browserl.ist/?q=last+2+versions

As well as additional Autoprefixer support for:

- Internet Explorer 8
- Internet Explorer 9

https://browserl.ist/?q=last+2+versions%2C+Explorer+%3E%3D+8

What this means to the end-user is we've added a level of backward
compatibility for modern features as much as possible. This doesn't
necessarily mean feature parity. Where it's impossible or impractical to
implement a modern feature, we fallback to standard practices for that browser.
For example, we do not deliver interactive scripting
for Internet Explorer 8 and 9,
but we do ensure that default browser features continue to work so users
that can't or don't want to upgrade continue to have access to the site and
our content.

#### Satellite app assets

Satellite apps may run within consumerfinance.gov, but manage their own assets
within the
[unprocessed/apps](https://github.com/cfpb/consumerfinance.gov/tree/main/cfgov/unprocessed/apps)
directory. These apps can have their own package.json file, webpack config file,
and
[browserlist config](https://github.com/browserslist/browserslist#config-file)
file. Together of which may create a different level of browser support,
third-party assets, or configuration for these apps, relative to the main site.

#### Browser Testing

We have automated tests that use a headless version of Chrome to ensure
the majority of the site is working as expected. For manual testing, we
realistically test this project locally or in a virtual environment with the
following list of browsers:

- Chrome
- Firefox
- Safari
- Internet Explorer 8, 9, 10, and 11
- Edge
- iOS Safari
- Chrome for Android

#### Autoprefixer

Autoprefixer parses our CSS and adds vendor prefixes to rules where necessary
using reported feature support by [Can I Use](https://caniuse.com/). For more
information visit the [Autoprefixer documentation site]
(https://autoprefixer.github.io/).

#### Babel

Babel compiles our [ES6](http://es6-features.org/) JavaScript where necessary
for the browsers that either don't support or have limited support of ES6
features. For more information visit the [Babel documentation site]
(https://babeljs.io/).

#### Known feature differences

- JavaScript:
  We do not serve interactive scripting to Internet Explorer 8 and 9,
  but we do collect analytics via JavaScript.

#### Resources

- https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/
- https://saucelabs.com/beta/dashboard/tests
- https://developer.samsung.com/remotetestlab/rtlDeviceList.action
