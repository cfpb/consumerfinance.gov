Feature: Verify the page structure for the Strategic Plan page
  As a first time visitor
  I want to verify that the Strategic Plan page structure is correct
  So that clicking on individual links cause the correct page to be displayed

@smoke_testing
Scenario Outline: Navigate to the Strategic Plan page, verify the page header is correct and at least 1 article is displayed
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Strategic plan"
  Then The Strategic Plan "<header_text>" page header is correctly displayed
    And I should see at least "1" article listed in the Strategic Plan page

Examples:
| header_text                                         |
| Consumer Financial Protection Bureau Strategic Plan |

Scenario Outline: Navigate to the Strategic Plan page, click on an article and verify the browser scrolls up to the correct section
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Strategic plan"
    And I click on the "<article_title>" item
  Then I should should see the page scroll to the "<page_section>" section

Examples:
| article_title        | page_section |
| OVERVIEW OF THE CFPB | #overview    |
| PLAN OVERVIEW        | #plan        |
