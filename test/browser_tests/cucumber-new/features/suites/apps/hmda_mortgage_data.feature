Feature: Verify the Mortgage data (HMDA) landing page works according to requirements
  As a first time visitor to the HMDA landing page
  I want to select year(s) of data on the landing page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the Explore HMDA data landing page

@smoke_testing @hmda
Scenario Outline: Select year and suggested filter
  Given I navigate to the Explore HMDA data landing page
  When I click on the "Explore data" link
  Then I select year <year>
  And I select filter <filter>
  When I click on the "Create a summary table" link
Examples:
| year | filter                   |
| 2017 | All records              |
| 2017 | All originated mortgages |
| 2017 | Mortgages for first-lien, owner-occupied, 1-4 family homes (including manufactured housing) |
