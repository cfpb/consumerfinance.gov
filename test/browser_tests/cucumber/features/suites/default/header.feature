
Feature: Header
  As a user of cf.gov
  I should be able to use the Header

  Background:
    Given I goto a browse filterable page

  Scenario: Desktop, at page load
    Then the header organism should display the header
    And the header organism should display the logo
    And the header organism should display the mega menu
    And the header organism should display the global search
    And the header organism should display the global eyebrow LG
    And the header organism should display the global header Cta LG
    And the header organism shouldn't display the global header Cta SM
    And the header organism shouldn't display the global eyebrow SM

  @mobile
  Scenario: Mobile, at page load
    Then the header organism should display the header
    And the header organism should display the logo
    And the header organism should display the mega menu
    And the header organism shouldn't display the overlay
    And the header organism should display the global search
    And the header organism shouldn't display the global header Cta LG

  @mobile
  Scenario: Mobile, if you click the mega menu trigger
    When I click the the mega-menu trigger
    Then the header organism should display the global header Cta SM
    Then the header organism shouldn't display the global eyebrow LG
    Then the header organism should display the global eyebrow SM

  @mobile
  Scenario: Mobile, if you click mega menu
    When I click on the mega-menu trigger
    Then the header organism should display the overlay
    And I click on search
    Then it should show the search and hide the mega-menu

  @mobile
  Scenario: Mobile, if you click search, then click mega menu
    When I click on the mega-menu search
    And click the mega-menu
    Then it should show the mega menu and hide search

