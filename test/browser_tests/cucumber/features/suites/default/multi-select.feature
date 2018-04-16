
Feature: MultiSelect Tags
  As a user of cf.gov
  I should be able to select using the multi-select

  Background:
    Given I goto a browse filterable page
    And I open the filterable list control

  Scenario: State on page load
    Then the multi-select should be rendered
    But no tags should be selected
    And the multi-select dropdown shouldn't be visible

  Scenario: Search input click
    When I click on the multi-select search input
    Then the multi-select dropdown should be visible

  Scenario: Search input focus
    When I focus on the multi-select search input
    Then the multi-select dropdown should be visible

  Scenario: Search input blur
    When I focus on the multi-select search input
    And I click away from the search input
    Then the multi-select dropdown shouldn't be visible
    And the multi-select dropdown length should be 0

  Scenario: Typing in search input, returning matched results
    When I enter "tag0" in the search input
    Then the multi-select dropdown should display "tag0"
    And the multi-select dropdown length should be 1

  Scenario: Typing in search input, not returning unmatched results
    When I enter "tag0" in the search input
    Then the multi-select dropdown shouldn't display "tag2"
    And the multi-select dropdown length should be 1

  Scenario: Typing in search input, clearing the input and closing results
    When I enter "tag0" in the search input
    And I hit the escape button on the search input
    Then the multi-select dropdown shouldn't be visible
    And the multi-select dropdown length should be 0
    And the options field shouldn't contain the class "filtered"

  Scenario: Typing in search input, highlighting the first item
    When I click on the multi-select search input
    And I hit the down arrow on the multi-select
    Then the first option should be highlighted

  Scenario: Interacting with options list, adding option to choices
    When I click on the multi-select search input
    And I click on the first option in the dropdown
    Then the choices element should contain the first option

  Scenario: Interacting with options list, removing option from choices
    When I click on the multi-select search input
    And I click on the first option in the dropdown
    And I click on the first option in the dropdown again
    Then the choices length should be 0

  @undefined
  Scenario: XIT - Interacting with options list, add an option with RETURN key
    When I click on the multi-select search input
    And I hit the down arrow on the multi-select
    And I switch to the active element

  @undefined
  Scenario: XIT - Interacting with options list, remove an option with RETURN key
    When I click on the multi-select search input
    And I hit the down arrow on the multi-select
    And I switch to the active element

  Scenario: Interacting with choices list, remove an option from choices
    When I click on the multi-select search input
    And I click on the first option in the dropdown
    And I click on the first choices element
    Then the choices length should be 0
