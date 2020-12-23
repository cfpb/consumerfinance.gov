Feature: Verify the /owning-a-home/mortgage-closing page works according to requirements
As a first time visitor to the Owning a Home page
I want to navigate the Mortgage Closing page
So that I can find the information I'm looking for

@404
Scenario Outline: Testing availability of pages on Mortgage Closing
  Given I navigate to the "<page_name>" page
  Then Links are working without 404 errors

Examples:
| page_name        |
| Mortgage Closing |
