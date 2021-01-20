Feature: Verify the Home page works according to requirements
As a first time visitor to the Owning a Home page
I want to navigate the home page
So that I can find the information I'm looking for

Background:
  Given I navigate to the OAH Landing page


@smoke_testing @landing_page @email_signup
Scenario: Testing valid email signup
  When I enter "test@yahoo.com"
    And I click the Signup button
  Then I should see "Thanks, we’ll be in touch!" displayed
    And I should see the Signup button disappear


@landing_page @email_signup
Scenario: Testing multiple validation messages
  When I enter "zz"
    And I click the Signup button
    And I click the Signup button again
    And I click the Signup button again
  Then I should NOT see multiple "Thanks, we’ll be in touch!" messages displayed


@landing_page @email_signup
Scenario Outline: Testing invalid email address
  When I enter "<email_address>"
    And I click the Signup button
  Then I should NOT see "Thanks, we’ll be in touch!" displayed

Examples:
| email_address |
| testyahoo.com |
| 11@           |
| @@            |
| 11.com        |
