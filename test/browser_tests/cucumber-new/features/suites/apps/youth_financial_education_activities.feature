Feature: Verify financial literacy activities page works according to requirements
  As a first time visitor to the financial literacy activities page
  I want to Search for activities on the page
  So that I can find the information I'm looking for

Background:
  Given I navigate to the financial literacy activities page

@smoke_testing @activities @block
Scenario Outline: Search for building block activities
  Given I navigate to the financial literacy activities page
  When I enter search activity finance
  Then I check building block <name> for activity
  And I click on the "Search" activity button
  Then I should find the text "<name>" on the page
Examples:
| name                                           |
| Executive function                             |
| Financial habits and norms                     |
| Financial knowledge and decision-making skills |

@smoke_testing @activities @school
Scenario Outline: Search for school subject activities
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I check school subject <name> for activity
  And I click on the "Search" activity button
Examples:
| name                                 |
| CTE (Career and technical education) |
| English or language arts             |
| Fine arts and performing arts        |
| Math                                 |
| Physical education or health         |
| Science                              |
| Social studies or history            |
| World languages                      |

@smoke_testing @activities @topic
Scenario Outline: Search for activities per topic
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I click topic <name> for activity
  And I click on the "Search" activity button
  Then I should find the text "<name>" on the page
Examples:
| name            |
| Earn            |
| Save and invest |
| Protect         |
| Spend           |
| Borrow          |

@smoke_testing @activities @level
Scenario Outline: Search for activities per grade level
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I check grade level <name> for activity
  And I click on the "Search" activity button
  Then I should find the text "<name>" on the page
Examples:
| name                |
| Middle school (6-8) |
| High school (9-10)  |
| High school (11-12) |

@smoke_testing @activities @age
Scenario Outline: Search for activities for an age range
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I check age range <name> for activity
  And I click on the "Search" activity button
Examples:
| name  |
| 11-14 |
| 13-15 |
| 16-19 |

@smoke_testing @activities @student
Scenario Outline: Search for student characteristic activities
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I check student characteristic <name> for activity
  And I click on the "Search" activity button
Examples:
| name                      |
| English language learners |
| Special education         |
| Low income                |
| Rural                     |
| Urban                     |

@smoke_testing @activities @type
Scenario Outline: Search for activities for a characteristic type
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I check activity characteristic type <name>
  And I click on the "Search" activity button
Examples:
| name        |
| Individual  |
| Small group |
| Whole class |

@smoke_testing @activities @strategy
Scenario Outline: Search for activities for a teaching strategy
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I check teaching strategy <name> for activity
  And I click on the "Search" activity button
Examples:
| name                      |
| Blended learning          |
| Competency-based learning |
| Cooperative learning      |
| Direct instruction        |
| Gamification              |
| Personalized instruction  |
| Project-based learning    |
| Simulation                |

@smoke_testing @activities @bloom
Scenario Outline: Search for activities per Bloom's Taxonomy level
  Given I navigate to the financial literacy activities page
  When I enter search activity tax
  Then I check Blooms Taxonomy level <name> for activity
  And I click on the "Search" activity button
Examples:
| name       |
| Remember   |
| Understand |
| Apply      |
| Analyze    |
| Evaluate   |
| Create     |

@smoke_testing @activities @duration
Scenario Outline: Search for activities for a duration
  Given I navigate to the financial literacy activities page
  When I enter search activity money
  Then I check activity duration <name>
  And I click on the "Search" activity button
  Then I should find the text "<name>" on the page
Examples:
| name          |
| 15-20 minutes |
| 45-60 minutes |
| 75-90 minutes |

@smoke_testing @activities @standard
Scenario Outline: Search for activities for a National Standard
  Given I navigate to the financial literacy activities page
  When I enter search activity economic
  Then I check National Standard <name> for activity
  And I click on the "Search" activity button
Examples:
| name                                   |
| Standard I. Earning income             |
| Standard II. Buying goods and services |
| Standard III. Saving                   |
| Standard IV. Using credit              |
| Standard V. Financial investing        |
| Standard VI. Protecting and insuring   |

@smoke_testing @activities @coalition
Scenario Outline: Search for Jump Start Coalition activities
  Given I navigate to the financial literacy activities page
  When I enter search activity coalition
  Then I check Jump Start Coalition <name> for activity
  And I click on the "Search" activity button
Examples:
| name                          |
| Spending and saving           |
| Credit and debt               |
| Employment and income         |
| Investing                     |
| Risk management and insurance |
| Financial decision-making     |
