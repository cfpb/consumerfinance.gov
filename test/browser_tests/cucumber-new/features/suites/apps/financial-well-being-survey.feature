Feature: Verify financial well-being survey page works according to requirements
  As a first time visitor to the financial well-being survey page
  I want to Answer ten questions to measure my current financial well-being
  So that I can see steps for me to take to improve it

@s1 @age18-61 @Never
Scenario: Financial Well-being survey 1 for age range 18-61
  Given I visit the consumerfinance consumer-tools/financial-well-being URL
  When I Click on "Completely" for question "I could handle a major unexpected expense"
  And I Click on "Completely" for question "I am securing my financial future"
  And I Click on "Not at all" for question "Because of my money situation, I feel like I will never have the things I want in life"
  And I Click on "Completely" for question "I can enjoy life because of the way I’m managing my money"
  And I Click on "Not at all" for question "I am just getting by financially"
  And I Click on "Not at all" for question "I am concerned that the money I have or will save won’t last"
  And I Click on "Never" for question "Giving a gift for a wedding, birthday or other occasion would put a strain on my finances for the month"
  And I Click on "Always" for question "I have money left over at the end of the month"
  And I Click on "Never" for question "I am behind with my finances"
  And I Click on "Never" for question "My finances control my life"
  And I Select my age group of "18-61"
  And I Select how I completed the questionnaire as "I read and answered the questions myself"
  And I click on the "Get my score" button on the financial well-being quiz
  Then I should find the text "Your score: 86" on the page
  And I should find the text "U.S. average: 54" on the page

@s2 @age18-61 @Always
Scenario: Financial Well-being survey 2 for age range 18-61
  Given I visit the consumerfinance consumer-tools/financial-well-being URL
  When I Click on "Not at all" for question "I could handle a major unexpected expense"
  And I Click on "Not at all" for question "I am securing my financial future"
  And I Click on "Completely" for question "Because of my money situation, I feel like I will never have the things I want in life"
  And I Click on "Not at all" for question "I can enjoy life because of the way I’m managing my money"
  And I Click on "Completely" for question "I am just getting by financially"
  And I Click on "Completely" for question "I am concerned that the money I have or will save won’t last"
  And I Click on "Always" for question "Giving a gift for a wedding, birthday or other occasion would put a strain on my finances for the month"
  And I Click on "Never" for question "I have money left over at the end of the month"
  And I Click on "Always" for question "I am behind with my finances"
  And I Click on "Always" for question "My finances control my life"
  And I Select my age group of "18-61"
  And I Select how I completed the questionnaire as "I read the questions to someone else and recorded their answers"
  And I click on the "Get my score" button on the financial well-being quiz
  Then I should find the text "Your score: 16" on the page

@s3 @age62+ @Very @Rarely
Scenario: Financial Well-being survey 3 for age range 62+
  Given I visit the consumerfinance consumer-tools/financial-well-being URL
  When I Click on "Very well" for question "I could handle a major unexpected expense"
  And I Click on "Very well" for question "I am securing my financial future"
  And I Click on "Very little" for question "Because of my money situation, I feel like I will never have the things I want in life"
  And I Click on "Very well" for question "I can enjoy life because of the way I’m managing my money"
  And I Click on "Very little" for question "I am just getting by financially"
  And I Click on "Very little" for question "I am concerned that the money I have or will save won’t last"
  And I Click on "Rarely" for question "Giving a gift for a wedding, birthday or other occasion would put a strain on my finances for the month"
  And I Click on "Often" for question "I have money left over at the end of the month"
  And I Click on "Rarely" for question "I am behind with my finances"
  And I Click on "Rarely" for question "My finances control my life"
  And I Select my age group of "62+"
  And I Select how I completed the questionnaire as "I read and answered the questions myself"
  And I click on the "Get my score" button on the financial well-being quiz
  Then I should find the text "Your score: 67" on the page

@s4 @age62+ @Very @Often
Scenario: Financial Well-being survey 4 for age range 62
  Given I visit the consumerfinance consumer-tools/financial-well-being URL
  When I Click on "Very little" for question "I could handle a major unexpected expense"
  And I Click on "Very little" for question "I am securing my financial future"
  And I Click on "Very well" for question "Because of my money situation, I feel like I will never have the things I want in life"
  And I Click on "Very little" for question "I can enjoy life because of the way I’m managing my money"
  And I Click on "Very well" for question "I am just getting by financially"
  And I Click on "Very well" for question "I am concerned that the money I have or will save won’t last"
  And I Click on "Often" for question "Giving a gift for a wedding, birthday or other occasion would put a strain on my finances for the month"
  And I Click on "Rarely" for question "I have money left over at the end of the month"
  And I Click on "Often" for question "I am behind with my finances"
  And I Click on "Often" for question "My finances control my life"
  And I Select my age group of "62+"
  And I Select how I completed the questionnaire as "I read the questions to someone else and recorded their answers"
  And I click on the "Get my score" button on the financial well-being quiz
  Then I should find the text "Your score: 42" on the page

@s5 @age18-61 @Somewhat @Sometimes
Scenario: Financial Well-being survey 5 for age range 18-61
  Given I visit the consumerfinance consumer-tools/financial-well-being URL
  When I Click on "Somewhat" for question "I could handle a major unexpected expense"
  And I Click on "Somewhat" for question "I am securing my financial future"
  And I Click on "Somewhat" for question "Because of my money situation, I feel like I will never have the things I want in life"
  And I Click on "Somewhat" for question "I can enjoy life because of the way I’m managing my money"
  And I Click on "Somewhat" for question "I am just getting by financially"
  And I Click on "Somewhat" for question "I am concerned that the money I have or will save won’t last"
  And I Click on "Sometimes" for question "Giving a gift for a wedding, birthday or other occasion would put a strain on my finances for the month"
  And I Click on "Sometimes" for question "I have money left over at the end of the month"
  And I Click on "Sometimes" for question "I am behind with my finances"
  And I Click on "Sometimes" for question "My finances control my life"
  And I Select my age group of "18-61"
  And I Select how I completed the questionnaire as "I read and answered the questions myself"
  And I click on the "Get my score" button on the financial well-being quiz
  Then I should find the text "Your score: 50" on the page

@s6 @age62+ @Somewhat @Sometimes
Scenario: Financial Well-being survey 6 for age range 62+
  Given I visit the consumerfinance consumer-tools/financial-well-being URL
  When I Click on "Somewhat" for question "I could handle a major unexpected expense"
  And I Click on "Somewhat" for question "I am securing my financial future"
  And I Click on "Somewhat" for question "Because of my money situation, I feel like I will never have the things I want in life"
  And I Click on "Somewhat" for question "I can enjoy life because of the way I’m managing my money"
  And I Click on "Somewhat" for question "I am just getting by financially"
  And I Click on "Somewhat" for question "I am concerned that the money I have or will save won’t last"
  And I Click on "Sometimes" for question "Giving a gift for a wedding, birthday or other occasion would put a strain on my finances for the month"
  And I Click on "Sometimes" for question "I have money left over at the end of the month"
  And I Click on "Sometimes" for question "I am behind with my finances"
  And I Click on "Sometimes" for question "My finances control my life"
  And I Select my age group of "62+"
  And I Select how I completed the questionnaire as "I read the questions to someone else and recorded their answers"
  And I click on the "Get my score" button on the financial well-being quiz
  Then I should find the text "Your score: 53" on the page
