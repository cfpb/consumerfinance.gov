
Feature: Filterable
  As a user of cf.gov
  I expect to see all results when I haven't selected a filter

  Scenario: Sublanding filterable page
  	Given I goto a sublanding filterable page
  	When I havent select a filter
  	Then I should see the first result
  	Then I should see the last result
  	Then I should see the right number of results
