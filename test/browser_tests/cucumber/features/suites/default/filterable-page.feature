Feature: Filterable
  As a user of cf.gov
  I expect to see all results when I haven't selected a filter

Scenario: Sublanding filterable page
  Given I goto URL "/about-us/blog/"
  But I do not select a filter
  Then I should not see filtered results

Scenario: Browse filterable page
  Given I goto URL "/policy-compliance/rulemaking/final-rules/"
  But I do not select a filter
  Then I should not see filtered results
