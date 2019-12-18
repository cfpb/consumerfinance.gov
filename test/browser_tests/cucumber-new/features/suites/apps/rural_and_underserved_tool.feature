Feature: Verify the Rural and underserved areas tool landing page works according to requirements
  As a first time visitor to the Rural and underserved areas tool landing page
  I want to Check status of properties for loans extended on the landing page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the Rural and underserved areas tool landing page

@smoke_testing @rural
Scenario Outline: Check status of properties for loans extended
  Given I navigate to the Rural and underserved areas tool landing page
  When I check status of properties for loans extended in <year>
  Then I Enter addresses manually <address>
  And I click on the "Check addresses" button
Examples:
| year | address                                      |
| 2019 | BCFP, 1700 G St. N.W. Washington, D.C. 20552 |
| 2018 | CFPB, 1990 K St. N.W. Washington, D.C. 20006 |
| 2017 | CFPB, PO Box 2900, Clinton, IA 52733-2900    |
