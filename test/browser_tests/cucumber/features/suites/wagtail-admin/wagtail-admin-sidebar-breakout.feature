Feature: As a user of Wagtail
	I should able to use the sidebar breakout to keep some sidebar content visible above the main page content at mobile sizes

Background:
	Given that the browser window is at least 1000 pixels wide
	And I create a Wagtail Sublanding page with the title “Breakout test”
	And I add a text introduction module with heading “Sidebar breakout test page”
	And I add a paragraph of full-width placeholder text 
	And I add a heading module to the sidebar breakout with the heading "Breakout heading"

Scenario: Sidebar breakout only
	When I publish the page
	And I goto URL “/breakout-test/“
	Then the text “Breakout heading” should be displayed to the right of the page heading “Sidebar breakout test page”
	And when I resize the browser to be 700 pixels wide
	Then the text “Breakout heading” should be displayed in between the page heading and the paragraph of placeholder text

Scenario: Sidebar content with breakout
	When I add a contact module to the sidefoot
	And I choose a contact snippet
	And I publish the page
	And I goto URL “/breakout-test/“
	Then the text “Breakout heading” should be displayed to the right of the page heading “Sidebar breakout test page” and the contact information should be displayed with a gray background to the right of the paragraph of placeholder text
	And when I resize the browser to be 700 pixels wide
	Then the text “Breakout heading” should be displayed in between the page heading and the placeholder text
	And the contact information should be displayed below the placeholder text