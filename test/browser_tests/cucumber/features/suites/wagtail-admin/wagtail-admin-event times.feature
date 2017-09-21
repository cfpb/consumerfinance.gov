 Feature: As a user of Wagtail
 	I should be able to add a date and time to an event in Eastern time, and see the time displayed on the published page in Eastern time.
 
 Background:
 	Given that I am logged into Wagtail as admin
	And I create a Wagtail Event page with the title “Event date”

 Scenario: Publish event in EDT
	When I enter a start date of 2017-07-24 16:00 and an end date of 2017-07-24 18:00 
	 And I publish the page
	 And I goto URL “/event-date”
	 Then the event date on the page should read “Jul 24, 2017 @ 04:00 PM EDT”

Scenario: Publish event in EST
	When I enter a start date of 2017-011-24 16:00 and an end date of 2017-11-24 18:00 
	 And I publish the page
	 And I goto URL “/event-date”
	 Then the event date on the page should read “Nov 24, 2017 @ 04:00 PM EST”