Feature: related posts
	As a user of Wagtail
	I expect to add related posts to the sidebar or sidefoot of a page that are populated automatically based on topic tags and post category

# These tests assume that some posts exist in order to populate the related posts based on category and tags. The tests require at least 3 blog posts, 3 newsroom posts, and 3 event posts tagged with "mortgages." At least 2 of the blog posts should be in the "Info for consumers" category and 1 in a different blog category. At least 2 of the newsroom posts should be in the "press release" category and 1 should be in a different category. At least 1 post of each type should be tagged only with "complaints," and 1 post of each type should be tagged with both "mortgages" and "complaints."
	 
Background:
	Given that I am logged into Wagtail as an admin
	And I create a Wagtail Browse page with the title “Related posts”
	And I enter “mortgages” in the tags field of the configuration tab
	And I open the sidefoot menu in the sidebar tab
	And I add a related posts module 

Scenario: Add related posts
	When I publish the page
	And I goto URL “/related-posts”
	Then I should see 3 blog posts, 3 newsroom posts, and 3 events tagged ”mortgages” in the sidefoot

Scenario: Add only blog posts
	When I check the blog posts check box
	And I uncheck the newsroom check box
	And I uncheck the events check box
	And I publish the page
	And I goto URL “/related-posts”
	Then I should see 3 blog posts tagged “mortgages” in the sidefoot

Scenario: Add only newsroom items
	When I check the newroom check box
	And I uncheck the blog posts check box
	And I uncheck the events check box
	And I publish the page
	And I goto URL  “/related-posts”
	Then I should see 3 newsroom posts tagged “mortgages” in the sidefoot

Scenario: Add posts by specific category
	When I select “Info for consumers” from the specific categories dropdown
	And I click the add another button
	And I select  “Press release” from the second specific categories dropdown
	And I publish the page
	And I goto URL “/related-posts”
	Then I should see only blog posts tagged “mortgages” and in the “Info for consumers” category, and only newsroom posts tagged “mortgages” and in the “press release” category in the sidefoot

Scenario: Add multiple tags
	When I enter “complaints” in the tags field of the configuration tab
	And I publish the page
	And I goto URL “/related-posts”
	Then I should see 3 blog posts, 3 newsroom posts, and 3 events tagged either “mortgages” or “complaints” in the sidefoot

Scenario: Match all topic tags
	When I enter “complaints” in the tags menu of the configuration tab
	And I check the “match all topic tags” check box in the related posts module in the sidebar tab
	And I publish the page
	And I goto URL “/related-posts-1”
	Then I should see only posts and events tagged with both “mortgages” and “complaints” in the sidefoot

Scenario: Change the number of related posts
	When I enter “2” in the limit input box
	And I publish the page
	And I goto URL “/related-posts”
	Then I should see 2 blog posts, 2 newsroom posts and 2 events tagged with “mortgages” in the sidefoot

Scenario: Remove heading and icon
	When I uncheck the Show Heading and Icon? check box
	And I publish the page
	And I goto URL “/related-posts”
	Then I should see 3 blog posts, 3 newsroom posts and 3 events tagged with ”mortgages” in the sidefoot, with no heading or minicon above either set of posts