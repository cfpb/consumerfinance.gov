Feature: System behavior for wagtail post types
  As a wagtail developer
  I want to execute a set of post type tests
  So that I can be sure that they system works properly

@wagtail @newsroom_deploy @wagtail_post_types @smoke_testing
Scenario Outline: Check all post types to ensure they are still registered and their archives load properly
  Given I visit the "www.consumerfinance.gov/<post_type>" URL
  Then I should see the page title as "<title> > Consumer Financial Protection Bureau"
  And I should find the text "<sidebar_top>" on the page
  And I should find the text "<sidebar_bottom>" on the page
  And I should find the text "<meta_information>" on the page
  And I should find the text "<archive_output>" on the page

Examples:
| post_type   | sidebar_top    | sidebar_bottom            | meta_information                              | archive_output                    | title           |
#| regulations | Implementation | QUESTIONS                 | OTHER NOTICES                                 | May 29                            | Regulations     |
#| reports     | Reports        | READ MORE                 | ‹ OLDER POSTS                                 | READ MORE                         | Reports Archive |
| amicus      | Amicus program | SUGGESTIONS               | BRIEFS FILED IN THE FEDERAL COURTS OF APPEALS | BRIEFS FILED IN THE SUPREME COURT | Amicus program  |
#| newsroom    | Newsroom       | press@consumerfinance.gov | Press Release                                 | Topic                             | Newsroom        |
