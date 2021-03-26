Feature: Verify the navigation tabs/links works according to requirements
  As a first time visitor to the Owning a Home page
  I want to click on invidual tabs and links
  So that I can easily navigate the site


@smoke_testing @landing_page
Scenario Outline: Test Journey links in the landing page
  Given I navigate to the OAH Landing page
  When I click on the link with id "<link_id>"
  Then I should be directed to the internal "<relative_url>" URL
  And I should see "<page_title>" displayed in the page title

Examples:
| link_id             | page_title       | relative_url     |
| prepare-header-link | Know the Process | process/prepare/ |
| prepare-learn-link  | Know the Process | process/prepare/ |
| explore-header-link | Know the Process | process/explore/ |
| explore-learn-link  | Know the Process | process/explore/ |
| compare-header-link | Know the Process | process/compare/ |
| compare-learn-link  | Know the Process | process/compare/ |
| close-header-link   | Know the Process | process/close/   |
| close-learn-link    | Know the Process | process/close/   |


@smoke_testing @landing_page
Scenario Outline: Test outbound links in the landing page
  Given I navigate to the OAH Landing page
  When I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name                                       | page_title               | relative_url                                               |
| Get answers from AskCFPB                 | Mortgages                | /askcfpb/search/?selected_facets=category_exact:mortgages  |
| Submit it to the CFPB                     | Submit a complaint       | /complaint/#mortgage                                       |
| Find a HUD-certified housing counselor           | Find a housing counselor | /find-a-housing-counselor/                                 |
| Most are listed in this loan originator database | Consumer Access | http://www.nmlsconsumeraccess.org/ |
| Learn how the CFPB is protecting mortgage borrowers | Know before you owe                | /know-before-you-owe/ |
| We can help | Mortgage help                | /mortgagehelp/ |
| Get videos, compliance guides, and other resources | Regulatory implementation                | /regulatory-implementation/ |
| Your home loan toolkit: a step-by-step guide | https://www.consumerfinance.gov/f/201503_cfpb_your-home-loan-toolkit-web.pdf                | https://www.consumerfinance.gov/f/201503_cfpb_your-home-loan-toolkit-web.pdf |
