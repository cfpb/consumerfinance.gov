# Navigational links: open in same tab
# Non-Navigational links: open in new tab
Feature: Verify the Loan Options page works according to requirements
  As a first time visitor to the Owning a Home page
  I want to navigate the Loan Options page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the "Loan Options" page


@smoke_testing @loan_options @loan_options_expandable
Scenario Outline: Click 'Learn More' to expand sections
  When I click Learn More to expand the "<section_name>" section
  Then I should see a collapse link for the "<section_name>" section
    And I should see "<expected_text>" inside the "<section_name>" section

Examples:
| section_name       | expected_text                      |
| Loan term          | Compare your loan term options     |
| Interest rate type | Compare your interest rate options |
| Loan type          | Choosing the right loan type       |


@loan_options @loan_options_expandable
Scenario Outline: Click 'Collapse' button to collapse sections
  When I click Learn More to expand the "<section_name>" section
    And I collapse the "<section_name>" section
  Then I should NOT see the "<section_name>" section expanded

Examples:
| section_name       |
| Loan term          |
| Interest rate type |
| Loan type          |


@loan_options @loan_options_expandable
Scenario Outline: Click 'Collapse <section_name>' link to collapse sections
  When I click Learn More to expand the "<section_name>" section
    And I collapse the "<section_name>" section
  Then I should NOT see the "<section_name>" section expanded

Examples:
| section_name       | link_name                   |
| Loan term          | Collapse loan terms         |
| Interest rate type | Collapse interest rate type |
| Loan type          | Collapse loan types         |


@smoke_testing @loan_options
Scenario Outline: Test inbound links in the Loan Options page
   When I click on the "<link_name>" link
   Then I should be directed to the internal "<relative_url>" URL
      And I should see "<page_title>" displayed in the page title

Examples:
| link_name     | page_title                                           | relative_url |
| Owning a Home | Owning a Home > Consumer Financial Protection Bureau | /            |


@smoke_testing @loan_options
Scenario: Test OAH link in the Loan Options page
   When I click on the "Owning a Home" link
   Then I should be directed to the OAH Landing page


@loan_options @loan_options_expandable
Scenario Outline: Expand 'Loan Types' section then click links inside the expanded section
  When I click Learn More to expand the "Loan type" section
    And I click Get all the details for "<loan_type>" loans
  Then I should be directed to the internal "<relative_url>" URL
      And I should see "Loan Options" displayed in the page title

Examples:
| loan_type        | relative_url                        |
| Conventional     | loan-options/conventional-loans/    |
| FHA              | loan-options/FHA-loans/             |
| Special programs | loan-options/special-loan-programs/ |


@loan_options @prod_only @loan_options_expandable
Scenario Outline: Expand 'Loan Types' section then click Non-Navigational links inside the expanded section
  When I click Learn More to expand the "Loan type" section
    And I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name          | relative_url                               | page_title                    |
| Qualified Mortgage | /askcfpb/1789/what-qualified-mortgage.html | What is a Qualified Mortgage? |

@loan_options @prod_only @loan_options_expandable
Scenario Outline: Expand 'Loan Term' section then click Non-Navigational links inside the expanded section
  When I click Learn More to expand the "Loan term" section
    And I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title Consumer Financial Protection Bureau open in a new tab

Examples:
| link_name                              | relative_url                                                                                                                 |
| principal and interest                 | /askcfpb/1941/on-a-mortgage-whats-the-difference-between-my-principal-and-interest-payment-and-my-total-monthly-payment.html |
| Learn why                              | /askcfpb/1941/on-a-mortgage-whats-the-difference-between-my-principal-and-interest-payment-and-my-total-monthly-payment.html |
| Learn more                             | /askcfpb/1965/how-do-mortgage-lenders-calculate-monthly-payments.html                                                        |
| Explore rates for different loan terms | /explore-rates/                                                                                                              |
| Loan Estimates                         | askcfpb/1995/what-is-a-loan-estimate.html |
| Learn more about balloon loans         | /askcfpb/104/what-is-a-balloon-loan.html  |


@loan_options @prod_only @loan_options_expandable
Scenario Outline: Expand 'Interest rate type' section then click links inside the expanded section
  When I click Learn More to expand the "Interest rate type" section
    And I click on the "<link_name>" link
  Then I should see the "<relative_url>" URL with page title Consumer Financial Protection Bureau open in a new tab

Examples:
| link_name                                   | relative_url                                                                                                                                        |
| principal and interest payment              | /askcfpb/1941/on-a-mortgage-whats-the-difference-between-my-principal-and-interest-payment-and-my-total-monthly-payment.html                        |
| increase or decrease based on the market    | /askcfpb/1949/for-an-adjustable-rate-mortgage-arm-what-are-the-index-and-margin-and-how-do-they-work.html                                           |
| payments can increase or decrease over time | /askcfpb/1947/if-i-am-considering-an-adjustable-rate-mortgage-arm-what-should-i-look-out-for-in-the-fine-print.html                                 |
| total monthly payment                       | /askcfpb/1941/on-a-mortgage-whats-the-difference-between-my-principal-and-interest-payment-and-my-total-monthly-payment.html                        |
| changes based on the market                 | /askcfpb/1949/for-an-adjustable-rate-mortgage-arm-what-are-the-index-and-margin-and-how-do-they-work.html                                           |
| could go up a lot                           | /askcfpb/1965/how-do-mortgage-lenders-calculate-monthly-payments.html                                                                               |
| notified in advance                         | /askcfpb/1843/i-received-notice-of-an-upcoming-rate-change-on-my-adjustable-rate-mortgage-ARM-why-did-i-receive-this-and-what-should-i-do-now.html  |
| specific rules                              | /askcfpb/1947/if-i-am-considering-an-adjustable-rate-mortgage-arm-what-should-i-look-out-for-in-the-fine-print.html                                 |
| how your rate is calculated                 | /askcfpb/1949/for-an-adjustable-rate-mortgage-arm-what-are-the-index-and-margin-and-how-do-they-work.html                                           |
| how much your rate and payment can adjust   | /askcfpb/1951/with-an-adjustable-rate-mortgage-arm-what-are-rate-caps-and-how-do-they-work.html                                                     |
| pre-payment penalties                       | /askcfpb/1957/what-is-a-prepayment-penalty.html                                                                                                     |
| loan balances that can increase             | /askcfpb/103/what-is-negative-amortization.html                                                                                                     |
| FHA loan                                    | /loan-options/FHA-loans/                                                                                                                            |
