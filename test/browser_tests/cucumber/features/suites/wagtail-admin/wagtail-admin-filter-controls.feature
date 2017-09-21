Feature: Wagtail admin filter controls
As a user of Wagtail
I should be able to customize the display of filterable list controls

Background:
	Given that I am logged into Wagtail as an admin
	And I create a Wagtail browse filterable page with the title “browse filter test”
	And I add a child blog post with the title and heading "test post 1" and placeholder content, including post preview description and image, and publish it
	And I add a child blog post with the title and heading "test post 2" and placeholder content, including post preview description and image, and publish it
	And I open the content menu
	And I add a filter control module

Scenario: Filter label
	When I type “Filter posts” in the Label input box
	And I publish the page
	And I goto URL “/browse-filter-test”
	The filterable list control should have the label “Filter posts”

Scenario: Expand filter
	When I check the “is expanded” checkbox
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the filterable list control should be expanded by default

Scenario: Filter title
	When I uncheck the "filter title" checkbox
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the filterable list control should not contain an "item name" search box

Scenario: Post date description
	When I type "Date published" in the post date description input field
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the date for each child post should read "Date published [date]"

Scenario: Remove category filter
	When I uncheck the Filter category checkbox
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the filterable list control should not contain a column for category filtering

Scenario: Remove topic filter
	When I uncheck the Filter Topics checkbox
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the filterable list control should not contain a topic input field

Scenario: Remove author filter
	When I uncheck the Filter Authors checkbox
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the filterable list control should not contain an author input field

Scenario: Remove date range filter
	When I uncheck the Filter Date Range checkbox
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the filterable list control should not contain date range input fields

Scenario: Preview 50/50s
	When I check the Render preview items as 50-50s checkbox
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the post previews should be displayed as 50/50 image and text components

Scenario: Link image and heading
	When I check the Link image and heading
	And I publish the page
	And I goto URL “/browse-filter-test”
	Then the post headings and the post preview images should link to the correct blog post page