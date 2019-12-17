#Feature: Paying for college
#  As a prospective college student
#  I want to understand college finance
#  So I can make informed financial decisions about paying for college
Feature: As a student I want accurate data about that school's costs so that I can make a better comparison.

@t1 @pfc
Scenario: Compare a public to a private 4-year university
  Given I visit the cost comparison tool
  And I remove all schools
  When I add a public 4-year university
  And I add a private 4-year university
  Then I should see cost of attendance per year left to pay as "$29,526" and "$33,901"

@pfc
Scenario: Get Started
  Given I visit the cost comparison tool
  When I add a public 4-year university

@pfc
Scenario: As a student with a financial offer, I want to enter my own data so I have the most accurate picture of my options
  Given I visit the cost comparison tool
  When I add a public 4-year university
  And I check the box saying I have a financial aid offer
  Then I should end up at the financial aid offer success screen

@ignore
Scenario: Student has a financial aid offer and has XML to enter
  Given I visit the cost comparison tool
  When I add a public 4-year university
  And I check the box saying I have a financial aid offer
  And I enter XML data
  Then I should end up at the success without-auto-populated data screen
  And the form should auto-populate with the XML data

@ignore
Scenario: Student has XML but it is malformed

@ignore
Scenario: As a business owner, I want to know that if we do not have data, the tool does not autopopulate
  Given I visit the cost comparison tool
  When I add a school we do not have data for
  Then I should be taken to the unable-to-autopopulate success screen

@ignore
Scenario Outline: Auto-populate costs for a 4-year public university different housing and residency options
  Given I visit the cost comparison tool
  When I add a public school with <residency> tuition and <housing> housing options
    # begin typing
    # choose the school from the autocomplete list
    # fix degree type to bachelors
    # fix program length to 4 year
    # Click continue
    # click in-state
    # click on-campus
  Then I should see the auto-populated success screen and the proper data loaded into the form
Examples:
| residency   | housing    |
| in-state    | on-campus  |
| out-state   | on-campus  |
| in-district | on-campus  |
| in -state   | off-campus |
| out-state   | off-campus |
| in-district | off-campus |
| in-state    | family     |
| out-state   | family     |
| in-district | family     |

@ignore
Scenario Outline: Auto-populate costs for a 4-year private university
  Given I visit the cost comparison tool
  When I add a private school with <housing> housing
  Then I should see the auto-populated success screen and the proper data loaded into the form 
Examples:
| housing    |
| off-campus |
| on-campus  |
| family     |

@pfc @repaying-student-debt
Scenario Outline: Answering questions about repaying student debt
  Given I visit the "www.consumerfinance.gov/paying-for-college/repay-student-debt/" URL
  When I select <answer1> for question "1"
    And I select <answer2> for question "2"
    And I select <answer3> for question "3" (if applicable)
    And I select <answer4> for question "4" (if applicable)
    And I select <answer5> for question "5" (if applicable)
    And I select <answer6> for question "6" (if applicable)
    And I select <answer7> for question "7" (if applicable)
  Then I should see the module for <module_to_load>
Examples:
| answer1 | answer2 | answer3 | answer4 | answer5 | answer6 | answer7 | module_to_load                     |
| Federal | Yes     | Yes     | Yes     | Yes     | n/a     | n/a     | Federal direct consolidation loans |
| Federal | Yes     | Yes     | Yes     | No      | Yes     | n/a     | Rehabilitation                     |
| Federal | Yes     | Yes     | Yes     | No      | No      | Yes     | Repay Your Loan                    |
| Federal | Yes     | Yes     | Yes     | No      | No      | No      | Know Your Options                  |
