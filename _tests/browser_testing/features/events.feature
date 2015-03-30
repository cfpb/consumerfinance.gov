Feature: Test the listing of events and navigation to individual event pages.
  As a first time visitor to the Events page
  I want to click on events that interest me
  So that I can attend an event and learn more about what CFPB does

Background:
  Given I navigate to the "Events" page

@events
Scenario Outline: Test that the proper number of events show up
  Then I should see "10" events on the page

@events
Scenario Outline: Test that clicking on individual events navigates to proper page
  When I click on the "<link_name>" link
  Then I should be directed to the internal "<relative_url>" URL
  And I should see "<page_title>" displayed in the page title

Examples:
  | link_name          |  relative_url          | page_title           |
  | Explainer: How small businesses play a role in the rulemaking process | /events/explainer-how-small-businesses-play-a-role-in-the-rulemaking-process/ | TITLE Spring 2014 rulemaking agenda  - cfgov-refresh demo |
  | Live from Newark! | /events/live-from-newark/ | TITLE Spring 2014 rulemaking agenda  - cfgov-refresh demo |

@events
Scenario Outline: Test that event tags are displaying
  Then I should see "<tag>" displayed under "<event_name>"

Examples:
  | tag_1         | event_name               |
  | FIELD HEARING | Save the date, Richmond! |
  | PAYDAY LOANS  | Save the date, Richmond! |
  | ARBITRATION   | Live from Newark!        |
  | FIELD HEARING | Live from Newark!        |

@events
Scenario Outline: Test that the location, date, and time are displaying properly
  Then I should see "<location>" displayed under "<event_name>"
  And I should see "<date>" displayed under "<event_name>"
  And I should see "<time>" displayed under "<event_name>"

Examples:
  | location       | date     | time         | event_name               |
  | Washington, DC | 03/26/15 | 09:00 AM UTC | Live from Richmond!      |
  | Washington, DC | 03/11/15 | 02:00 PM UTC | Save the date, Richmond! |