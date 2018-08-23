# The feature description is for humans only
Feature: Regs3K search page
  As a user of Regs3K's search page
  I should be able to search and filter my search results

  Background:
    # This assumes you have Regs3K search set up at the below URL
    Given I goto URL "/policy-compliance/rulemaking/regulations/search-regulations/results/"

  Scenario: Search for a term
    When I enter "automobile" in the regulations search field
    And I submit the search form
    Then the page url should contain "q=automobile"

  Scenario: Filter by regulations
    When I enter "disclosure" in the regulations search field
    And I submit the search form

    And I select the regulation 1010 filter
    And I wait for the search results to load
    Then regulation 1010 filter tag should appear

    And I select the regulation 1011 filter
    And I wait for the search results to load
    Then regulation 1011 filter tag should appear

    And I remove the regulation 1010 filter tag
    And I wait for the search results to load
    Then regulation 1010 filter tag should disappear
    Then regulation 1010 filter should not be selected

    And I select the regulation 1026 filter
    And I wait for the search results to load
    Then regulation 1026 filter tag should appear

    And I select the regulation 1011 filter
    And I wait for the search results to load
    Then regulation 1011 filter tag should disappear
    Then regulation 1011 filter should not be selected
