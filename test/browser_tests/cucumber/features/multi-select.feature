
Feature: MultiSelect Tags
  As a user of cf.gov
  I should be able to select using the multi-select

  Scenario: Selecting topic tags on the Filterable List Control
  	Given I goto a sublanding filterable page
  	When I expand the filter
  	Then I should be able to select topics using the multi-select
