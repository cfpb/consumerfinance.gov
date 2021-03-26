Feature: Global Search
  As a user of cf.gov
  I should be able to use the global search molecule
  to search for content on the site

Background:
  Given I goto URL "/"

Scenario: Large Size, on page Load
  Then the search molecule should have a search trigger
  And it shouldn't have search input content
  And it shouldn't have suggested search terms

Scenario: Large Size, after clicking search
  When I click on the search molecule
  Then the search molecule shouldn't have a search trigger
  And it should have search input content
  And it should focus the search input field

Scenario: Large Size, after entering Text
  When I enter "test" in the search molecule

Scenario: Large Size, should navigate to search portal
  When I enter "test" in the search molecule
  Then I should navigate to search portal

Scenario: Large Size, after clicking off search
  And I click off the search molecule
  Then it shouldn't have search input content

Scenario: Large Size, after the tab key is pressed
  When I focus on the search molecule trigger
  And I perform tab actions on the search molecule
  Then it shouldn't have search input content

Scenario: Mobile, should have suggested search terms
  When I click on the search molecule
