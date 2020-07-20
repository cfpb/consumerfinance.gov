Feature: Mega Menu
  As a user of cf.gov
  I should be able to use the mega menu organism
  to navigate the site

Background:
  Given I goto URL "/"

Scenario: Large Size, on page Load
  Then the mega-menu organism should not show content

Scenario: Large Size, mouse moves between menu items
  When mouse moves from one link to another
  Then should only show second link content

@mobile
Scenario: Mobile Size, mouse moves between menu items
  Then the mega-menu organism should show menu when clicked

@mobile
Scenario: Mobile Size, mouse moves between menu items
  Then the mega-menu organism should show the PolyCom menu when clicked

@mobile
Scenario: Mobile Size, mouse moves between menu items
  Then the mega-menu organism should not shift menus when tabbing
