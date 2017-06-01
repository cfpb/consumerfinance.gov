
Feature: Filterable
  As a user of cf.gov
  I expect to see all results when I haven't selected a filter

  Scenario: Sublanding filterable page
  	Given I goto a sublanding filterable page
  	But I do not select a filter
  	Then I should see the first page result, sfp child 0
  	And I should see the last page result, sfp child 9
  	And I should see 10 page results

  Scenario: Browse filterable page
  	Given I goto a browse filterable page
  	But I do not select a filter
  	Then I should see the first page result, bfp child 0
  	And I should see the last page result, bfp child 9
  	And I should see 10 page results
