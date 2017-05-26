
Feature: Rich Text Editor
  As a user of the Rich Text Editor
  I should be able to use all the elements

  Background:
    Given I am logged into Wagtail as an admin
    And I create a Wagtail Sublanding Page
    And I open the content menu
    And I select the full width text organism
    And I select the content element

  Scenario: Insert Text into the editor
    When I insert "Testing text insertion" into the rich text editor
    Then the rich text editor should contain "Testing text insertion"

  Scenario: Bold Text
    When I insert "Testing bold text" into the rich text editor
    And I select the text in the rich text editor
    And I click the bold button in the rich text editor
    Then "Testing bold text" should be wrapped in a b tag

  Scenario: Italicize Text
    When I insert "Testing italic text" into the rich text editor
    And I select the text in the rich text editor
    And I click the italic button in the rich text editor
    Then "Testing italic text" should be wrapped in a i tag

  Scenario: H2 Text
    When I insert "Testing H2 text" into the rich text editor
    And I select the text in the rich text editor
    And I click the H2 button in the rich text editor
    Then "Testing H2 text" should be wrapped in a h2 tag

  Scenario: H3 Text
    When I insert "Testing H3 text" into the rich text editor
    And I select the text in the rich text editor
    And I click the H3 button in the rich text editor
    Then "Testing H3 text" should be wrapped in a h3 tag

  Scenario: H4 Text
    When I insert "Testing H4 text" into the rich text editor
    And I select the text in the rich text editor
    And I click the H4 button in the rich text editor
    Then "Testing H4 text" should be wrapped in a h4 tag

  Scenario: H5 Text
    When I insert "Testing H5 text" into the rich text editor
    And I select the text in the rich text editor
    And I click the H5 button in the rich text editor
    Then "Testing H5 text" should be wrapped in a h5 tag

  Scenario: OL Text
    When I insert "Testing OL element" into the rich text editor
    And I select the text in the rich text editor
    And I click the ol button in the rich text editor
    Then "Testing OL element" should be wrapped in a ol tag

  Scenario: UL Text
    When I insert "Testing UL element" into the rich text editor
    And I select the text in the rich text editor
    And I click the ul button in the rich text editor
    Then "Testing UL element" should be wrapped in a ul tag

  Scenario: HR element
    When I click the hr button in the rich text editor
    Then the rich text editor should contain a hr element

  Scenario: Undo Text
    When I insert 12345 into the rich text editor
    Then the rich text editor should contain 12345
    And I click the undo button in the rich text editor
    Then the rich text editor should contain 1

  Scenario: Redo Text
    When I insert 12345 into the rich text editor
    Then the rich text editor should contain 12345
    And I click the undo button in the rich text editor
    Then the rich text editor should contain 1
    And I click the redo button in the rich text editor
    Then the rich text editor should contain 12345
