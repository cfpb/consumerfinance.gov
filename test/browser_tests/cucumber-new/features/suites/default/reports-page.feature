Feature: Verify the Reports page structure is correct
  As a visitor to the Reports page
  I want to verify that the page structure is correct
  So that clicking on individual links cause the correct Reports article to be displayed

@smoke_testing @reports @page_structure
Scenario Outline: Navigate menu to the Reports page, check page header/paragraph then click on the article to verify it loads the correct page
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Reports"
  Then I should see "6" articles listed in the Reports page
    And The Reports page header is correctly displayed as "<header_text>"
    And The paragraph sections are NOT empty
    And Clicking on a Reports article causes the correct article to be displayed

Examples:
| header_text |
| Reports     |
