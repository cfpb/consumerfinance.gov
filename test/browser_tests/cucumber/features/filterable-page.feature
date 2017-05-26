
Feature: Filterable
  As a user of cf.gov
  I expect to see all results when I haven't selected a filter

  Scenario: Sublanding filterable page
  	Given I goto a sublanding filterable page
  	When I do not select a filter on the sublanding filterable page
  	Then I should see the first result, sfp child 0
  	Then I should see the last result, sfp child 9
  	Then I should see the right number of results on the sublanding filterable page

  Scenario: Browse filterable page
  	Given I goto a browse filterable page
  	When I do not select a filter on the browse filterable page
  	Then I should see the first result, bfp child 0
  	Then I should see the last result, bfp child 9
  	Then I should see the right number of results on the browse filterable page
