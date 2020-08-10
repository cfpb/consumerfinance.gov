Feature: Test the default values in the Closing Disclosure page
  As a first time visitor to the Owning a Home page
  I want to have content loaded
  So that I can get clever and conquer the world

Background:
  Given I navigate to the "Closing Disclosure" page


@closing_disclosure @smoke_testing
Scenario Outline: Test that tabs are on the page
  Then I should see "<tab_name>" tab

Examples:
| tab_name    |
| Checklist   |
| Definitions |


@closing_disclosure
Scenario Outline: Test that the content is loaded
  When I click the tab "<tab_name>"
  Then Content image is loaded

Examples:
| tab_name    |
| Checklist   |
| Definitions |


@closing_disclosure
Scenario Outline: Test that resizing window size changes image size too
  When I click the tab "<tab_name>"
    When I resize window image "<css_selector>" size changes too

Examples:
| tab_name    | css_selector        |
| Checklist   | img.image-map_image |
| Definitions | img.image-map_image |


@closing_disclosure
Scenario Outline: Test that expandable explainers are loaded
  When I click the tab "<tab_name>"
  Then Expandable explainers for "<tab_name>" are loaded
    And Expandable explainers for tab other than "<tab_name>" are invisible

Examples:
| tab_name    |
| Checklist   |
| Definitions |


@closing_disclosure
Scenario Outline: Test overlays/highlights
  When I click the tab "<tab_name>"
    When I hover over an overlay the corresponding explainer has class hover-has-attention

Examples:
| tab_name    |
| Checklist   |
| Definitions |


@closing_disclosure
Scenario Outline: Test overlays/highlights
  When I click the tab "<tab_name>"
    When I click an overlay the corresponding explainer has class has-attention

Examples:
| tab_name    |
| Checklist   |
| Definitions |


@closing_disclosure
Scenario Outline: Test pagination
  When I click on page "<page_num>"
  Then page "<page_num>" is displayed

Examples:
| page_num |
| 1        |
| 2        |
| 3        |
| 4        |
| 5        |
| 1        |


@closing_disclosure
Scenario Outline: Test Next Page
  When I click page "<current_num>" in Form Explainer
    And I click the next button in page "<current_num>"
  Then page "<page_num>" is displayed

Examples:
| current_num | page_num |
| 1           | 2        |
| 2           | 3        |
| 3           | 4        |
| 4           | 5        |


@closing_disclosure
Scenario Outline: Test Prev Page
  When I click page "<current_num>" in Form Explainer
   And I click the previous button in page "<current_num>"
  Then page "<page_num>" is displayed

Examples:
| current_num | page_num |
| 5           | 4        |
| 4           | 3        |
| 3           | 2        |
| 2           | 1        |


@404 @closing_disclosure
Scenario Outline: Testing availability of pages on Closing Disclosure
  Given I navigate to the "<page_name>" page
  Then Links are working without 404 errors

Examples:
| page_name          |
| Closing Disclosure |

