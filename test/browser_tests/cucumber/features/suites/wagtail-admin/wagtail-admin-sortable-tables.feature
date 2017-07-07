
Feature: Rich Text Editor
  As a user of Wagtail
  I should be able to set sortable options on a table

  Background:
    Given I am logged into Wagtail as an admin
    And I create a Wagtail Browse Page
    And I open the content menu
    And I select the table block option
    And I select the Row header option
    And I enter "Example 1" in the first column of the first row
    And I enter "Example 2" in the second column of the first row
    And I enter "Example 3" in the third column of the first row

  Scenario: Turn on sortable tables
    When I check the "Sortable table" option
    Then the editor should display the "Sortable Table Options" table

  Scenario: Select Alphabetical sorting
    When I select the Alphabetical option for the first column
    Then "Example 1" should be wrapped in a button tag with a data-sort_type="string" attribute

  Scenario: Select Numerical
    When I select the Alphabetical option for the second column
    Then "Example 2" should be wrapped in a button tag with a data-sort_type="number" attribute

  Scenario: Select None
    When I select the None option for the third column
    Then "Example 3" should be wrapped in a p tag
