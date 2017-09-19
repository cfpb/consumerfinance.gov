#noinspection CucumberUndefinedStep
Feature: Credit card agreement database
  As a credit card customer
  I want to search for agreements between credit card issuers and customers
  So that I can view the general terms and conditions, pricing, and fee information.

# Agreements smoke testing
@smoke_testing
Scenario: Reach the Credit card agreement database page through the menu
  Given I visit the www.consumerfinance.gov/jobs/ URL
  When I hover over "PARTICIPATE" menu
  And I click on "Credit cards" item
  And I click on the "Credit Card Agreement Database" link
  Then I should be directed to the "www.consumerfinance.gov/credit-cards/agreements/" URL
  And the page should load properly
  And I should see the page title as "Credit card agreement database - Consumer Financial Protection Bureau"

@smoke_testing
Scenario: Reach the page listing credit card agreements from Bank of America in the database
  Given I visit the www.consumerfinance.gov/credit-cards/agreements/ URL
  When I select what I call the "card issuer" drop list and search "bank of america" and choose first
  Then I should be directed to the "www.consumerfinance.gov/credit-cards/agreements/issuer/176/" URL
  And the page should load properly
  And I should find the text "Agreements by 'Bank of America NA'" on the page


# behave -w
# behave -t=smoke_testing --logging-level=INFO
