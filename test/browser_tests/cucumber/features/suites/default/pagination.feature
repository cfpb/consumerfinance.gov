
Feature: Pagination
  As a user of cf.gov
  I should be able to use the pagination molecule
  to navigate on the filterable pages

  Background:
    Given I goto a browse filterable page

  Scenario: Navigate to the next page
    When I click on the next button
    Then the page url should contain "page=2"
