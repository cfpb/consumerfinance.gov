Feature: Verify the Rural and underserved areas tool landing page works according to requirements
  As a first time visitor to the Rural and underserved areas tool landing page
  I want to Check status of properties for loans extended on the landing page
  So that I can find the information I'm looking for

@rural
Scenario Outline: Check status of properties for loans extended
  Given I visit the consumerfinance rural-or-underserved-tool URL
  When I check status of properties for loans extended in <year>
  Then I Enter addresses manually <address>
  And I click on the "Check addresses" button
  Then I should find the text "1 of 1 addresses processed for <year> rural or underserved area safe harbor designation." on the page
  And I should find the text "<address>" on the page
  And I should find the text "<identified>" on the page
Examples:
| year | address                                      | identified                  |
| 2019 | BCFP, 1700 G St. N.W. Washington, D.C. 20552 | 1 address is not identified |
| 2018 | CFPB, 1990 K St. N.W. Washington, D.C. 20006 | 1 address is not identified |
| 2017 | CFPB, PO Box 2900, Clinton, IA 52733-2900    | 1 address is not identified |
