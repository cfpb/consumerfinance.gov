Feature: Header
  As a user of cf.gov
  I should be able to use the Header

Background:
  Given I goto URL "/"

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
  When I click on the mega-menu trigger
  Then the header organism should display the global header Cta SM
  Then the header organism shouldn't display the global eyebrow LG
  Then the header organism should display the global eyebrow SM

@mobile
Scenario: Mobile, if you click mega menu, if you click search
  When I click on the mega-menu trigger
  Then the header organism should display the overlay
  When I click on the mega-menu search trigger
  Then the mega-menu search form should be displayed
  And the mega-menu shouldn't be displayed
