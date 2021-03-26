# Navigational links: open in same tab
# Non-Navigational links: open in new tab
Feature: Verify the Conventional Loan page works according to requirements
  As a first time visitor to the Owning a Home page
  I want to navigate the Conventional Loan page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the "Conventional Loan" page

@smoke_testing @loan_options
Scenario Outline: Test Navigational links in the Conventional Loan page open is same tab
  When I click on the "<link_name>" link
  Then I should be directed to the internal "<relative_url>" URL
    And I should see "<page_title>" displayed in the page title

Examples:
| link_name                  | relative_url                                         | page_title    |
| Owning a Home              | /                                                    | Owning a Home |
| Understand loan options    | /loan-options/                                       | Loan Options  |
| More on mortgage insurance | /loan-options/conventional-loans/#mortgage-insurance | Loan Options  |

@smoke_testing @loan_options
Scenario Outline: Test NON-Navigational links in the Conventional Loan page open in new tab
  When I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name | relative_url             | page_title   |
| FHA loans | /loan-options/FHA-loans/ | Loan Options |

@smoke_testing @loan_options @prod_only
Scenario Outline: Test Navigational outbound links in the Conventional Loan page
  When I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name                                                         | relative_url                                                                        | page_title                                                         |
| Fannie Mae or Freddie Mac                                         | /askcfpb/1959/what-are-fannie-mae-and-freddie-mac.html                              | What are Fannie Mae and Freddie Mac?                               |
| unless you’re buying a home with multiple units                   | /askcfpb/1961/how-can-i-find-the-loan-limit-for-a-conforming-loan-in-my-county.html | How can I find the loan limit for a conforming loan in my county?  |
| Maximum loan amount varies by county                              | /askcfpb/1961/how-can-i-find-the-loan-limit-for-a-conforming-loan-in-my-county.html | How can I find the loan limit for a conforming loan in my county?  |
| Loan Estimates                    | askcfpb/1995/what-is-a-loan-estimate.html    | Consumer Financial Protection Bureau                |
| Learn more about mortgage insurance                               | /askcfpb/1953/what-is-mortgage-insurance-and-how-does-it-work.html                  | What is mortgage insurance and how does it work?                   |
| What are Fannie Mae and Freddie Mac?                              | /askcfpb/1959/what-are-fannie-mae-and-freddie-mac.html                              | What are Fannie Mae and Freddie Mac?                               |
| How can I find the loan limit for a conforming loan in my county? | /askcfpb/1961/how-can-i-find-the-loan-limit-for-a-conforming-loan-in-my-county.html | How can I find the loan limit for a conforming loan in my county?  |


@smoke_testing @loan_options
Scenario Outline: Test OTHER LOAN TYPES links in the Conventional Loan page
  When I click OTHER LOAN TYPES "<loan_type>"
  Then I should be directed to the internal "<relative_url>" URL
    And I should see "<page_title>" displayed in the page title

Examples:
| loan_type        | relative_url                         | page_title   |
| FHA              | /loan-options/FHA-loans/             | Loan Options |
| Special Programs | /loan-options/special-loan-programs/ | Loan Options |
