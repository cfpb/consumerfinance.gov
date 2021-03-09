# Navigational links: open in same tab
# Non-Navigational links: open in new tab
Feature: Verify the Special Programs Loan page works according to requirements
  As a first time visitor to the Owning a Home page
  I want to navigate the Special Programs Loan page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the "Special Loan Programs" page


@smoke_testing @loan_options
Scenario Outline: Test Navigational links in the Special Programs Loan page
  When I click on the "<link_name>" link
  Then I should be directed to the internal "<relative_url>" URL
    And I should see "<page_title>" displayed in the page title

Examples:
| link_name                  | relative_url                                           | page_title    |
| Owning a Home              | /                                                      | Owning a Home |
| More on mortgage insurance | loan-options/special-loan-programs/#mortgage-insurance | Loan Options  |
| mortgage insurance         | loan-options/special-loan-programs/#mortgage-insurance | Loan Options  |


@smoke_testing @loan_options
Scenario Outline: Test NON-Navigational links in the Special Programs Loan page open in new tab
  When I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name          | relative_url                     | page_title   |
| conventional       | loan-options/conventional-loans/ | Loan Options |
| FHA                | loan-options/FHA-loans/          | Loan Options |
| conventional loans | loan-options/conventional-loans/ | Loan Options |


@smoke_testing @loan_options @prod_only
Scenario Outline: Test NON-Navigational outbound links in the Special Programs Loan page
  When I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name                           | relative_url                                                        | page_title                                        |
| Department of Veterans              | benefits.va.gov/homeloans/                                          | Home Loans Home                                   |
| eligible                            | benefits.va.gov/homeloans/purchaseco_certificate.asp                | Certificate of Eligibility                        |
| upfront fee                         | benefits.va.gov/homeloans/purchaseco_loan_fee.asp                   | Loan Fees                                         |
| US Department of Agriculture        | https://www.rd.usda.gov/programs-services/single-family-housing-guaranteed-loan-program                   | Single Family Housing Guaranteed Loan Program                          |
| Find out if you                     | eligibility.sc.egov.usda.gov/eligibility/welcomeAction.do           | Welcome                                           |
| this tool                           | downpaymentresource.com/                                            | Down Payment Resource                             |
| local housing counselor             | find-a-housing-counselor/                                           | Find a housing counselor                          |
| Learn more about mortgage insurance | askcfpb/1953/what-is-mortgage-insurance-and-how-does-it-work.html   | What is mortgage insurance and how does it work?  |
| Loan Estimates                      | askcfpb/1995/what-is-a-loan-estimate.html    | Consumer Financial Protection Bureau                 |


@smoke_testing @loan_options
Scenario Outline: Test Related links in the Special Programs Loan page
  When I click OTHER LOAN TYPES "<loan_type>"
  Then I should be directed to the internal "<relative_url>" URL
    And I should see "<page_title>" displayed in the page title

Examples:
| loan_type    | relative_url                      | page_title   |
| Conventional | /loan-options/conventional-loans/ | Loan Options |
| FHA          | /loan-options/FHA-loans/          | Loan Options |
