# How we use Travis CI

## What Travis does
We use [Travis CI](https://travis-ci.org/) on cfgov-refresh to perform the following tasks:

- Run automated unit tests and acceptance tests.
- Deploy this documentation website to GitHub on the [`gh-pages` branch](https://github.com/cfpb/cfgov-refresh/tree/gh-pages).

## How Travis is configured
We use the following constraints to optimize Travis builds for speed and utility:

- Travis runs tests on pull requests only, including subsequent pushes to a pull request's branch. Tests are not run on the `master` branch.
- Travis deploys documentation on merges and pushes to the `master` branch only, and not on pull requests.
- We do not run Travis builds of any kind on any other branches that are not `master`, and that are not pull request branches.

To customize Travis to fit the above constraints, we use a combination of:

 - [Build conditionals](https://docs.travis-ci.com/user/conditions-v1) and [build stages](https://docs.travis-ci.com/user/build-stages/) in our [.travis.yml](https://github.com/cfpb/cfgov-refresh/blob/master/.travis.yml) file 
 - "Settings" in the Travis UI at https://travis-ci.org

## An extra task for satellite repositories

For our [satellite apps](../related-projects/#satellite-apps), Travis is also used to build and attach a deployment wheel file to every release.

An example is the `.whl` file on [this release of the retirement app](https://github.com/cfpb/retirement/releases/tag/0.7.6).
