
Feature: Wagtail Login
  As a user of Wagtail
  I should be able to login to the admin section

  Scenario: Logging into the admin
  	Given I goto /login
    When I enter my login criteria
    Then I should be able to access the admin section
