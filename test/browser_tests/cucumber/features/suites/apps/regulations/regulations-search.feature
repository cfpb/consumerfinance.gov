# The feature description is for humans only
Feature: Regs3K search page
  As a user of Regs3K's search page
  I should be able to use the search field
  to search for a query

  Background:
    # This assumes you have Regs3K search set up at the below URL
    Given I goto URL "/policy-compliance/rulemaking/regulations/search/results/"

  Scenario: Search for a term
    When I enter "automobile" in the regulations search field
    And I submit the search form
    Then the page url should contain "q=automobile"
