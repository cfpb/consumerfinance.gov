Feature: Credit card agreement database
  As a consumer
  I want to review general terms and conditions, pricing, and fee information
  So that I can learn more about credit card agreements.

@smoke_testing
Scenario: Reach the page listing credit card agreements from Bank of America in the database
  Given I visit the www.consumerfinance.gov/credit-cards/agreements/ URL
  When I select what I call the "card issuer" drop list and search "Bank of America" and choose first
  Then I should be directed to the "www.consumerfinance.gov/credit-cards/agreements/issuer/bank-of-america/" URL
  And I should find the text "Agreements by 'Bank of America'" on the page
