Feature: Reusable Text Snippets
  As a user of cf.gov
  I expect to see a consistent snippet of reusable text
  When it is added to a page

  Background:
    Given I goto URL "/rts"
    #NOOP And I have added one or more reusable text snippets to the page
    #NOOP And those snippets have text "This is the text of a reusable snippet."

  Scenario: sidefoot_heading has NOT been entered
    And there exists a reusable text snippet on this page
    #NOOP And the sidefoot_heading field of that snippet is empty
    Then the snippet output shouldn't include a slug-style header

  Scenario: sidefoot_heading HAS been entered
    And there exists a reusable text snippet on this page
    #NOOP And the sidefoot_heading field of that snippet is not empty
    Then the snippet output should include a slug-style header
