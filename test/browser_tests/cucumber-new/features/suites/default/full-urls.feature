Feature: Verify that files use the fully qualified URL instead of the relative URL
  As a wagtail developer
  I want to execute a set of tests
  So that I can verify that resource files use the full URL

@wagtail @smoke_testing @image
Scenario Outline: Check all homepage images to verify they use the full URL
  Given I visit the www.consumerfinance.gov homepage
  Then I should find the "<relative_path>" image on the page

  Given I visit the "<relative_path>" URL
  Then I should be directed to the "www.consumerfinance.gov<relative_path>" URL
    And I should see the page title contains "<start_text>"

Examples:
| name    | relative_path                                              | start_text              |
| logo    | /wp-content/themes/cfpb_nemo/_/img/logo-vert.png           | logo-vert.png           |
| rss     | /wp-content/themes/cfpb_nemo/_/img/rss_footer_icon.png     | rss_footer_icon.png     |
| twitter | /wp-content/themes/cfpb_nemo/_/img/twitter_footer_icon.png | twitter_footer_icon.png |

# These fail inconsistently but frequently
@wagtail @image @flapper
Scenario Outline: Check all homepage images to verify they use the full URL
  Given I visit the www.consumerfinance.gov homepage
  Then I should find the "<relative_path>" image on the page

  Given I visit the "<relative_path>" URL
  Then I should be directed to the "www.consumerfinance.gov<relative_path>" URL
    And I should see the page title contains "<start_text>"

Examples:
| name     | relative_path                                              | start_text              |
#| facebook | /wp-content/themes/cfpb_nemo/_/img/fb_footer_icon.png      | fb_footer_icon.png      |
| flickr   | /wp-content/themes/cfpb_nemo/_/img/flickr_footer_icon.png  | flickr_footer_icon.png  |
| youtube  | /wp-content/themes/cfpb_nemo/_/img/youtube_footer_icon.png | youtube_footer_icon.png |
| logo     | /wp-content/themes/cfpb_nemo/_/img/logo.svg                | logo.svg                |

@wagtail @smoke_testing @header
Scenario Outline: Check all homepage resources to verify they use the full URL (base URL + relative path)
  Given I visit the "www.consumerfinance.gov/<page_url>" URL
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
    And I should find the "<tag>" resource "<relative_path>" on the page

  Given I visit the "<relative_path>" URL
  Then I should be directed to the "www.consumerfinance.gov<relative_path>" URL
    And I should see the page title contains "<contains_text>"

Examples:
| page_url                  | tag  | relative_path                                                               | contains_text                            |
|                           | link | /wp-content/themes/cfpb_nemo/_/img/apple-touch-icon-precomposed.png         | apple-touch-icon-precomposed.png         |
|                           | link | /wp-content/themes/cfpb_nemo/_/img/apple-touch-icon-72x72-precomposed.png   | apple-touch-icon-72x72-precomposed.png   |
|                           | link | /wp-content/themes/cfpb_nemo/_/img/apple-touch-icon-114x114-precomposed.png | apple-touch-icon-114x114-precomposed.png |
|                           | link | /wp-content/themes/cfpb_nemo/_/img/apple-touch-icon-144x144-precomposed.png | apple-touch-icon-144x144-precomposed.png |
|                           | link | /wp-content/themes/cfpb_nemo/_/c/woff.css                                   | woff.css                                 |
|                           | link | /wp-content/themes/cfpb_nemo/_/c/hp.css                                     | hp.css                                   |
|                           | link | /wp-content/themes/cfpb_nemo/_/c/styles.css                                 | styles.css                               |
#|                           | link | /wp-content/plugins/contact-form-7/includes/css/styles.css                  | styles.css                               |
| find-a-housing-counselor/ | link | /wp-content/themes/cfpb_nemo/_/c/hud-hca-api-print-style.css                | hud-hca-api-print-style.css              |
| find-a-housing-counselor/ | link | /wp-content/themes/cfpb_nemo/_/cfpb-icon-font/css/icons.css                 | icons.css                                |
| mortgage/                 | link | /wp-content/themes/cfpb_nemo/_/cfpb-icon-font/css/icons.css                 | cfpb-icon-font/css/icons.css             |

@wagtail @child
Scenario Outline: Check all child-page resources to verify they use the full URL (base URL + relative path)
  Given I visit the "www.consumerfinance.gov/<page_url>" URL
  Then I should find the "<relative_path>" image on the page

  Given I visit the "<relative_path>" URL
  Then I should see the page title contains "<contains_text>"

Examples:
| page_url    | relative_path                                              | contains_text           |
#| the-bureau/ | /wp-content/themes/cfpb_nemo/_/img/icon_small_facebook.png | icon_small_facebook.png |
| the-bureau/ | /wp-content/themes/cfpb_nemo/_/img/icon_small_email.png    | icon_small_email.png    |

@wagtail @child @flapper
Scenario Outline: Check all child-page resources to verify they use the full URL (base URL + relative path)
  Given I visit the "www.consumerfinance.gov/<page_url>" URL
  Then I should find the "<relative_path>" image on the page

  Given I visit the "<relative_path>" URL
  Then I should see the page title contains "<contains_text>"

Examples:
| page_url    | relative_path                                             | contains_text          |
#| newsroom/   | /wp-content/themes/cfpb_nemo/_/img/rss.png                | rss.png                |
| the-bureau/ | /wp-content/themes/cfpb_nemo/_/img/icon_small_twitter.png | icon_small_twitter.png |

@wagtail @script
Scenario Outline: Check all scripts to verify they use the full URL (base URL + relative path)
  Given I visit the "www.consumerfinance.gov/<page_url>" URL
  Then I should be directed to the "www.consumerfinance.gov/<page_url>" URL
    And I should find the "<tag>" script "<relative_path>" on the page

  Given I visit the "<relative_path>" URL
  Then I should be directed to the "www.consumerfinance.gov<relative_path>" URL
    And I should see the page title contains "<contains_text>"

Examples:
| page_url                   | tag    | relative_path                                                 | contains_text               |
|                            | script | /wp-content/themes/cfpb_nemo/_/js/jquery-1.9.1.min.js         | jquery-1.9.1.min.js         |
|                            | script | /wp-content/themes/cfpb_nemo/_/js/functions.js                | js/functions.js             |
|                            | script | /wp-content/themes/cfpb_nemo/_/js/analytics-global.js         | analytics-global.js         |
| regulatory-implementation/ | script | /wp-content/themes/cfpb_nemo/_/js/regulations-pdf-tracking.js | regulations-pdf-tracking.js |
#| complaint/                 | script | /wp-content/themes/cfpb_nemo/_/js/cr-003.js                   | cr-003.js                   |
#| find-a-housing-counselor/  | script | /wp-content/themes/cfpb_nemo/_/js/hud-hca-api.js              | hud-hca-api.js              |
#| mortgage/                  | script | /wp-content/themes/cfpb_nemo/_/js/mortgage-analytics.js       | mortgage-analytics.js       |
