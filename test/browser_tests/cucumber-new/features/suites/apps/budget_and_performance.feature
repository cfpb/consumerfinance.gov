Feature: Verify the page structure for the Budget and Performance page
  As a first time visitor
  I want to verify that the Strategic Plan page structure is correct
  So that clicking on invidual links cause the correct page to be displayed

@smoke_testing
Scenario Outline: Navigate to the Budget page, verify the page header is correct and at least 1 Budget article is displayed
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Budget and performance"
  Then The "<header_text>" page header is correctly displayed
    And I should see at least "1" article listed in the Budget page

Examples:
| header_text     |
| The CFPB budget |
