Feature: Credit card agreement database
  As a consumer
  I want to review general terms and conditions, pricing, and fee information
  So that I can learn more about credit card agreements.

@ignore_chrome_Linux
Scenario: Reach the page listing credit card agreements from Bank of America in the database
  Given I visit the www.consumerfinance.gov/credit-cards/agreements/ URL
  When I select what I call the "card issuer" drop list and search "Bank of America" and choose first
  Then I should be directed to the "www.consumerfinance.gov/credit-cards/agreements/issuer/176/" URL
  And I should find the text "Agreements by 'Bank of America'" on the page

@smoke_testing
Scenario: Reach the page listing credit card agreements from NASA Federal Credit Union in the database
  Given I visit the www.consumerfinance.gov/credit-cards/agreements/ URL
  When I select what I call the "card issuer" drop list and search "nasa" and choose first
  Then I should be directed to the "www.consumerfinance.gov/credit-cards/agreements/issuer/41/" URL
  And I should find the text "Agreements by 'NASA Federal Credit Union'" on the page

@smoke_testing
Scenario: Reach the Credit card agreement database page through the menu
  Given I visit the www.consumerfinance.gov homepage
  When I use the "PARTICIPATE" menu to access "Credit cards"
  Then I should be directed to the "www.consumerfinance.gov/credit-cards/knowbeforeyouowe/" URL
  When I click on the "Credit Card Agreement Database" link
  Then I should be directed to the "www.consumerfinance.gov/credit-cards/agreements/" URL
  And I should see the page title as "Credit card agreement database > Consumer Financial Protection Bureau"
