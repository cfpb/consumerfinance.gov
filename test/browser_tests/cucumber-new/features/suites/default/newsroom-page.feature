Feature: Verify Newsroom page structure
  As a visitor to the Newsroom page
  I want to verify that the Newsroom page structure is correct
  So that clicking on individual links cause the correct Newsroom article to be displayed
  So that clicking on individual links/tags cause the correct page(s) to be displayed

@smoke_testing @newsroom
Scenario: Navigate menu to the Newsroom page, check the correct number of articles are displayed and verify the page header is correct
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
  Then I should see "15" articles listed in the Newsroom page
    And The "Newsroom" page header is correctly displayed in the Newsroom

@smoke_testing @newsroom
Scenario: Navigate menu to the Newsroom page, verify paragraph is not empty then click on the article to verify it loads the correct page
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
  Then The paragraph inside the Newsroom article is NOT empty
    And Clicking on a Newsroom article causes the correct article to be displayed

@wagtail @newsroom
Scenario: Navigate menu to the Newsroom page, verify the correct number of 'Type' tags are displayed
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
  Then  I should see at least "2" Type tags listed in the Newsroom sidebar

@wagtail @newsroom
Scenario: Navigate menu to the Newsroom page, verify the correct number of 'Topic' tags are displayed
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
    And I click "More »" to expand
  Then  I should see at least "2" Topic tags listed in the Newsroom sidebar

@wagtail @newsroom
Scenario: Navigate to the Newsroom page, click on a 'Type' tag and verify that the URL string includes the 'Type" selected'
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
  Then Clicking on a "TYPE" tag should display the correct tag in the URL query string

@wagtail @newsroom
Scenario: Navigate to the Newsroom page, click on a 'Topic' tag and verify that the URL string includes the 'Topic" selected'
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
  Then Clicking on a "TOPIC" tag should display the correct tag in the URL query string

@wagtail @newsroom
Scenario Outline: Navigate to the Newsroom page, click on a 'Type' tag, verify that articles with the selected 'Type' tag are displayed and the window title contains the selected 'Type' tag
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
    And I click on the "<type_tag>" button
  Then I should find at least 1 Newsroom post on the page
    And I should see the "<type_tag>" tag on the Newsroom TYPE post
    And I should see the page title as "<type_tag> > Newsroom > Consumer Financial Protection Bureau"

Examples:
| type_tag |
| Op-Ed    |

@wagtail @newsroom
Scenario Outline: Navigate to the Newsroom page, click on a 'Topic' tag, verify that articles with the selected 'Topic' tag are displayed and the window title contains the selected 'Topic' tag
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
    And I click "More »" to expand
    And I click on the "<topic_tag>" button
  Then I should find at least 1 Newsroom post on the page
    And I should see the "<topic_tag>" tag on the Newsroom TOPIC post
    And I should see the page title as "<topic_tag> > Newsroom > Consumer Financial Protection Bureau"
Examples:
| topic_tag |
| Mortgages |
 
@wagtail @newsroom
Scenario Outline: Ensure that selecting multiple TYPE tags works as expected
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
    And I click on the "<type_tag_1>" button
    And I click on the "<type_tag_2>" button
  Then I should see the "<type_tag_1>" tag on the Newsroom TYPE post
    And I should see the "<type_tag_2>" tag on the Newsroom TYPE post
    And I should see the page title as "<type_tag_2> and <type_tag_1> > Newsroom > Consumer Financial Protection Bureau"

Examples:
| type_tag_1 | type_tag_2 |
| Op-Ed      | Testimony  |

@wagtail @newsroom
Scenario Outline: Ensure that selecting multiple TOPIC tags works as expected
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
    And I click on the "<type_tag_1>" button
    And I click on the "<type_tag_2>" button
  Then I should see the "<type_tag_1>" tag on the Newsroom TOPIC post
    And I should see the "<type_tag_2>" tag on the Newsroom TOPIC post
    And I should see the page title as "<type_tag_2> and <type_tag_1> > Newsroom > Consumer Financial Protection Bureau"
Examples:
| type_tag_1 | type_tag_2 |
| Mortgages  | Banking    |

@wagtail @newsroom
Scenario Outline: Ensure that selecting one Type and one Topic tags works as expected
  Given I visit the "www.consumerfinance.gov/" URL
  When I use the "INSIDE THE CFPB" menu to access "Newsroom"
    And I click on the "<type_tag>" button
    And I click on the "<topic_tag>" button
  Then  I should see the "<topic_tag>" tag on the Newsroom TOPIC post
    And I should see the page title as "<type_tag> about <topic_tag> > Newsroom > Consumer Financial Protection Bureau"
Examples:
| type_tag | topic_tag |
| Op-Ed    | Mortgages |

@wagtail @newsroom_deploy
Scenario: Verify date archives work in the newsroom
  Given I visit the "www.consumerfinance.gov/newsroom/2013/10" URL
  Then I should see the page title as "October 2013 > Newsroom > Consumer Financial Protection Bureau"

@wagtail @newsroom_deploy
Scenario: Verify date archive pagination works in the newsroom
  Given I visit the "www.consumerfinance.gov/newsroom/2013/10/page/2" URL
  Then I should see the page title as "October 2013 > page 2 > Newsroom > Consumer Financial Protection Bureau"
