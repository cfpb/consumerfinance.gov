Feature:
  As a user of Wagtail
  I should be able to trust that only published pages are live

  Background:
    Given I am logged into Wagtail as an admin

  Scenario: Page never published
    When I create a draft Browse Page with title "Publish Unpublish 1"
    And I goto URL "/publish-unpublish-1"
    Then I should see page title "404 error: not found"

  Scenario: Page published
    When I create a draft Browse Page with title "Publish Unpublish 2"
    And I publish the page
    And I goto URL "/publish-unpublish-2"
    Then I should see page title "Publish Unpublish 2 | Consumer Financial Protection Bureau"

  Scenario: Page published then unpublished
    When I create a draft Browse Page with title "Publish Unpublish 3"
    And I publish the page
    And I navigate back to the edit page
    And I unpublish the page
    And I goto URL "/publish-unpublish-3"
    Then I should see page title "404 error: not found"
