# How we use GitHub Actions for continuous integration and automation

## What GitHub Actions do
We use [GitHub Actions](https://help.github.com/en/articles/about-github-actions) on consumerfinance.gov to perform the following tasks:

- Run automated lint checkers
- Run automated unit tests
- Measure unit test coverage
- Build and deploy this documentation to GitHub on the [`gh-pages` branch](https://github.com/cfpb/consumerfinance.gov/tree/gh-pages).
- Clean up stored artifacts

## How GitHub Actions are configured
We use the following constraints to optimize our CI builds for speed and utility:

- Our linting and unit tests run on pull requests only, including subsequent pushes to a pull request's branch. Tests are not run on the `main` branch.
- Our documentation is deployed on merges and pushes to the `main` branch only, and not on pull requests.
- We do not run builds of any kind on any other branches that are not `main`, and that are not pull request branches.
- We store coverage artifacts in between the unit test jobs and the coverage jobs. This requires us to run an action every hour using [the purge-artifacts action](https://github.com/marketplace/actions/purge-artifacts) to clean up these stored artifacts.

We use a combination of:

- [Build matrices](https://help.github.com/en/articles/workflow-syntax-for-github-actions#jobsjob_idstrategymatrix) to run the same tests on different versions of our dependnecies
- [Additional services](https://help.github.com/en/articles/workflow-syntax-for-github-actions#jobsjob_idservices) to provide, for example, PostgreSQL for our tests

Our workflows are defined in our [`.github/workflows`](https://github.com/cfpb/consumerfinance.gov/tree/main/.github/workflows) directory.

## An extra task for satellite repositories
For our [satellite apps](../related-projects/#satellite-apps), we use GitHub Actions (or Travis, if a repo hasn't been migrated to Actions yet) to build and attach a deployment wheel file to every release.

An example is the `.whl` file on [this release of the retirement app](https://github.com/cfpb/retirement/releases/tag/0.7.6).
