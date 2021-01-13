Feature: Pagination
  As a user of cf.gov
  I should be able to use the pagination molecule
  to navigate on the filterable pages

Background:
  Given I goto URL "/about-us/blog/"

@skip
Scenario: Navigate to the next page
  When I click on the next button
  Then the page url should contain "page=2"

@skip
Scenario: Navigate to the previous page
  When I click on the next button
  And I click on the previous button again
  Then the page url should contain "page=1"

@skip
Scenario: Navigate to nth Page
  When I enter "2" in the page input field
  And I click on the next button again
  Then the page url should contain "page=2"
