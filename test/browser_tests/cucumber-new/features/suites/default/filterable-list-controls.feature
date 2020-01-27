Feature: Filterable list controls
  As a visitor to cf.gov
  I expect to be able to filter lists based on the content relevant to me

# The tests assume some blog posts already exist, and will need some test post data if they're run locally.
# This includes at least one post that contains the word "loan" in the title, one post without the word "loan" in the title,
# posts published both before and after the date 01/01/2017. The posts should be in several different categories,
# and tagged with several different topic tags, including at least one with the tag "mortgages" and at least one without the "mortgages" tag.
# The posts should also have several different authors, including at least one with the author "CFPB Web Team".

Background:
  Given I goto URL "/about-us/blog/"
  And I open the filterable list control

@undefined
Scenario: Item name search
  When I enter "loan" in the item name input field
  And I apply filters
  Then I should see only results with the word "loan" in the post title

@undefined
Scenario: Select a category
  When I select a checkbox in the Category list
  And I apply filters
  Then I should see only results in that category

@undefined
Scenario: Select multiple categories
  When I select two checkboxes in the Category list
  And I apply filters
  Then I should see only results that are in at least one of the two selected categories

@undefined
Scenario: Date range to present
  When I enter "01/01/2017" in the From date entry field
  And I apply filters
  Then I should see only results dated 01/01/2017 or later

@undefined
Scenario: Date range in past
  When I enter "01/01/2016" in the From date entry field
  And I enter "01/01/2017" in the To date entry field
  Then I should see only results between 01/01/2016 and 01/01/2017, inclusive

@undefined
Scenario: Select a topic
  When I select a checkbox in the Topic list
  And I apply filters
  Then I should see only results tagged with the selected topic

@undefined
Scenario: Select multiple topics
  When I select two checkboxes in the Topic list
  And I apply filters
  Then I should see only results tagged with at least one of the two selected topics

@undefined
Scenario: Type-ahead topics
  When I type "mortgage" in the topic input box
  Then the list of topics should show only tags that contain the word "mortgage"
  And when I select a topic in the list
  And I apply filters
  Then I should see only results tagged with the selected topic

@undefined
Scenario: Select category and topic
  When I select a checkbox in the Category list
  When I select a checkbox in the Topic list
  And I apply filters
  Then I should see only results that are both in the selected category and tagged with the selected topic

@undefined
Scenario: Clear fliters
  When I select a checkbox in the Category list
  When I select a checkbox in the Topic list
  And I apply filters
  Then I should see only results that are both in the selected category and tagged with the selected topic
  And when I click "clear filters"
  Then I should see the full list of results

@undefined
Scenario: Select an author
  When I select a checkbox in the Author list
  And I apply filters
  Then I should see only results posted by the selected author

@undefined
Scenario: Select multiple authors
  When I select two checkboxes in the Author list
  And I apply filters
  Then I should see only results posted by at least one of the two selected authors

@undefined
Scenario: Type-ahead authors
  When I type "CFPB" in the Author input box
  Then the list of authors should show only items that contain "CFPB"
  And when I select a checkbox in the Author list
  And I apply filters
  Then I should see only results posted by the selected author

@undefined
Scenario: Name search plus category
  When I type "loans" in the item name input box
  And I select a checkbox in the Category list
  And I apply filters
  Then I should see only results in the selected category with "loans" in the post title

@undefined
Scenario: Name search plus topic
  When I type "loans" in the item name input box
  And I select a checkbox in the Topic list
  And I apply filters
  Then I should see only results tagged with the selected topic with "loans" in the post title

@undefined
Scenario: Name search plus date range
  When I type "loans" in the item name input box
  And I type "01/01/2017" in the From date entry field
  And I apply filters
  Then I should see only results dated 01/01/2017 or later with "loans" in the post title

@undefined
Scenario: Name search plus author
  When I type "loans" in the item name input box
  And I select a checkbox in the Author list
  And I apply filters
  Then I should see only results posted by the select author with "loans" in the post title
