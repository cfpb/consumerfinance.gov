Feature: Test the filtering of Newsroom posts
  As a first time visitor to the Newsroom page
  I want to filter the articles on the page
  So that I can better find the article(s) I'm looking for

Background:
  Given I navigate to the "Newsroom" page

@newsroom
Scenario Outline: Check that the Filter posts button is present
  When I navigate to the "Newsroom" page
  Then I should see the Filter posts button

@newsroom
Scenario Outline: Filter articles by category
  When I click the checkbox for "<category_name>"
    And I click Filter
  Then I should see "<results_number>" results

Examples:
  | category_name       | results_number |
  | Op-Ed               | 14             |
  | Press Release       | 5              |

@newsroom
Scenario Outline: Filter articles by topic search
  When I enter "<search_phrase>" into the topic search box
    And I click the "<topic_name>" option in the results
  Then I should see "<results_number>" results
    And I should see "<topic_name>" as the listed filter

Examples:
  | search_phrase       | topic_name        | results_number |
  | for                 | Foreclosure       | 5              |

@newsroom
Scenario Outline: Filter articles by author search
  When I enter "<search_phrase>" into the author search box
    And I click the "<author_name>" option in the results
  Then I should see "<results_number>" results
    And I should see "<author_name>" as the listed filter

Examples:
  | search_phrase       | author_name        | results_number |
  | bat                 | Batman             | 14             |

@newsroom
Scenario Outline: Filter articles by date published
  When I select "<from_month>" from the From Month dropdown
    And I select "<from_year>" from the From Year dropdown
    And I select "<to_month>" from the To Month dropdown
    And I select "<to_year>" from the To Year dropdown
  Then I should should see "<results_number>" results
    And I should see "<from_date>" as the listed From Date
    And I should see "<to_date>" as the listed To Date

Examples:
  | from_month    | from_year | to_month | to_year | results_number | from_date    | to_date       |
  | 01            | 2011      | 02       | 2011    | 9              | January 2011 | February 2011 |

@newsroom
Scenario Outline: Test that clicking Clear filters actually clears filters
  When I click the checkbox for "<category_name>"
    And I enter "<search_phrase>" into the topic search box
    And I click the "<topic_name>" option in the results
    And I enter "<author_search>" into the author search box
    And I click the "<author_name>" option in the results
    And I select "<from_month>" from the From Month dropdown
    And I select "<from_year>" from the From Year dropdown
    And I select "<to_month>" from the To Month dropdown
    And I select "<to_year>" from the To Year dropdown
    And I click Clear filters
  Then I should see 0 filters chosen
    And I should see the checkbox next so "<category_name>" unchecked

Examples:
| category_name | search_phrase | topic_name | author_search | author_name | from_month | from_year | to_month | to_year |

@newsroom
Scenario Outline: Test that the pagination displays properly
  When I click the checkbox for "<topic_name>"
    And I click Apply filters
  Then I should see Pagination is displayed

Examples:
 | topic_name |
 | Op-Ed      |

@newsroom
Scenario Outline: Test that the pagination doesn't display when it's not needed
  When I click the checkbox for "<topic_name>"
    And I click Apply filters
  Then I should not see Pagination displayed

Examples:
 | topic_name    |
 | Press Release |

@newsroom
Scenario Outline: Test that pagination works
  When I click the "<pagination_button>"
  Then I should see a Current page value of "<current_page>"

Examples:
  | pagination_button | current_page |
  | Next              | 2            |
  | 2                 | 2            |

@newsroom
Scenario Outline: Test that going backwards in pagination works
  When I click the Next button
    And I click the Previous button
  Then I should see a Current page value of 1
