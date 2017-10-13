Feature: 
As content editor in Wagtail
I should be able to add pre-defined snippets of text that can be reused on multiple pages

Background:
	Given that I am logged into Wagtail as an admin
	And I open the snippets menu
	And I open the Reusable texts list
	And I add a new snippet with title and sidefoot heading "Snippet 1" and placeholder text

Scenario: Create a new snippet
	When I click on Add Reusable text
	And I type "Snippet test" in the Snippet title field
	And I type "Snippet test" in the Sidefoot heading field
	And I type "This is a test of snippets." in the Text field
	And I click Save
	Then the new snippet should be created, and show in the snippet list.

Scenario: Edit a snippet title
	When I click on Snippet 1 in the list of snippets
	And I type "Snippet 1 edit" in the Snippet title field
	And I click Save
	Then the snippet title should now be "Snippet 1 edit"

Scenario: Edit a snippet sidefood heading
	When I click on Snippet 1 in the list of snippets
	And I type "Snippet heading edit" in the Sidefoot heading field
	And I click Save
	Then the snippet sidefoot heading should now be "Snippet heading edit"

Scenario: Edit snippet text
	When I click on Snippet 1 in the list of snippets
	And I type "This is a test of editing snippet text." in the Text field
	And I click Save
	Then the snippet text should now be "This is a test of editing snippet text."

Scenario: Add a snippet to a page
	When I create a new Wagtail Learn page with the title "Snippet test"
	And I open the Sidebar tab
	And I open the Sidefoot menu
	And I add a Reusable text module
	And I click on Add reusable text
	And I select Snippet 1 from the list of snippets
	And I publish the page
	And I goto URL "/snippet-test"
	Then the text of Snippet 1 should appear in the sidebar of the page.





