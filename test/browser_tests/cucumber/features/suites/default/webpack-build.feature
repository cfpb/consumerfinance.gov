Feature: Webpack-build
  As a front-end developer
  I should ensure the build is transpiled correctly

Background:
  Given I run gulp build to generate JS bundles

@webpack
Scenario: The following transpilers should have run:
            check-es2015-constants
            transform-es2015-arrow-functions
  #Regex test: https://regex101.com/r/BBC1pS/2
  Then the JS bundles shouldn't contain double arrows or constants
