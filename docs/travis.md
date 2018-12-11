# How we use Travis CI

## What Travis does
We use [Travis CI](https://travis-ci.org/) on cfgov-refresh to perform the following tasks:

- Run automated unit tests, accessibility tests, and acceptance tests.
- Deploy this documentation website to Github on the [gh-pages branch](https://github.com/cfpb/cfgov-refresh/tree/gh-pages).

## How Travis is configured
We use the following constraints to optimize Travis builds for speed and utility:

- Travis runs tests on Pull Requests and subsequent pushes to Pull Request branches only, and not on the master branch.
- Travis deploys documentation on merges and pushes to the master branch only, and not on PRs.

We use a combination of [build conditionals](https://docs.travis-ci.com/user/conditions-v1) and [build stages](https://docs.travis-ci.com/user/build-stages/) in the [.travis.yml](https://github.com/cfpb/cfgov-refresh/blob/master/.travis.yml) file and Settings in the Travis UI to customize Travis to fit the above constraints.