Feature: Leadership calendar page
  As a public visitor to consumerfinance.gov
  I want to navigate through different available months
  So that I can view leadership events for various months

@smoke_testing
Scenario: Reach the Leadership calendar page from the menu link to verify the anchor tag is NOT displayed at this point
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "PARTICIPATE" menu to access "Leadership calendar"
  Then I should be directed to the "www.consumerfinance.gov/leadership-calendar/" URL

Scenario: In the Leadership calendar page, click previous/next month buttons to verify the anchor tag IS displayed
  # Click Previous month
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "PARTICIPATE" menu to access "Leadership calendar"
    And I click on the "previous" month button
  Then I should see "#calendar-anchor" in the leadership calendar URL
  # Click Previous then click Next month
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "PARTICIPATE" menu to access "Leadership calendar"
    And I click on the "previous" month button
    And I click on the "next" month button
  Then I should see "#calendar-anchor" in the leadership calendar URL

Scenario: In the Leadership calendar page, click previous button TWICE to verify the previous month is displayed
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "PARTICIPATE" menu to access "Leadership calendar"
  Then I should see the previous month displayed when I click on previous month button twice