Feature: Verify the /owning-a-home/process page works according to requirements
As a first time visitor to the Owning a Home page
I want to navigate the process page
So that I can find the information I'm looking for

@journey @404
Scenario Outline: Testing availability of all pages
  Given I navigate to the "<page_name>" page
  Then I see page loaded
  Then Links are working without 404 errors

Examples:
| page_name            |
| Know the Process     |
| Prepare to Shop      |
| Explore Loan Options |
| Compare Loan Options |
| Get Ready to Close   |

@journey @404
Scenario Outline: Testing availability of all pages
  Given I navigate to the "<page_name>" page
  Then Links are working without 404 errors

Examples:
| Sources |
