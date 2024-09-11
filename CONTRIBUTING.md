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
JavaScript, CSS/SCSS, and markup should follow our
[front-end standards](https://github.com/cfpb/development).
When in doubt, mimic the styles and patterns in the existing codebase.

### Browser support

See our
[browser support docs](https://cfpb.github.io/consumerfinance.gov/browser-support)
for more information.

#### Browser Testing

We run automated browser tests in headless Chrome with `yarn cy`.
See our [cross browser testing docs](https://cfpb.github.io/consumerfinance.gov/other-front-end-testing/#cross-browser-testing) for other testing methods.

#### Satellite app assets

Satellite apps may run within consumerfinance.gov, but manage their own assets
within the
[unprocessed/apps](https://github.com/cfpb/consumerfinance.gov/tree/main/cfgov/unprocessed/apps)
directory. These apps can have their own dependencies within their package.json file.

#### Resources

- https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/
- https://saucelabs.com/beta/dashboard/tests
- https://developer.samsung.com/remotetestlab/rtlDeviceList.action
