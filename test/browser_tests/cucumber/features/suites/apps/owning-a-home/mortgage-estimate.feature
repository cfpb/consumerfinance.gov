Feature: verify the /owning-a-home/mortgage-estimate page works according to requirements
As a first time visitor to the Buying a House page
I want to navigate the Mortgage Estimate page
So that I can find the information I'm looking for

@404
Scenario Outline: Testing availability of pages on Mortgage Estimate
  Given I navigate to the "<page_name>" page
  Then Links are working without 404 errors

Examples:
  | page_name             |
  | Mortgage Estimate     |
