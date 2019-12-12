Feature: consumerfinance.gov home page
  As a public visitor to consumerfinance.gov
  I want to view the home page and navigate its links
  So that I can interact with the CFPB and become a learned consumer

@smoke_testing
Scenario: Reach the Open government page from the footer link
  Given I visit the www.consumerfinance.gov homepage
  When I click on the "Open Government" link in the footer
  Then I should be directed to the "www.consumerfinance.gov/open-government/" URL
    And I should see the page title contains "Open Government"

@smoke_testing
Scenario: Reach the Home page using the CFPB logo link
  Given I visit the www.consumerfinance.gov homepage
  When I click on the "Open Government" link in the footer
    And I click on the CFPB logo image
  Then I should be directed to the homepage
    And I should see the page title is "Consumer Financial Protection Bureau"

@smoke_testing
Scenario: Reach the Open Government Activities page from the Open government page using the Open Government Activities link
  Given I visit the www.consumerfinance.gov homepage
  When I click on the "Open Government" link in the footer
    And I click on the "Learn how we adhere to open government policies" link
  Then I should be directed to the "www.consumerfinance.gov/open-government/our-open-government-activities/" URL
    And I should see the page title is "Our Open Government Activities | Consumer Financial Protection Bureau"
