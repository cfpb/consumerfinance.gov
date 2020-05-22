# Navigational links: open in same tab
# Non-Navigational links: open in new tab
Feature: test the Rate Checker inbound and outbound links
  As a first time visitor to the Rate Checker page
  I want to click on links
  So that I can make informed choices when shopping for a mortgage loan

Background:
  Given I navigate to the "Rate Checker" page


@rate_checker
Scenario Outline: Click Non-Navigational links
  When I click on the "<link_name>" link in the Rate Checker page
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name                           | relative_url                                                    | page_title                                     |
| Loan Estimates                      | askcfpb/1995/what-is-a-loan-estimate.html    | Consumer Financial Protection Bureau                |
| discount points                     | askcfpb/136/what-are-discount-points-or-points.html             | What are discount points or points?            |
| rate lock                           | askcfpb/143/whats-a-lock-in-or-a-rate-lock.html                 | What's a lock-in or a rate lock?               |
| checked your credit report recently | annualcreditreport.com                                          | Annual Credit Report.com                       |
| get them corrected                  | askcfpb/314/how-do-i-dispute-an-error-on-my-credit-report.html  | How do I dispute an error on my credit report? |
| www.informars.com                   | informars.com                                                   | Informa Research Services                      |
| kind of loan                        | owning-a-home/loan-options/                                     | Consumer Financial Protection Bureau           |
| points | askcfpb/136/what-are-discount-points-or-points.html | Consumer Financial Protection Bureau |
| mortgage insurance | askcfpb/1953/what-is-mortgage-insurance-and-how-does-it-work.html | Consumer Financial Protection Bureau |
| closing costs  | askcfpb/1845/what-fees-or-charges-are-paid-closing-and-who-pays-them.html | Consumer Financial Protection Bureau |
| Loan Estimates | askcfpb/1995/what-is-a-loan-estimate.html | Consumer Financial Protection Bureau |


@rate_checker
Scenario Outline: Click Non-Navigational links inside tab page
  When I click on the "I won’t buy for several months" tab in the Rate Checker page
    And I click on the "<link_name>" link in the Rate Checker page
  Then I should see the "<relative_url>" URL with page title <page_title> open in a new tab

Examples:
| link_name                                | relative_url                                                    | page_title                                 |
| Loan Estimates                    | askcfpb/1995/what-is-a-loan-estimate.html    | Consumer Financial Protection Bureau                |
| Learn more about credit scores           | askcfpb/315/what-is-my-credit-score.html                        | What is my credit score?                   |
| Learn about improving your credit scores | askcfpb/318/how-do-i-get-and-keep-a-good-credit-score.html      | How do I get and keep a good credit score? |
| Learn more about down payments           | askcfpb/120/what-kind-of-down-payment-do-i-need-how-does-the-amount-of-down-payment-i-make-affect-the-terms-of-my-mortgage-loan.html | What kind of down payment do I need?        |


@rate_checker
Scenario: Click internal links
  When I click on the "About our data source" link in the Rate Checker page
  Then I should see the page scroll to the "#about" section
