Feature:
	As a user of Wagtail
	I expect to use page preview fields to set preview content for items listed on browse filterable pages

Background:
	Given that I am logged into Wagtail as an admin
	And I add a Wagtail Blog page to About Us/Blog with the title “Page preview test”
	And I open the page preview fields menu in the Configuration tab

Scenario: Add preview title
	When I type “This post is a test” in the Preview title input field
	And I publish the page
	And I goto URL “/about-us/blog/“
	Then the title of the post in the filterable list should be “This post is a test”

Scenario: Add preview subheading text
	When I type “preview subheading test” in the Preview subheading input field
	And I publish the page
	And I goto URL “/about-us/blog/“
	Then the subheading “preview subheading test” should appear below the title of the post

Scenario: Add preview description
	When I type “Description of this post goes here” in the Preview description input field
	And I publish the page
	And I goto URL “/about-us/blog/“
	Then the paragraph text reading “Description of this post goes here” should appear below the title of the post

Scenario: Add secondary link
	When I type “Secondary link text goes here” in the Secondary link text input field
	And I type “/about-us/“ in the Secondary link URL text input field
	And I publish the page
	And I goto URL “/about-us/blog/“
	Then a link pointing to https://www.consumerfinance.gov/about-us/ with text “Secondary link text goes here” should appear below the title of the post

Scenario: Add preview image
	When I choose an image using the Preview image selector
	And I publish the page
	And I goto URL “/about-us/blog/“
	Then the selected image should appear to the left of the of the title of the post
