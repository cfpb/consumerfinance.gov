from django.views.generic.base import TemplateView, RedirectView
from django.conf.urls import include, url

def rewrite_url(url1, url2, **kwargs):
    return url(url1, RedirectView.as_view(url=url2, **kwargs))

urlredirects =  [

]
# # these used to live in httpd.conf
# Redirect permanent /get-help-now /complaint
# Redirect permanent /developers/sourcecodepolicy https://cfpb.github.io/source-code-policy
# Redirect permanent /developers/ https://cfpb.github.io/
# Redirect permanent /developer/ https://cfpb.github.io/
# Redirect permanent /developer https://cfpb.github.io/
# Redirect permanent /payingforcollege /paying-for-college
# Redirect /regcomments /notice-and-comment
# Redirect /the-bureau/about-raj-date/ /the-bureau/
# Redirect /students/defaultoptions/ /paying-for-college/repay-student-debt/#Question-1
# Redirect /students/repay/ /paying-for-college/repay-student-debt/#Question-1
# Redirect /pfc/ /paying-for-college/?utm_source=redirect&utm_medium=redirect&utm_campaign=pfc
# Redirect /pfc /paying-for-college/?utm_source=redirect&utm_medium=redirect&utm_campaign=pfc
#
# Redirect gone /static/colorbox
#
# # (english) Ask CFPB no longer has special print pages
# RedirectMatch permanent \/askcfpb\/(\d+)\/(.+)\.print.html$ /askcfpb/$1/$2.html
# Redirect /askcfpb/submit-question/ /askcfpb/
#
#
#
#
#
# RedirectMatch  ^/the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers/[/]?$ /blog/the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers/
# RedirectMatch  ^/financial-education-for-moms-and-all-women([/]?)  /blog/financial-education-for-moms-and-all-women/
# RedirectMatch  ^/know-before-you-owe-help-us-make-your-mortgage-forms-better([/]?)  /blog/know-before-you-owe-help-us-make-your-mortgage-forms-better/
# RedirectMatch  ^/know-before-you-owe-designing-a-new-disclosure([/]?)  /blog/know-before-you-owe-designing-a-new-disclosure/
# RedirectMatch  ^/independent-research-at-the-cfpb([/]?)  /blog/independent-research-at-the-cfpb/
# RedirectMatch  ^/know-before-you-owe-go([/]?)  /blog/know-before-you-owe-go/
# RedirectMatch  ^/working-to-give-consumers-the-transparency-they-deserve([/]?)  /blog/working-to-give-consumers-the-transparency-they-deserve/
# RedirectMatch  ^/older-americans-and-the-cfpb([/]?)  /blog/older-americans-and-the-cfpb/
# RedirectMatch  ^/remembering([/]?)  /blog/remembering/
# RedirectMatch  ^/know-before-you-owe-where-did-the-online-participants-come-from([/]?)  /blog/know-before-you-owe-where-did-the-online-participants-come-from/
# RedirectMatch  ^/know-before-you-owe-credit-unions-community-banks([/]?)  /blog/know-before-you-owe-credit-unions-community-banks/
# RedirectMatch  ^/explainer-what-is-a-nonbank-and-what-makes-one-larger([/]?)  /blog/explainer-what-is-a-nonbank-and-what-makes-one-larger/
# RedirectMatch  ^/13000-lessons-learned([/]?)  /blog/13000-lessons-learned/
# RedirectMatch  ^/mortgage-disclosure-is-heating-up([/]?)  /blog/mortgage-disclosure-is-heating-up/
# RedirectMatch  ^/know-before-you-owe-were-back([/]?)  /blog/know-before-you-owe-were-back/
# RedirectMatch  ^/get-ready-to-conquer-your-student-loans([/]?)  /blog/get-ready-to-conquer-your-student-loans/
# RedirectMatch  ^/reaching-out-for-input-help-us-define-larger-participants([/]?)  /blog/reaching-out-for-input-help-us-define-larger-participants/
# RedirectMatch  ^/the-cfpb-and-jags-partnering-to-protect-servicemembers([/]?)  /blog/the-cfpb-and-jags-partnering-to-protect-servicemembers/
# RedirectMatch  ^/making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad([/]?)  /blog/making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad/
# RedirectMatch  ^/joining-the-financial-literacy-and-education-commission([/]?)  /blog/joining-the-financial-literacy-and-education-commission/
# RedirectMatch  ^/a-model-form-for-mortgage-statements([/]?)  /blog/a-model-form-for-mortgage-statements/
# RedirectMatch  ^/vita([/]?)  /blog/vita/
# RedirectMatch  ^/save-the-date-new-york([/]?)  /blog/save-the-date-new-york/
# RedirectMatch  ^/your-thoughts-on-private-student-loans([/]?)  /blog/your-thoughts-on-private-student-loans/
# RedirectMatch  ^/five-ways-to-keep-more-of-your-tax-refund([/]?)  /blog/five-ways-to-keep-more-of-your-tax-refund/
# RedirectMatch  ^/your-feedback-on-know-before-you-owe-student-loans([/]?)  /blog/your-feedback-on-know-before-you-owe-student-loans/
# RedirectMatch  ^/oped/(.*)  /opeds/$1
# RedirectMatch  ^/a-new-tool-for-protecting-the-military-community([/]?)  /blog/a-new-tool-for-protecting-the-military-community/
# RedirectMatch  ^/know-before-you-owe-something-new-for-the-new-year([/]?)  /blog/know-before-you-owe-something-new-for-the-new-year/
# RedirectMatch  ^/speech/(.*)  /speeches/$1
# RedirectMatch  ^/getting-a-complete-picture-of-the-payday-market([/]?)  /blog/getting-a-complete-picture-of-the-payday-market/
# RedirectMatch  ^/hearing-your-stories-on-payday-lending([/]?)  /blog/hearing-your-stories-on-payday-lending/
# RedirectMatch  ^/fulfilling-our-commitment-to-diversity([/]?)  /blog/fulfilling-our-commitment-to-diversity/
# RedirectMatch  ^/the-cfpb-launches-its-nonbank-supervision-program([/]?)  /blog/the-cfpb-launches-its-nonbank-supervision-program/
# RedirectMatch  ^/a-video-message-from-rich-cordray([/]?)  /blog/a-video-message-from-rich-cordray/
# RedirectMatch  ^/cfpb-mortgage-complaint-system-is-up-and-running([/]?)  /blog/cfpb-mortgage-complaint-system-is-up-and-running/
# RedirectMatch  ^/standing-up-for-consumers([/]?)  /blog/standing-up-for-consumers/
# RedirectMatch  ^/destination-portland-me-2([/]?)  /blog/destination-portland-me-2/
# RedirectMatch  ^/financial-fitness-forum([/]?)  /blog/financial-fitness-forum/
# RedirectMatch  ^/a-conversation-with-the-south-florida-latino-community([/]?)  /blog/a-conversation-with-the-south-florida-latino-community/
# RedirectMatch  ^/the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers([/]?)  /blog/the-cfpb-wants-you-to-blow-the-whistle-on-lawbreakers/
# RedirectMatch  ^/addressing-credit-discrimination([/]?)  /blog/addressing-credit-discrimination/
# RedirectMatch  ^/know-before-you-owe-closer-to-closing-mortgage-disclosure-that-is([/]?)  /blog/know-before-you-owe-closer-to-closing-mortgage-disclosure-that-is/
# RedirectMatch  ^/live-holly-petraeus-kicks-off-our-financial-fitness-forum([/]?)  /blog/live-holly-petraeus-kicks-off-our-financial-fitness-forum/
# RedirectMatch  ^/the-cfpb-ombudsmans-office-an-independent-impartial-confidential-resource([/]?)  /blog/the-cfpb-ombudsmans-office-an-independent-impartial-confidential-resource/
# RedirectMatch  ^/how-do-i-shop-for-a-credit-card([/]?)  /blog/how-do-i-shop-for-a-credit-card/
# RedirectMatch  ^/know-before-you-owe-making-credit-card-agreements-readable([/]?)  /blog/know-before-you-owe-making-credit-card-agreements-readable/
# RedirectMatch  ^/live-from-cleveland([/]?)  /blog/live-from-cleveland/
# RedirectMatch  ^/tips-for-avoiding-mortgage-modification-scams([/]?)  /blog/tips-for-avoiding-mortgage-modification-scams/
# RedirectMatch  ^/credit-card-complaints-by-the-numbers([/]?)  /blog/credit-card-complaints-by-the-numbers/
# RedirectMatch  ^/cleveland-save-the-date([/]?)  /blog/cleveland-save-the-date/
# RedirectMatch  ^/lessons-from-the-road([/]?)  /blog/lessons-from-the-road/
# RedirectMatch  ^/chime-in-on-private-student-loans([/]?)  /blog/chime-in-on-private-student-loans/
# RedirectMatch  ^/honoring-veterans([/]?)  /blog/honoring-veterans/
# RedirectMatch  ^/plan-your-spending-to-avoid-holiday-debt([/]?)  /blog/plan-your-spending-to-avoid-holiday-debt/
# RedirectMatch  ^/know-before-you-owe-its-closing-time([/]?)  /blog/know-before-you-owe-its-closing-time/
# RedirectMatch  ^/protecting-military-members-from-predatory-lending([/]?)  /blog/protecting-military-members-from-predatory-lending/
# RedirectMatch  ^/know-before-you-owe-lets-tackle-student-loans([/]?)  /blog/know-before-you-owe-lets-tackle-student-loans/
# RedirectMatch  ^/know-your-student-loan-repayment-options([/]?)  /blog/know-your-student-loan-repayment-options/
# RedirectMatch  ^/live-from-minneapolis([/]?)  /blog/live-from-minneapolis/
# RedirectMatch  ^/from-day-one([/]?)  /blog/from-day-one/
# RedirectMatch  ^/know-before-you-owe-whats-next([/]?)  /blog/know-before-you-owe-whats-next/
# RedirectMatch  ^/guide-cfpb-supervision([/]?)  /blog/guide-cfpb-supervision/
# RedirectMatch  ^/were-listening([/]?)  /blog/were-listening/
# RedirectMatch  ^/meet-us-in-minnesota([/]?)  /blog/meet-us-in-minnesota/
# RedirectMatch  ^/help-for-struggling-military-homeowners([/]?)  /blog/help-for-struggling-military-homeowners/
# RedirectMatch  ^/seeing-servicemembers-as-dollar-signs-in-uniform([/]?)  /blog/seeing-servicemembers-as-dollar-signs-in-uniform/
# RedirectMatch  ^/lessons-weve-learned([/]?)  /blog/lessons-weve-learned/
# RedirectMatch  ^/live-from-philadelphia([/]?)  /blog/live-from-philadelphia/
# RedirectMatch  ^/the-cfpb-applying-the-lessons-of-the-financial-crisis([/]?)  /blog/the-cfpb-applying-the-lessons-of-the-financial-crisis/
# RedirectMatch  ^/know-before-you-owe-and-now-for-something-completely-different([/]?)  /blog/know-before-you-owe-and-now-for-something-completely-different/
# RedirectMatch  ^/avoiding-loan-scams-after-a-natural-disaster([/]?)  /blog/avoiding-loan-scams-after-a-natural-disaster/
# RedirectMatch  ^/co-signing-on-campus([/]?)  /blog/co-signing-on-campus/
# RedirectMatch  ^/coordinating-consumer-complaints([/]?)  /blog/coordinating-consumer-complaints/
# RedirectMatch  ^/promoting-openness-in-cfpb-rulemaking([/]?)  /blog/promoting-openness-in-cfpb-rulemaking/
# RedirectMatch  ^/on-our-way([/]?)  /blog/on-our-way/
# RedirectMatch  ^/military-advocates-on-duty([/]?)  /blog/military-advocates-on-duty/
# RedirectMatch  ^/know-before-you-owe-weigh-in-now([/]?)  /blog/know-before-you-owe-weigh-in-now/
# RedirectMatch  ^/mortgage-disclosures-are-getting-better-thanks-to-you([/]?)  /blog/mortgage-disclosures-are-getting-better-thanks-to-you/
# RedirectMatch  ^/get-and-keep-a-good-credit-score([/]?)  /blog/get-and-keep-a-good-credit-score/
# RedirectMatch  ^/preserving-a-level-playing-field-and-access-to-mortgages([/]?)  /blog/preserving-a-level-playing-field-and-access-to-mortgages/
# RedirectMatch  ^/a-consumer-centered-supervision-program([/]?)  /blog/a-consumer-centered-supervision-program/
# RedirectMatch  ^/a-strong-foundation([/]?)  /blog/a-strong-foundation/
# RedirectMatch  ^/cfpb-spending-update-second-quarter-2011([/]?)  /blog/cfpb-spending-update-second-quarter-2011/
# RedirectMatch  ^/continuing-our-work-with-community-banks-and-credit-unions([/]?)  /blog/continuing-our-work-with-community-banks-and-credit-unions/
# RedirectMatch  ^/talking-to-our-daughters-and-sons-about-personal-finance([/]?)  /blog/talking-to-our-daughters-and-sons-about-personal-finance/
# RedirectMatch  ^/consumer-education-and-engagement-at-the-cfpb([/]?)  /blog/consumer-education-and-engagement-at-the-cfpb/
# RedirectMatch  ^/national-financial-literacy-month([/]?)  /blog/national-financial-literacy-month/
# RedirectMatch  ^/fulfilling-a-commitment([/]?)  /blog/fulfilling-a-commitment/
# RedirectMatch  ^/keeping-it-sunny-at-the-cfpb([/]?)  /blog/keeping-it-sunny-at-the-cfpb/
# RedirectMatch  ^/cfpb-spending-update-first-quarter-2011([/]?)  /blog/cfpb-spending-update-first-quarter-2011/
# RedirectMatch  ^/so-how-do-we-put-elizabeth-warrens-calendar-online([/]?)  /blog/so-how-do-we-put-elizabeth-warrens-calendar-online/
# RedirectMatch  ^/be-a-part-of-our-supervision-team([/]?)  /blog/be-a-part-of-our-supervision-team/
# RedirectMatch  ^/an-accountable-consumer-bureau([/]?)  /blog/an-accountable-consumer-bureau/
# RedirectMatch  ^/the-card-act-conference-what-we-learned([/]?)  /blog/the-card-act-conference-what-we-learned/
# RedirectMatch  ^/its-always-sunny-at-the-cfpb([/]?)  /blog/its-always-sunny-at-the-cfpb/
# RedirectMatch  ^/a-new-voice-for-students([/]?)  /blog/a-new-voice-for-students/
# RedirectMatch  ^/a-ray-of-hope-for-american-consumers([/]?)  /blog/a-ray-of-hope-for-american-consumers/
# RedirectMatch  ^/better-together-how-ncpw-partner-agencies-are-protecting-consumers([/]?)  /blog/better-together-how-ncpw-partner-agencies-are-protecting-consumers/
# RedirectMatch  ^/december-2010-cfpb-implementation-team-reaches-100-employees([/]?)  /blog/december-2010-cfpb-implementation-team-reaches-100-employees/
# RedirectMatch  ^/february-2011-cfpbs-hr-system-comes-online([/]?)  /blog/february-2011-cfpbs-hr-system-comes-online/
# RedirectMatch  ^/september-2010-transfer-date-announced([/]?)  /blog/september-2010-transfer-date-announced/
# RedirectMatch  ^/open-for-suggestions-our-favorite-videos([/]?)  /blog/open-for-suggestions-our-favorite-videos/
# RedirectMatch  ^/finding-a-home([/]?)  /blog/finding-a-home/
# RedirectMatch  ^/the-credit-card-act-turns-one([/]?)  /blog/the-credit-card-act-turns-one/
# RedirectMatch  ^/asking-the-public-about-the-card-act([/]?)  /blog/asking-the-public-about-the-card-act/
# RedirectMatch  ^/professor-warren-speaks-with-americas-credit-unions([/]?)  /blog/professor-warren-speaks-with-americas-credit-unions/
# RedirectMatch  ^/talking-to-small-financial-service-providers([/]?)  /blog/talking-to-small-financial-service-providers/
# RedirectMatch  ^/at-the-podium-with-americas-credit-unions([/]?)  /blog/at-the-podium-with-americas-credit-unions/
# RedirectMatch  ^/one-teachers-challenge([/]?)  /blog/one-teachers-challenge/
# RedirectMatch  ^/a-level-playing-field-for-consumer-financial-products-and-services([/]?)  /blog/a-level-playing-field-for-consumer-financial-products-and-services/
# RedirectMatch  ^/building-better-consumer-protection([/]?)  /blog/building-better-consumer-protection/
# RedirectMatch  ^/consumer-scams([/]?)  /blog/consumer-scams/
# RedirectMatch  ^/professor-warren-speaks-to-consumers-union([/]?)  /blog/professor-warren-speaks-to-consumers-union/
# RedirectMatch  ^/october-2010-cfpb-implementation-team-moves-into-temporary-headquarters([/]?)  /blog/october-2010-cfpb-implementation-team-moves-into-temporary-headquarters/
# RedirectMatch  ^/the-cfpbs-budget([/]?)  /blog/the-cfpbs-budget/
# RedirectMatch  ^/february-2011-cfpb-website-launches([/]?)  /blog/february-2011-cfpb-website-launches/
# RedirectMatch  ^/holly-petraeus-testifies([/]?)  /blog/holly-petraeus-testifies/
# RedirectMatch  ^/calendars-credit-cards-and-consumer-education([/]?)  /blog/calendars-credit-cards-and-consumer-education/
# RedirectMatch  ^/the-cfpb-and-the-religious-community([/]?)  /blog/the-cfpb-and-the-religious-community/
# RedirectMatch  ^/robins-story-andrews-story([/]?)  /blog/robins-story-andrews-story/
# RedirectMatch  ^/responding-to-your-suggestions([/]?)  /blog/responding-to-your-suggestions/
# RedirectMatch  ^/openforsuggestions([/]?)  /blog/openforsuggestions/
# RedirectMatch  ^/welcometothewebsite([/]?)  /blog/welcometothewebsite/
# RedirectMatch  ^/off-topic-blog-comments([/]?)  /blog/off-topic-blog-comments/
# RedirectMatch  ^/hearing-directly-from-our-servicemembers([/]?)  /blog/hearing-directly-from-our-servicemembers/
# RedirectMatch  ^/welcominghollypetraeus  /blog/welcominghollypetraeus/
# RedirectMatch  ^/notice-about-possibly-malicious-emails([/]?)  /blog/notice-about-possibly-malicious-emails/
# RedirectMatch  ^/set-a-goal-and-start-a-savings-habit([/]?)  /blog/set-a-goal-and-start-a-savings-habit/
# RedirectMatch  ^/were-taking-nominations-for-our-consumer-advisory-board([/]?)  /blog/were-taking-nominations-for-our-consumer-advisory-board/
# RedirectMatch  ^/live-from-new-york-city([/]?)  /blog/live-from-new-york-city/
# RedirectMatch  ^/whats-your-status-when-it-comes-to-overdraft-coverage([/]?)  /blog/whats-your-status-when-it-comes-to-overdraft-coverage/
# RedirectMatch  ^/sbrefa-small-providers-and-mortgage-disclosure([/]?)  /blog/sbrefa-small-providers-and-mortgage-disclosure/
# RedirectMatch  ^/know-before-you-owe-the-last-dance-or-is-it([/]?)  /blog/know-before-you-owe-the-last-dance-or-is-it/
# RedirectMatch  ^/office-of-financial-education-begins-listening-tour-in-new-york([/]?)  /blog/office-of-financial-education-begins-listening-tour-in-new-york/
# RedirectMatch  ^/we-want-to-make-it-easier-for-you-to-submit-comments-on-streamlining-regulations([/]?)  /blog/we-want-to-make-it-easier-for-you-to-submit-comments-on-streamlining-regulations/
# RedirectMatch  ^/making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad([/]?)  /blog/making-a-difference-in-the-lives-of-immigrants-and-others-who-send-money-abroad/
# RedirectMatch  ^/HBD([/]?)  /blog/four-years-working-for-you/
# RedirectMatch  ^/hbd([/]?)  /blog/four-years-working-for-you/
# RedirectMatch  ^/studentdebtstress([/]?)  /blog/tell-us-about-your-student-debt-stress/
# RedirectMatch  ^/managing-someone-elses-money-virginia([/]?)$  /blog/managing-someone-elses-money-virginia/
#
# Redirect  301  /privacy-office  /privacy
#
# Redirect  /envios         /sending-money/es
# Redirect  /gui-tien       /sending-money/vi
# Redirect  /gửi-tiền       /sending-money/vi
# Redirect  /perang-padala  /sending-money/tl
# Redirect  /transfe-lajan  /sending-money/ht
# Redirect  /transfè-lajan  /sending-money/ht
#
# Redirect  /blog/prepaid  /blog/prepaid-products-new-disclosures-to-help-you-compare-options
# Redirect  /HMDA  /hmda
# RedirectMatch  301  (?i)^/yourstories  /your-story/?utm_source=print\&utm_medium=flyer\&utm_term=2015\&utm_campaign=TaxInsert
# Redirect  301  /yourstory  /everyone-has-a-story/
# Redirect  /regcomments  /notice-and-comment
# Redirect  301  /parent  /money-as-you-grow/
# Redirect  301  /parents  /money-as-you-grow/
# Redirect  /debtsurvey.html  /debtsurvey/
# Redirect  /AskCFPB  /askcfpb
# Redirect  301  /youhavetheright  /you-have-the-right
# Redirect  301  /taxtimesaving  /tax-time-saving
# Redirect  301  /financial-well-being  /reports/financial-well-being-scale/
#
#
# # Fix for a typo that went out in an email release
# RedirectMatch  301  ^/project$ /projectcatalyst
#
# # Know Before You Owe
# RedirectMatch  301  ^/kbyo(.*)  /know-before-you-owe$1
# RedirectMatch  301  ^/knowbeforeyouowe(.*)  /know-before-you-owe$1
# RedirectMatch  301  (.*)/realestateprofessionals(.*)  $1/real-estate-professionals$2
# RedirectMatch  301  ^/real-estate[/]?$  /know-before-you-owe/real-estate-professionals/
#
# # Retirement redirects
# RedirectMatch  (?i)^/retirement/claiming-social-security/?$ /retirement/before-you-claim/
# RedirectMatch  (?i)^/jubilacion/?$  /retirement/before-you-claim/es/
# RedirectMatch  (?i)^/retirement/?$  /retirement/before-you-claim/
#
# # Ask CFPB redirects, requested July 2015 by Ashley Gordon
#
# Redirect /askcfpb/125/what-does-it-mean-to-be-prequalified-for-a-mortgage.html /askcfpb/127/whats-the-difference-between-being-prequalified-and-preapproved-for-a-mortgage.html
# Redirect /askcfpb/126/what-does-it-mean-to-be-preapproved-for-a-mortgage-loan.html /askcfpb/127/whats-the-difference-between-being-prequalified-and-preapproved-for-a-mortgage.html
# Redirect /askcfpb/150/what-documents-will-my-lender-or-mortgage-broker-request-after-i-have-found-the-right-loan-for-me.html /askcfpb/144/what-does-it-mean-to-apply-for-a-loan-or-fill-out-a-loan-application.html
# Redirect /askcfpb/145/what-happens-after-i-apply-for-a-mortgage.html /askcfpb/144/what-does-it-mean-to-apply-for-a-loan-or-fill-out-a-loan-application.html
# Redirect /askcfpb/171/what-papers-should-i-get-after-i-decide-on-the-type-of-loan-and-choose-my-lender-or-mortgage-broker.html /askcfpb/144/what-does-it-mean-to-apply-for-a-loan-or-fill-out-a-loan-application.html
# Redirect /askcfpb/169/i-applied-for-a-home-loan-and-never-received-a-response-to-my-mortgage-application-what-can-i-do.html /askcfpb/148/i-never-received-a-good-faith-estimate-or-gfe-what-can-i-do.html
# Redirect /askcfpb/149/my-gfe-has-an-interest-rate-lock-time-period-does-this-mean-the-interest-rate-is-locked-in.html /askcfpb/143/whats-a-lock-in-or-a-rate-lock.html
# Redirect /askcfpb/151/how-do-i-figure-out-what-my-monthly-payment-for-a-mortgage-loan-will-be.html /askcfpb/1965/how-do-mortgage-lenders-calculate-monthly-payments.html
# Redirect /askcfpb/138/what-kinds-of-fees-are-involved-with-my-mortgage-loan.html /askcfpb/153/what-costs-will-i-have-to-pay-as-part-of-taking-out-a-mortgage-loan.html
# Redirect /askcfpb/139/what-are-closing-costs.html /askcfpb/1845/what-fees-or-charges-are-paid-closing-and-who-pays-them.html
# Redirect /askcfpb/194/i-used-the-title-services-and-lenders-title-insurance-companies-or-owners-title-insurance-company-listed-by-my-lender-on-my-gfe-but-was-charged-more-than-10-percent-more-than-my-gfe-said-i-would-be-now-my-lender-wont-pay-me-back-what-can-i-do.html /askcfpb/172/can-the-final-mortgage-costs-be-different-from-the-good-faith-estimate-gfe.html
# Redirect /askcfpb/156/what-are-adjusted-origination-charges.html /askcfpb/155/what-are-origination-services-what-is-an-origination-fee.html
# Redirect /askcfpb/191/my-lender-or-broker-gave-me-a-gfe-for-15-year-loan-but-when-i-got-to-the-closing-the-documents-said-it-was-a-30-year-loan-my-lender-or-broker-said-not-to-worry-i-can-refinance-later-but-thats-not-in-any-of-my-paperwork-and-i-dont-want-to-close-a-loan-whos.html /askcfpb/184/what-if-my-lender-quoted-me-one-rate-at-application-but-raised-it-at-closing.html
# Redirect /askcfpb/142/what-is-a-no-cash-loan.html /askcfpb/141/is-there-such-a-thing-as-a-no-cost-or-no-closing-loan-or-refinancing.html
#
# # Ask CFPB redirects, requested October 2015 by Erica Kritt
#
# Redirect /es/obtener-respuestas/c/comprar-una-casa/125/que-significa-estar-pre-calificado-para-una-hipoteca.html /es/obtener-respuestas/c/comprar-una-casa/127/cual-es-la-diferencia-entre-estar-pre-calificado-y-estar-pre-aprobado-para-una-hipoteca.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/126/que-significa-estar-pre-aprobado-para-un-prestamo-hipotecario.html /es/obtener-respuestas/c/comprar-una-casa/127/cual-es-la-diferencia-entre-estar-pre-calificado-y-estar-pre-aprobado-para-una-hipoteca.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/150/que-documentos-me-solicitara-el-prestamista-o-corredor-hipotecario-despues-de-encontrar-el-prestamo-adecuado-para-mi.html /es/obtener-respuestas/c/comprar-una-casa/144/que-significa-solicitar-un-prestamo.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/145/que-sucede-despues-de-solicitar-un-prestamo.html /es/obtener-respuestas/c/comprar-una-casa/144/que-significa-solicitar-un-prestamo.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/171/que-papeles-debo-obtener-despues-que-decidir-el-tipo-de-prestamo-y-escoger-mi-prestamista-o-corredor-hipotecario.html /es/obtener-respuestas/c/comprar-una-casa/144/que-significa-solicitar-un-prestamo.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/169/solicite-un-prestamo-y-nunca-recibi-respuesta-mi-solicitud-que-puedo-hacer.html /es/obtener-respuestas/c/comprar-una-casa/148/nunca-recibi-el-estimado-de-buena-fe-o-gfe-que-puedo-hacer.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/149/mi-gfe-tiene-un-periodo-de-tiempo-asegurado-para-la-tasa-de-interes-esto-significa-que-la-tasa-de-interes-esta-asegurada.html /es/obtener-respuestas/c/comprar-una-casa/143/que-es-tasa-asegurada-o-lock-rate.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/138/recibi-una-estimacion-de-prestamo-actualizada-de-mi-prestamista-que-muestra-una-mayor-tasa-de-interes-y-gastos-de-cierre-mas-altos.html /es/obtener-respuestas/c/comprar-una-casa/153/que-costos-tendre-que-pagar-por-obtener-un-prestamo-hipotecario.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/194/yo-use-los-servicios-del-titulo-y-las-companias-de-titulo-seguro-del-prestamista-o-la-compania-de-seguros-del-titulo-del-propietario-imprimidos-por-mi-prestamista-en-el-gfe-pero-me-cobraron-10-por-ciento-mas-de-lo-que-el-gfe-se-decia-ahora-el-prestamista-.html /es/obtener-respuestas/c/comprar-una-casa/172/Los-costos-finales-de-mi-hipoteca-pueden-aumentar-con-respecto-a-lo-que-se-indicaba-en-la-estimacion-del-prestamo.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/156/que-son-los-costos-de-originacion-ajustados.html /es/obtener-respuestas/c/comprar-una-casa/155/que-son-servicios-de-originacion-que-es-un-costo-de-originacion.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/191/mi-prestamista-o-corredor-me-dio-un-gfe-para-un-prestamo-a-15-anos-pero-al-cierre-los-documentos-decian-que-era-un-prestamo-a-30-anos-mi-prestamista-o-corredor-dijo-que-no-me-preocupara-que-puedo-refinanciar-mas-tarde-pero-eso-no-esta-en-mis-documentos-y-.html /es/obtener-respuestas/c/comprar-una-casa/184/que-sucede-si-el-prestamista-me-dio-una-tasa-en-el-momento-de-la-solicitud-pero-la-elevo-en-el-cierre.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/173/si-algo-relacionado-con-mi-prestamo-cambia-cuando-debe-informarme-el-prestamista.html /es/obtener-respuestas/c/comprar-una-casa/1991/recibi-una-estimacion-de-prestamo-actualizada-de-mi-prestamista-que-muestra-una-mayor-tasa-de-interes-y-gastos-de-cierre-mas-altos.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/174/cuando-me-da-la-tasa-de-interes-final-el-prestamista.html /es/obtener-respuestas/c/comprar-una-casa/1983/Que-es-la-informacion-de-cierre.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/142/que-es-un-prestamo-sin-efectivo-no-cash.html /es/obtener-respuestas/c/comprar-una-casa/141/existen-prestamos-o-refinanciamiento-sin-costo-no-cost-o-sin-cierre-no-closing.html
# Redirect /askcfpb/173/if-something-related-to-my-loan-changes-when-does-the-lender-have-to-tell-me.html /askcfpb/1991/I-received-a-revised-Loan-Estimate-from-my-lender-showing-a-higher-interest-rate-and-increased-closing-costs.html
# Redirect /askcfpb/174/when-does-the-lender-have-to-disclose-the-final-interest-rate.html /askcfpb/1983/what-is-a-closing-disclosure.html
# Redirect /askcfpb/165/how-can-i-understand-how-much-my-home-loan-or-mortgage-payment-could-change-if-i-receive-a-different-interest-rate.html /askcfpb/1965/how-do-mortgage-lenders-calculate-monthly-payments.html
#
#
# # Ask CFPB redirects, requested May 2016 by Ruth Mercado
#
# Redirect /es/obtener-respuestas/c/comprar-una-casa/139/que-son-los-costos-de-cierre.html /es/obtener-respuestas/c/comprar-una-casa/1845/que-honorarios-o-cargos-se-pagan-al-cerrar-una-hipoteca-y-quien-los-paga.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/151/como-calculo-cual-sera-mi-pago-mensual-por-un-prestamo-hipotecario.html /es/obtener-respuestas/c/comprar-una-casa/1965/como-los-prestamistas-hipotecarios-calculan-los-pagos-mensuales.html
# Redirect /es/obtener-respuestas/c/comprar-una-casa/165/como-entender-cuanto-mi-pago-podria-cambiar-si-recibo-una-tasa-de-interes-diferente.html /es/obtener-respuestas/c/comprar-una-casa/1965/como-los-prestamistas-hipotecarios-calculan-los-pagos-mensuales.html
#
#
# # Ask CFPB redirects, requested June 2016 in conjunction with Auto Loans release
# # NOTE: This simplified format is only safe under the assumption that
# # we will never make it to 7,410+ Ask CFPB questions.
# # For redirects of question IDs under 400 or so, best to use the full URL.
#
# Redirect /askcfpb/729  /askcfpb/825
# Redirect /askcfpb/741  /askcfpb/759
# Redirect /askcfpb/793  /askcfpb/751
# Redirect /askcfpb/829  /askcfpb/743
# Redirect /askcfpb/879  /askcfpb/831
# Redirect /askcfpb/885  /askcfpb/759
# Redirect /askcfpb/1173 /askcfpb/1171
# Redirect /askcfpb/1175 /askcfpb/1171
#
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/729/que-es-una-garantia-extension-o-un-contrato-de-servicio.html /es/obtener-respuestas/c/comprar-un-vehiculo/825/cual-es-la-diferencia-entre-una-garantia-y-una-garantia-extendida.html
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/741/que-es-financiamiento-de-concesionario.html /es/obtener-respuestas/c/comprar-un-vehiculo/759/cual-es-la-diferencia-entre-financiamiento-bancario-y-financiamiento-concertado-con-el-concesionario.html
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/793/mi-banco-solo-me-aprobara-un-prestamo-por-25000-pero-el-concesionario-me-indica-que-puedo-calificar-para-un-prestamo-mayor-quien-esta-en-lo-correcto.html /es/obtener-respuestas/c/comprar-un-vehiculo/751/estoy-pensando-en-adquirir-o-alquilar-un-vehiculo-como-puedo-decidir-cuanto-puedo-pedir-prestad.html
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/829/mis-documentos-indican-que-un-cesionario-tiene-derecho-de-retencion-sobre-el-titulo-de-mi-vehiculo-que-quiere-decir-esto.html /es/obtener-respuestas/c/comprar-un-vehiculo/743/que-es-un-cesionario.html
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/879/pase-5-horas-en-el-concesionario-comprando-un-automovil-y-obteniendo-lo-que-pense-que-era-una-buena-tasa-de-interes-finalmente-el-dealer-dijo-vaya-y-llevese-el-automovil-terminaremos-el-financiamiento-mas-tarde-al-dia-siguiente-p-recibi-una-llamada-del-co.html /es/obtener-respuestas/c/comprar-un-vehiculo/831/compre-un-automovil-y-recibi-una-llamada-del-vendedor-quien-dijo-que-necesito-regresar-al-dealer-o-concesionario-para-hablar-sobre-mi-prestamo-pense-que-habia-sido-aprobado-que-puedo-hacer.html
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/885/debo-financiar-mi-automovil-con-el-concesionario-con-una-cooperativa-de-credito-o-con-un-banco.html /es/obtener-respuestas/c/comprar-un-vehiculo/759/cual-es-la-diferencia-entre-financiamiento-bancario-y-financiamiento-concertado-con-el-concesionario.html
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/1173/cuales-son-mis-derechos-segun-la-ley-si-el-prestamista-o-concesionario-me-discrimino-cuando-solicite-un-prestamo-de-vehiculo.html /es/obtener-respuestas/c/comprar-un-vehiculo/1171/solicite-un-prestamo-vehicular-pero-el-prestamista-o-el-concesionario-rechazo-mi-solicitud-creo-que-el-prestamista-o-el-concesionario-me-discrimino-que-derechos-tengo-legalmente.html
# Redirect /es/obtener-respuestas/c/comprar-un-vehiculo/1175/acabo-de-empezar-un-nuevo-negocio-e-intente-obtener-un-prestamo-vehicular-para-mi-empresa-creo-que-el-prestamista-o-el-concesionario-me-discrimino-y-a-mi-empresa-tambien-cuales-son-los-derechos-que-me-otorga-la-ley.html /es/obtener-respuestas/c/comprar-un-vehiculo/1171/solicite-un-prestamo-vehicular-pero-el-prestamista-o-el-concesionario-rechazo-mi-solicitud-creo-que-el-prestamista-o-el-concesionario-me-discrimino-que-derechos-tengo-legalmente.html
#
#
# # Owning a Home redirects
#
# RewriteRule ^owningahome$ /owning-a-home$1 [L,R=301]
# Redirect permanent /owningahome /owning-a-home
# Redirect permanent /OWNING-A-HOME /owning-a-home
# Redirect permanent /OWNINGAHOME /owning-a-home
#
# Redirect /mortgage-estimate /owning-a-home/mortgage-estimate/?utm_source=mortgageestimate&utm_medium=redirect&utm_campaign=OAHredirects
# Redirect /mortgage-closing /owning-a-home/mortgage-closing/?utm_source=mortgageclosing&utm_medium=redirect&utm_campaign=OAHredirects
# Redirect /owning-a-home/check-rates /owning-a-home/explore-rates/?utm_source=checkrates&utm_medium=redirect&utm_campaign=OAHredirects
# RedirectMatch ^/owning-a-home/monthly-payment-worksheet[/]*$ /owning-a-home/resources/monthly_payment_worksheet.pdf
#
# # Consumer Complaint Database
# Redirect  301  /complaintdatabase/technical-documentation  https://cfpb.github.io/api/ccdb/
#
# # New document releases
# Redirect 301 /f/201501_cfpb_list-consumer-reporting-agencies.pdf /f/201604_cfpb_list-of-consumer-reporting-companies.pdf
# Redirect 301 /f/201601_cpfb_list-of-consumer-reporting-companies.pdf /f/201604_cfpb_list-of-consumer-reporting-companies.pdf
#
# # redirects associated with the v1 project
#
#     Redirect /pressreleases/ /about-us/newsroom/
#     Redirect /opeds/  /about-us/newsroom/
#     Redirect /testimonies/ /about-us/newsroom/
#     Redirect /speeches/  /about-us/newsroom/
#     Redirect /newsroom/ /about-us/newsroom/
#     RedirectMatch (?i)^/moneyasyougrow/  /money-as-you-grow/
#     Redirect /payingforcollege/ /paying-for-college/
#     Redirect /owning-a-home/check-rates/  /owning-a-home/explore-rates/?utm_source=checkrates&utm_medium=redirect&utm_campaign=OAHredirects/
#     Redirect /knowbeforeyouowe/ /know-before-you-owe/
#     Redirect /d/askcfpb/  /askcfpb/
#     Redirect /reports/a-snapshot-of-servicemember-complaints/  /reports/osa-semi-annual-snapshot-of-servicemember-comp/
#     Redirect /project/ /projectcatalyst/
#     Redirect /lang /language
#     Redirect /no-fear-act/ /office-civil-rights/no-fear-act/
#     Redirect /index.html /
#
#     Redirect	/budget/cfo-q3-2012/	/about-us/budget-strategy/financial-reports/cfo-q3-2012/
#     Redirect	/budget/cfo-q2-2012/	/about-us/budget-strategy/financial-reports/cfo-q2-2012/
#     Redirect	/budget/cfo-q1-2012/	/about-us/budget-strategy/financial-reports/cfo-q1-2012/
#     Redirect	/budget/cfo-q4-2011/	/about-us/budget-strategy/financial-reports/cfo-q4-2011/
#     Redirect	/budget/cfo-q3-2011/	/about-us/budget-strategy/financial-reports/cfo-q3-2011/
#     Redirect	/budget/cfo-q2-2011/	/about-us/budget-strategy/financial-reports/cfo-q2-2011/
#     Redirect	/budget/cfo-q1-2011/	/about-us/budget-strategy/financial-reports/cfo-q1-2011/
#     Redirect    /budget/civil-penalty-fund    /about-us/payments-harmed-consumers/payments-by-case
#     Redirect	/budget/	/about-us/budget-strategy/
#
#     RedirectMatch ^\/leadership-calendar\/(?!cfpb-leadership.json)   /about-us/the-bureau/leadership-calendar/
#     Redirect /the-bureau/about-rich-cordray/   /about-us/the-bureau/about-director/
# 	Redirect	/administrativeadjudication/2015-cfpb-0029/	/policy-compliance/enforcement/actions/integrity-advance/
# 	Redirect	/administrativeadjudication/2014-cfpb-0002/	/policy-compliance/enforcement/actions/phh-corporation/
# 	Redirect	/administrativeadjudication/2013-cfpb-0002/	/policy-compliance/enforcement/actions/3d-resorts-bluegrass/
# 	Redirect	/administrativeadjudication/	/policy-compliance/enforcement/actions/?form-id=0&filter0_categories=admin-filing&filter0_from_date=&filter0_to_date=
#
# 	Redirect	/amicus/amicus-faqs/	/policy-compliance/amicus/suggest/
# 	Redirect	/amicus/	/policy-compliance/amicus/
#
#
#
#
#     Redirect /jobs/title     /careers/current-openings/
#     Redirect /jobs/location  /careers/current-openings/
#     RedirectMatch ^\/jobs\/detail\/.*  /careers/current-openings/
#     RedirectMatch ^\/jobs\/(?!supervision)(?!technology-innovation-fellows)(?!jobs.json).* /about-us/careers/
#
#
#     Redirect /advisory-groups/advisory-groups-meeting-details/ /about-us/advisory-groups/
#     Redirect /advisory-groups/ /about-us/advisory-groups/
#     Redirect /hmda/  /data-research/hmda/
#     Redirect /data-research/mortgage-data-hmda/  /data-research/hmda/
#
#     Redirect /complaintdatabase/ /data-research/consumer-complaints/
#
#     RedirectMatch ^\/regulations[\/]?$ /policy-compliance/rulemaking/
#     Redirect /remittances-transfer-rule-amendment-to-regulation-e/  /policy-compliance/rulemaking/final-rules/electronic-fund-transfers-regulation-e/
#     Redirect /regulations/integrated-mortgage-disclosures-under-the-real-estate-settlement-procedures-act-regulation-x-and-the-truth-in-lending-act-regulation-z/ /policy-compliance/rulemaking/final-rules/2013-integrated-mortgage-disclosure-rule-under-real-estate-settlement-procedures-act-regulation-x-and-truth-lending-act-regulation-z/
#
#     RedirectMatch ^\/retirement[\/]?$  /retirement/before-you-claim
#
#     # Legacy /credit-cards pages
#     #   Redirect most to data-research
#
#     RedirectMatch ^\/credit-cards\/(?!agreements)(?!knowbeforeyouowe)(?!credit-card-act)(?!college-agreements).*  /data-research/credit-card-data/
#
#     #   college agreements to /data-research/credit-card-data/college-credit-card-agreement/
#     Redirect /credit-cards/college-agreements/   /data-research/credit-card-data/college-credit-card-agreement/
#
#
#
#     # regulatory-implementation
#
#     RedirectMatch ^\/regulatory\-implementation\/?$ /policy-compliance/guidance/implementation-guidance/
#     Redirect	/regulatory-implementation/title-xiv	/policy-compliance/guidance/implementation-guidance/title-xiv-mortgage-rules/
#     Redirect	/regulatory-implementation/tila-respa	/policy-compliance/guidance/implementation-guidance/tila-respa-disclosure-rule/
#     Redirect	/remittances-transfer-rule-amendment-to-regulation-e	/policy-compliance/guidance/implementation-guidance/remittance-transfer-rule/
#     Redirect	/regulatory-implementation/hmda	/policy-compliance/guidance/implementation-guidance/hmda-implementation/
#
#     # legacy regulations URL's
#
#     Redirect	/regulations/integrated-mortgage-disclosures-under-the-real-estate-settlement-procedures-act-regulation-x-and-the-truth-in-lending-act-regulation-z/	/policy-compliance/rulemaking/final-rules/2013-integrated-mortgage-disclosure-rule-under-real-estate-settlement-procedures-act-regulation-x-and-truth-lending-act-regulation-z/
#     Redirect	/regulations/consumer-financial-civil-penalty-fund-rule/	/policy-compliance/rulemaking/final-rules/consumer-financial-civil-penalty-fund-rule/
#     Redirect	/regulations/loan-originator-compensation-requirements-under-the-truth-in-lending-act-regulation-z/	/policy-compliance/rulemaking/final-rules/loan-originator-compensation-requirements-under-truth-lending-act-regulation-z/
#     Redirect	/regulations/disclosure-and-delivery-requirements-for-copies-of-appraisals-and-other-written-valuations-under-the-equal-credit-opportunity-act-regulation-b/	/policy-compliance/rulemaking/final-rules/disclosure-and-delivery-requirements-copies-appraisals-and-other-written-valuations-under-equal-credit-opportunity-act-regulation-b/
#     Redirect	/regulations/appraisals-for-higher-priced-mortgage-loans/	/policy-compliance/rulemaking/final-rules/appraisals-higher-priced-mortgage-loans/
#     Redirect	/regulations/2013-real-estate-settlement-procedures-act-regulation-x-and-truth-in-lending-act-regulation-z-mortgage-servicing-final-rules/	/policy-compliance/rulemaking/final-rules/2013-real-estate-settlement-procedures-act-regulation-x-and-truth-lending-act-regulation-z-mortgage-servicing-final-rules/
#     Redirect	/regulations/escrow-requirements-under-the-truth-in-lending-act-regulation-z/	/policy-compliance/rulemaking/final-rules/escrow-requirements-under-truth-lending-act-regulation-z/
#     Redirect	/regulations/high-cost-mortgage-and-homeownership-counseling-amendments-to-regulation-z-and-homeownership-counseling-amendments-to-regulation-x/	/policy-compliance/rulemaking/final-rules/high-cost-mortgage-and-homeownership-counseling-amendments-truth-lending-act-regulation-z-and-homeownership-counseling-amendments-real-estate-settlement-procedures-act-regulation-x/
#     Redirect	/regulations/ability-to-repay-and-qualified-mortgage-standards-under-the-truth-in-lending-act-regulation-z/	/policy-compliance/rulemaking/final-rules/ability-repay-and-qualified-mortgage-standards-under-truth-lending-act-regulation-z/
#
#
#     # misc redirects
#
#     Redirect	/regulatory-agenda-archive/	/policy-compliance/rulemaking/regulatory-agenda/
#     Redirect	/fall-2011-semiannual-regulatory-agenda-and-regulatory-plan/	/policy-compliance/rulemaking/regulatory-agenda/fall-2011-semiannual-regulatory-agenda-and-regulatory-plan/
#     Redirect	/fall-2011-statement-of-regulatory-priorities/	/policy-compliance/rulemaking/regulatory-agenda/fall-2011-statement-regulatory-priorities/
#
#     Redirect	/guidance/supervision/manual/  /policy-compliance/guidance/supervision-examinations/
#     Redirect    /guidance/supervision/	/policy-compliance/guidance/supervision-examinations/
#     Redirect	/guidance/petitions-to-modify-or-set-aside/	/policy-compliance/enforcement/petitions/
#
#     Redirect	/guidance/	/policy-compliance/guidance/
#
#     Redirect    /mortgage-rules-at-a-glance/   /policy-compliance/rulemaking/final-rules/?form-id=1&filter1_title=&filter1_topics=Mortgages
#     Redirect    /students-and-recent-graduates/  /careers/students-and-graduates/
#
#     Redirect	/notice-and-comment/	/policy-compliance/notice-opportunities-comment/
#     Redirect	/amicus/	/policy-compliance/amicus-program/
#     Redirect	/amicus/amicus-faqs/	/policy-compliance/amicus/suggest/
#     Redirect	/small-financial-services-providers/	/policy-compliance/community-banks-credit-unions/
#     Redirect	/doing-business-with-us/	/about-us/doing-business-with-us/
#     Redirect	/advisory-groups/	/about-us/advisory-groups/
#     Redirect	/advisory-groups/advisory-groups-meeting-details/	/about-us/advisory-groups/
#     Redirect	/projectcatalyst/ 	/about-us/project-catalyst/
#     Redirect	/ProjectCatalyst/ 	/about-us/project-catalyst/
#     Redirect	/contact-us/	/about-us/contact-us/
#
#     Redirect	/foia/sample-foia-request/	/foia-requests/submit-request/
#     Redirect	/foia/foia-fee-schedule/	/foia-requests/fee-schedule/
#     RedirectMatch ^\/foia\/(?!quarterly)(.*)$  /foia-requests/$1
#     Redirect	/privacy-policy/	/privacy/digital-privacy-policy/
#     Redirect	/privacy/complaints/	/privacy/file-privacy-complaint/
#     Redirect	/open/	/open-government/
#     Redirect	/informationquality/	/open-government/information-quality-guidelines/
#     Redirect	/equal-employment-opportunity/	/office-civil-rights/
#     Redirect	/equal-employment-opportunity/whistleblowers/	/office-civil-rights/whistleblowers/
#     Redirect /table-of-applicable-citations-and-corresponding-provisions-for-rural-and-underserved-counties/  /rural-or-underserved-tool/
#     Redirect  /comment-policy/ /about-us/comment-policy/
#
#     Redirect /ombudsman/charter/  /cfpb-ombudsman/ombudsman-charter/
#     Redirect /ombudsman/ /cfpb-ombudsman/
#
#
#     # redirect SORN notices
#     Redirect /privacy/amending-and-correcting-records-under-the-privacy-act /privacy/amending-and-correcting-records-under-privacy-act
#     Redirect /privacy/privacy-policy-for-non-us-persons/ /privacy/privacy-policy-non-us-citizens/
#
#     RedirectMatch	^\/privacy\/(?!privacy-policy-non-us-citizens)(?!generic-email-sign-privacy-act-statement)(?!digital-privacy-policy)(?!system-records-notices)(?!privacy-impact-assessments)(?!amending-and-correcting-records-under-privacy-act)(?!amending-and-correcting-records-under-the-privacy-act)(?!complaints)(?!file-privacy-complaint)(?!privacy-policy)([\w-]+)\/?	/privacy/system-records-notices/$1/
#
# # strip pagination from legacy blog and category URL's
#
# RedirectMatch \/blog\/(.+)\/page\/(\d+) /blog/$1/
#
#     # Legacy blog date URL's
#
#
# Redirect /blog/2011/01/ /about-us/blog/?filter1_from_date=01%2F01%2F2011&filter1_to_date=01%2F31%2F2011
# Redirect /blog/2011/02/ /about-us/blog/?filter1_from_date=02%2F01%2F2011&filter1_to_date=02%2F28%2F2011
# Redirect /blog/2011/03/ /about-us/blog/?filter1_from_date=03%2F01%2F2011&filter1_to_date=03%2F31%2F2011
# Redirect /blog/2011/04/ /about-us/blog/?filter1_from_date=04%2F01%2F2011&filter1_to_date=04%2F30%2F2011
# Redirect /blog/2011/05/ /about-us/blog/?filter1_from_date=05%2F01%2F2011&filter1_to_date=05%2F31%2F2011
# Redirect /blog/2011/06/ /about-us/blog/?filter1_from_date=06%2F01%2F2011&filter1_to_date=06%2F30%2F2011
# Redirect /blog/2011/07/ /about-us/blog/?filter1_from_date=07%2F01%2F2011&filter1_to_date=07%2F31%2F2011
# Redirect /blog/2011/08/ /about-us/blog/?filter1_from_date=08%2F01%2F2011&filter1_to_date=08%2F31%2F2011
# Redirect /blog/2011/09/ /about-us/blog/?filter1_from_date=09%2F01%2F2011&filter1_to_date=09%2F30%2F2011
# Redirect /blog/2011/10/ /about-us/blog/?filter1_from_date=10%2F01%2F2011&filter1_to_date=10%2F31%2F2011
# Redirect /blog/2011/11/ /about-us/blog/?filter1_from_date=11%2F01%2F2011&filter1_to_date=11%2F30%2F2011
# Redirect /blog/2011/12/ /about-us/blog/?filter1_from_date=12%2F01%2F2011&filter1_to_date=12%2F31%2F2011
# Redirect /blog/2012/01/ /about-us/blog/?filter1_from_date=01%2F01%2F2012&filter1_to_date=01%2F31%2F2012
# Redirect /blog/2012/02/ /about-us/blog/?filter1_from_date=02%2F01%2F2012&filter1_to_date=02%2F29%2F2012
# Redirect /blog/2012/03/ /about-us/blog/?filter1_from_date=03%2F01%2F2012&filter1_to_date=03%2F31%2F2012
# Redirect /blog/2012/04/ /about-us/blog/?filter1_from_date=04%2F01%2F2012&filter1_to_date=04%2F30%2F2012
# Redirect /blog/2012/05/ /about-us/blog/?filter1_from_date=05%2F01%2F2012&filter1_to_date=05%2F31%2F2012
# Redirect /blog/2012/06/ /about-us/blog/?filter1_from_date=06%2F01%2F2012&filter1_to_date=06%2F30%2F2012
# Redirect /blog/2012/07/ /about-us/blog/?filter1_from_date=07%2F01%2F2012&filter1_to_date=07%2F31%2F2012
# Redirect /blog/2012/08/ /about-us/blog/?filter1_from_date=08%2F01%2F2012&filter1_to_date=08%2F31%2F2012
# Redirect /blog/2012/09/ /about-us/blog/?filter1_from_date=09%2F01%2F2012&filter1_to_date=09%2F30%2F2012
# Redirect /blog/2012/10/ /about-us/blog/?filter1_from_date=10%2F01%2F2012&filter1_to_date=10%2F31%2F2012
# Redirect /blog/2012/11/ /about-us/blog/?filter1_from_date=11%2F01%2F2012&filter1_to_date=11%2F30%2F2012
# Redirect /blog/2012/12/ /about-us/blog/?filter1_from_date=12%2F01%2F2012&filter1_to_date=12%2F31%2F2012
# Redirect /blog/2013/01/ /about-us/blog/?filter1_from_date=01%2F01%2F2013&filter1_to_date=01%2F31%2F2013
# Redirect /blog/2013/02/ /about-us/blog/?filter1_from_date=02%2F01%2F2013&filter1_to_date=02%2F28%2F2013
# Redirect /blog/2013/03/ /about-us/blog/?filter1_from_date=03%2F01%2F2013&filter1_to_date=03%2F31%2F2013
# Redirect /blog/2013/04/ /about-us/blog/?filter1_from_date=04%2F01%2F2013&filter1_to_date=04%2F30%2F2013
# Redirect /blog/2013/05/ /about-us/blog/?filter1_from_date=05%2F01%2F2013&filter1_to_date=05%2F31%2F2013
# Redirect /blog/2013/06/ /about-us/blog/?filter1_from_date=06%2F01%2F2013&filter1_to_date=06%2F30%2F2013
# Redirect /blog/2013/07/ /about-us/blog/?filter1_from_date=07%2F01%2F2013&filter1_to_date=07%2F31%2F2013
# Redirect /blog/2013/08/ /about-us/blog/?filter1_from_date=08%2F01%2F2013&filter1_to_date=08%2F31%2F2013
# Redirect /blog/2013/09/ /about-us/blog/?filter1_from_date=09%2F01%2F2013&filter1_to_date=09%2F30%2F2013
# Redirect /blog/2013/10/ /about-us/blog/?filter1_from_date=10%2F01%2F2013&filter1_to_date=10%2F31%2F2013
# Redirect /blog/2013/11/ /about-us/blog/?filter1_from_date=11%2F01%2F2013&filter1_to_date=11%2F30%2F2013
# Redirect /blog/2013/12/ /about-us/blog/?filter1_from_date=12%2F01%2F2013&filter1_to_date=12%2F31%2F2013
# Redirect /blog/2014/01/ /about-us/blog/?filter1_from_date=01%2F01%2F2014&filter1_to_date=01%2F31%2F2014
# Redirect /blog/2014/02/ /about-us/blog/?filter1_from_date=02%2F01%2F2014&filter1_to_date=02%2F28%2F2014
# Redirect /blog/2014/03/ /about-us/blog/?filter1_from_date=03%2F01%2F2014&filter1_to_date=03%2F31%2F2014
# Redirect /blog/2014/04/ /about-us/blog/?filter1_from_date=04%2F01%2F2014&filter1_to_date=04%2F30%2F2014
# Redirect /blog/2014/05/ /about-us/blog/?filter1_from_date=05%2F01%2F2014&filter1_to_date=05%2F31%2F2014
# Redirect /blog/2014/06/ /about-us/blog/?filter1_from_date=06%2F01%2F2014&filter1_to_date=06%2F30%2F2014
# Redirect /blog/2014/07/ /about-us/blog/?filter1_from_date=07%2F01%2F2014&filter1_to_date=07%2F31%2F2014
# Redirect /blog/2014/08/ /about-us/blog/?filter1_from_date=08%2F01%2F2014&filter1_to_date=08%2F31%2F2014
# Redirect /blog/2014/09/ /about-us/blog/?filter1_from_date=09%2F01%2F2014&filter1_to_date=09%2F30%2F2014
# Redirect /blog/2014/10/ /about-us/blog/?filter1_from_date=10%2F01%2F2014&filter1_to_date=10%2F31%2F2014
# Redirect /blog/2014/11/ /about-us/blog/?filter1_from_date=11%2F01%2F2014&filter1_to_date=11%2F30%2F2014
# Redirect /blog/2014/12/ /about-us/blog/?filter1_from_date=12%2F01%2F2014&filter1_to_date=12%2F31%2F2014
# Redirect /blog/2015/01/ /about-us/blog/?filter1_from_date=01%2F01%2F2015&filter1_to_date=01%2F31%2F2015
# Redirect /blog/2015/02/ /about-us/blog/?filter1_from_date=02%2F01%2F2015&filter1_to_date=02%2F28%2F2015
# Redirect /blog/2015/03/ /about-us/blog/?filter1_from_date=03%2F01%2F2015&filter1_to_date=03%2F31%2F2015
# Redirect /blog/2015/04/ /about-us/blog/?filter1_from_date=04%2F01%2F2015&filter1_to_date=04%2F30%2F2015
# Redirect /blog/2015/05/ /about-us/blog/?filter1_from_date=05%2F01%2F2015&filter1_to_date=05%2F31%2F2015
# Redirect /blog/2015/06/ /about-us/blog/?filter1_from_date=06%2F01%2F2015&filter1_to_date=06%2F30%2F2015
# Redirect /blog/2015/07/ /about-us/blog/?filter1_from_date=07%2F01%2F2015&filter1_to_date=07%2F31%2F2015
# Redirect /blog/2015/08/ /about-us/blog/?filter1_from_date=08%2F01%2F2015&filter1_to_date=08%2F31%2F2015
# Redirect /blog/2015/09/ /about-us/blog/?filter1_from_date=09%2F01%2F2015&filter1_to_date=09%2F30%2F2015
# Redirect /blog/2015/10/ /about-us/blog/?filter1_from_date=10%2F01%2F2015&filter1_to_date=10%2F31%2F2015
# Redirect /blog/2015/11/ /about-us/blog/?filter1_from_date=11%2F01%2F2015&filter1_to_date=11%2F30%2F2015
# Redirect /blog/2015/12/ /about-us/blog/?filter1_from_date=12%2F01%2F2015&filter1_to_date=12%2F31%2F2015
# Redirect /blog/2016/01/ /about-us/blog/?filter1_from_date=01%2F01%2F2016&filter1_to_date=01%2F31%2F2016
# Redirect /blog/2016/02/ /about-us/blog/?filter1_from_date=02%2F01%2F2016&filter1_to_date=02%2F29%2F2016
# Redirect /blog/2016/03/ /about-us/blog/?filter1_from_date=03%2F01%2F2016&filter1_to_date=03%2F31%2F2016
# Redirect /blog/2016/04/ /about-us/blog/?filter1_from_date=04%2F01%2F2016&filter1_to_date=04%2F30%2F2016
# Redirect /blog/2016/05/ /about-us/blog/?filter1_from_date=05%2F01%2F2016&filter1_to_date=05%2F31%2F2016
# Redirect /blog/2016/06/ /about-us/blog/?filter1_from_date=06%2F01%2F2016&filter1_to_date=06%2F30%2F2016
# Redirect /blog/2016/07/ /about-us/blog/?filter1_from_date=07%2F01%2F2016&filter1_to_date=07%2F31%2F2016
# Redirect /blog/2016/08/ /about-us/blog/?filter1_from_date=08%2F01%2F2016&filter1_to_date=08%2F31%2F2016
# Redirect /blog/2016/09/ /about-us/blog/?filter1_from_date=09%2F01%2F2016&filter1_to_date=09%2F30%2F2016
# Redirect /blog/2016/10/ /about-us/blog/?filter1_from_date=10%2F01%2F2016&filter1_to_date=10%2F31%2F2016
# Redirect /blog/2016/11/ /about-us/blog/?filter1_from_date=11%2F01%2F2016&filter1_to_date=11%2F30%2F2016
# Redirect /blog/2016/12/ /about-us/blog/?filter1_from_date=12%2F01%2F2016&filter1_to_date=12%2F31%2F2016
#
#
#
#
#     # Legacy blog category URL's
#
# RedirectMatch	\/blog\/category\/mortgages\/.*$	/about-us/blog/?filter1_topics=Mortgages
# RedirectMatch	\/blog\/category\/mortgages\/mortgage-closing-mortgages\/.*$	/about-us/blog/?filter1_topics=Mortgage+closing
# RedirectMatch	\/blog\/category\/mortgages\/reverse-mortgages\/.*$	/about-us/blog/?filter1_topics=Reverse+mortgages
# RedirectMatch	\/blog\/category\/students\/.*$	/about-us/blog/?filter1_topics=Students
# RedirectMatch	\/blog\/category\/student-loans\/.*$	/about-us/blog/?filter1_topics=Student+loans
# RedirectMatch	\/blog\/category\/financial-education\/.*$	/about-us/blog/?filter1_topics=Financial+education
# RedirectMatch	\/blog\/category\/servicemembers\/.*$	/about-us/blog/?filter1_topics=Servicemembers
# RedirectMatch	\/blog\/category\/older-americans\/.*$	/about-us/blog/?filter1_topics=Older+Americans
# RedirectMatch	\/blog\/category\/featured\/.*$	/about-us/blog/?filter1_topics=Featured
# RedirectMatch	\/blog\/category\/rulemaking\/.*$	/about-us/blog/?filter1_topics=Rulemaking
# RedirectMatch	\/blog\/category\/enforcement\/.*$	/about-us/blog/?filter1_topics=Enforcement
# RedirectMatch	\/blog\/category\/know-before-you-owe\/.*$	/about-us/blog/?filter1_topics=Know+Before+You+Owe
# RedirectMatch	\/blog\/category\/video\/.*$	/about-us/blog/?filter1_topics=Video
# RedirectMatch	\/blog\/category\/video\/livestream\/.*$	/about-us/blog/?filter1_topics=Livestream
# RedirectMatch	\/blog\/category\/credit-cards\/.*$	/about-us/blog/?filter1_topics=Credit+cards
# RedirectMatch	\/blog\/category\/building-the-agency\/.*$	/about-us/blog/?filter1_topics=About+the+Bureau
# RedirectMatch	\/blog\/category\/mortgage-disclosure\/.*$	/about-us/blog/?filter1_topics=Mortgage+disclosure
# RedirectMatch	\/blog\/category\/about-the-bureau\/.*$	/about-us/blog/?filter1_topics=About+the+Bureau
# RedirectMatch	\/blog\/category\/about-the-bureau\/technology\/.*$	/about-us/blog/?filter1_topics=Technology
# RedirectMatch	\/blog\/category\/outreach\/.*$	/about-us/blog/?filter1_topics=Outreach
# RedirectMatch	\/blog\/category\/consumer-advisory-board\/.*$	/about-us/blog/?filter1_topics=Consumer+Advisory+Board
# RedirectMatch	\/blog\/category\/consumer-advisory\/.*$	/about-us/blog/?filter1_topics=Consumer+advisory
# RedirectMatch	\/blog\/category\/consumer-protection\/.*$	/about-us/blog/?filter1_topics=Financial+education
# RedirectMatch	\/blog\/category\/debt-collection-2\/.*$	/about-us/blog/?filter1_topics=Debt+collection
# RedirectMatch	\/blog\/category\/consumer-response\/.*$	/about-us/blog/?filter1_topics=Consumer+Response
# RedirectMatch	\/blog\/category\/complaints\/.*$	/about-us/blog/?filter1_topics=Complaints
# RedirectMatch	\/blog\/category\/consumer-voice\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/bureau-milestones\/.*$	/about-us/blog/?filter1_topics=Bureau+milestones
# RedirectMatch	\/blog\/category\/payday-loans\/.*$	/about-us/blog/?filter1_topics=Payday+loans
# RedirectMatch	\/blog\/category\/financial-empowerment\/.*$	/about-us/blog/?filter1_topics=Financial+Empowerment
# RedirectMatch	\/blog\/category\/fair-lending\/.*$	/about-us/blog/?filter1_topics=Fair+lending
# RedirectMatch	\/blog\/category\/open-gov\/.*$	/about-us/blog/?filter1_topics=Open+government
# RedirectMatch	\/blog\/category\/data\/.*$	/about-us/blog/?filter1_topics=Data
# RedirectMatch	\/blog\/category\/research\/.*$	/about-us/blog/?filter1_topics=Research
# RedirectMatch	\/blog\/category\/credit-scores\/.*$	/about-us/blog/?filter1_topics=Credit+reporting
# RedirectMatch	\/blog\/category\/credit-report\/.*$	/about-us/blog/?filter1_topics=Credit+reporting
# RedirectMatch	\/blog\/category\/checking\/.*$	/about-us/blog/?filter1_topics=Checking
# RedirectMatch	\/blog\/category\/save-the-date\/.*$	/about-us/blog/?filter1_topics=Save+the+date
# RedirectMatch	\/blog\/category\/field-hearing\/.*$	/about-us/blog/?filter1_topics=Field+hearing
# RedirectMatch	\/blog\/category\/supervision\/.*$	/about-us/blog/?filter1_topics=Supervision
# RedirectMatch	\/blog\/category\/supervision\/nonbanks\/.*$	/about-us/blog/?filter1_topics=Nonbanks
# RedirectMatch	\/blog\/category\/supervision\/bank-supervision-supervision\/.*$	/about-us/blog/?filter1_topics=Bank+supervision
# RedirectMatch	\/blog\/category\/remittances\/.*$	/about-us/blog/?filter1_topics=Money+transfers
# RedirectMatch	\/blog\/category\/private-student-loans\/.*$	/about-us/blog/?filter1_topics=Student+loans
# RedirectMatch	\/blog\/category\/scams\/.*$	/about-us/blog/?filter1_topics=Scams
# RedirectMatch	\/blog\/category\/uncategorized\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/website\/.*$	/about-us/blog/?filter1_topics=Online+resources
# RedirectMatch	\/blog\/category\/national-consumer-protection-week\/.*$	/about-us/blog/?filter1_topics=National+Consumer+Protection+Week
# RedirectMatch	\/blog\/category\/parents\/.*$	/about-us/blog/?filter1_topics=Parents
# RedirectMatch	\/blog\/category\/everyone-has-a-story\/.*$	/about-us/blog/?filter1_topics=Everyone+has+a+story
# RedirectMatch	\/blog\/category\/consumer-engagement\/.*$	/about-us/blog/?filter1_topics=Consumer+Engagement
# RedirectMatch	\/blog\/category\/tell-your-story\/.*$	/about-us/blog/?filter1_topics=Everyone+has+a+story
# RedirectMatch	\/blog\/category\/auto-loans\/.*$	/about-us/blog/?filter1_topics=Auto+loans
# RedirectMatch	\/blog\/category\/credit-unions\/.*$	/about-us/blog/?filter1_topics=Credit+unions
# RedirectMatch	\/blog\/category\/arbitration\/.*$	/about-us/blog/?filter1_topics=Arbitration
# RedirectMatch	\/blog\/category\/saving\/.*$	/about-us/blog/?filter1_topics=Saving
# RedirectMatch	\/blog\/category\/community-banks\/.*$	/about-us/blog/?filter1_topics=Community+banks
# RedirectMatch	\/blog\/category\/open-for-suggestions\/.*$	/about-us/blog/?filter1_topics=Open+for+Suggestions
# RedirectMatch	\/blog\/category\/explainer\/.*$	/about-us/blog/?filter1_topics=Explainer
# RedirectMatch	\/blog\/category\/cfpb-ombudsman\/.*$	/about-us/blog/?filter1_topics=CFPB+Ombudsman
# RedirectMatch	\/blog\/category\/ecoa\/.*$	/about-us/blog/?filter1_topics=ECOA
# RedirectMatch	\/blog\/category\/prepaid-cards\/.*$	/about-us/blog/?filter1_topics=Prepaid+cards
# RedirectMatch	\/blog\/category\/consumer-story\/.*$	/about-us/blog/?filter1_topics=Consumer+story
# RedirectMatch	\/blog\/category\/military\/.*$	/about-us/blog/?filter1_topics=Servicemembers
# RedirectMatch	\/blog\/category\/academic-research-council\/.*$	/about-us/blog/?filter1_topics=Academic+Research+Council
# RedirectMatch	\/blog\/category\/our-team\/.*$	/about-us/blog/?filter1_topics=About+the+Bureau
# RedirectMatch	\/blog\/category\/credit-card-act\/.*$	/about-us/blog/?filter1_topics=Credit+cards
# RedirectMatch	\/blog\/category\/overdrafts\/.*$	/about-us/blog/?filter1_topics=Overdrafts
# RedirectMatch	\/blog\/category\/jobs\/.*$	/about-us/blog/?filter1_topics=Careers
# RedirectMatch	\/blog\/category\/debit-cards\/.*$	/about-us/blog/?filter1_topics=Debit+cards
# RedirectMatch	\/blog\/category\/project-catalyst\/.*$	/about-us/blog/?filter1_topics=Project+Catalyst
# RedirectMatch	\/blog\/category\/fraud\/.*$	/about-us/blog/?filter1_topics=Fraud
# RedirectMatch	\/blog\/category\/foreclosure\/.*$	/about-us/blog/?filter1_topics=Foreclosure
# RedirectMatch	\/blog\/category\/young-americans\/.*$	/about-us/blog/?filter1_topics=Youth
# RedirectMatch	\/blog\/category\/medical-debt\/.*$	/about-us/blog/?filter1_topics=Medical+debt
# RedirectMatch	\/blog\/category\/youth\/.*$	/about-us/blog/?filter1_topics=Youth
# RedirectMatch	\/blog\/category\/financial-literacy-month\/.*$	/about-us/blog/?filter1_topics=Financial+Literacy+Month
# RedirectMatch	\/blog\/category\/mortgage-closing\/.*$	/about-us/blog/?filter1_topics=Mortgage+closing
# RedirectMatch	\/blog\/category\/regulations\/.*$	/about-us/blog/?filter1_topics=Regulations
# RedirectMatch	\/blog\/category\/community-bank-advisory-council\/.*$	/about-us/blog/?filter1_topics=Community+Bank+Advisory+Council
# RedirectMatch	\/blog\/category\/bank-supervision\/.*$	/about-us/blog/?filter1_topics=Supervision
# RedirectMatch	\/blog\/category\/equal-opportunity\/.*$	/about-us/blog/?filter1_topics=Equal+opportunity
# RedirectMatch	\/blog\/category\/from-the-director\/.*$	/about-us/blog/?filter1_topics=From+the+director
# RedirectMatch	\/blog\/category\/compliance\/.*$	/about-us/blog/?filter1_topics=Compliance
# RedirectMatch	\/blog\/category\/tribal-governments\/.*$	/about-us/blog/?filter1_topics=Tribal+governments
# RedirectMatch	\/blog\/category\/doing-business-with-us\/.*$	/about-us/blog/?filter1_topics=Procurement
# RedirectMatch	\/blog\/category\/taxes\/.*$	/about-us/blog/?filter1_topics=Taxes
# RedirectMatch	\/blog\/category\/banking-3\/.*$	/about-us/blog/?filter1_topics=Banking
# RedirectMatch	\/blog\/category\/predatory-lending\/.*$	/about-us/blog/?filter1_topics=Student+loans
# RedirectMatch	\/blog\/category\/mymoney-gov\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/financial-crisis\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/speech\/.*$	/newsroom/?filter_category=Speech
# RedirectMatch	\/blog\/category\/access-to-finance\/.*$	/about-us/blog/?filter1_topics=Access+to+finance
# RedirectMatch	\/blog\/category\/civil-penalty-fund\/.*$	/about-us/blog/?filter1_topics=Civil+Penalty+Fund
# RedirectMatch	\/blog\/category\/spanish\/.*$	/about-us/blog/?filter1_topics=CFPB+en+Espanol
# RedirectMatch	\/blog\/category\/small-business\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/disability\/.*$	/about-us/blog/?filter1_topics=Persons+with+disabilities
# RedirectMatch	\/blog\/category\/this-week\/.*$	/about-us/blog/?filter1_topics=About+the+Bureau
# RedirectMatch	\/blog\/category\/faith-based-community\/.*$	/about-us/blog/?filter1_topics=Outreach
# RedirectMatch	\/blog\/category\/home-equity-loan\/.*$	/about-us/blog/?filter1_topics=Home+equity+loan
# RedirectMatch	\/blog\/category\/fair-housing-act\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/small-business-review\/.*$	/about-us/blog/?filter1_topics=Small+business+review
# RedirectMatch	\/blog\/category\/design\/.*$	/about-us/blog/?filter1_topics=Design
# RedirectMatch	\/blog\/category\/partnerships\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/fair-credit-reporting-act\/.*$	/about-us/blog/?filter1_topics=Credit+reporting
# RedirectMatch	\/blog\/category\/consumers-with-disabilities\/.*$	/about-us/blog/?filter1_topics=Persons+with+disabilities
# RedirectMatch	\/blog\/category\/money-transfers\/.*$	/about-us/blog/?filter1_topics=Money+transfers
# RedirectMatch	\/blog\/category\/diversity\/.*$	/about-us/blog/?filter1_topics=Diversity
# RedirectMatch	\/blog\/category\/security\/.*$	/about-us/blog/?filter1_topics=Security
# RedirectMatch	\/blog\/category\/mobile-financial-services\/.*$	/about-us/blog/?filter1_topics=Mobile+financial+services
# RedirectMatch	\/blog\/category\/equal-credit-opportunity-act\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/fair-debt-collection-practices-act\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/real-estate-settlement-procedures-act\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/truth-in-lending-act\/.*$	/about-us/blog/
# RedirectMatch	\/blog\/category\/virtual-currency\/.*$	/about-us/blog/?filter1_topics=Virtual+currency
# RedirectMatch	\/blog\/category\/equal-treatment\/.*$	/about-us/blog/?filter1_topics=Discrimination
#
#
# # FinEd Resources downloads
# RedirectMatch ^/money-as-you-grow/(.*)\.pdf$ /static/fin-ed-resources/money-as-you-grow/$1.pdf
# RedirectMatch ^/library-resources/(.*)\.(docx|pdf|png|txt|zip)$ /static/fin-ed-resources/library-resources/$1.$2
# RedirectMatch ^/tax-preparer-resources/(.*)\.(docx|pdf|png|txt|zip)$ /static/fin-ed-resources/tax-preparer-resources/$1.$2
#
# # A bad link of the header screenshot exists in a few places:
# Redirect /static/img/fmc-about-us-540x300.png /static/img/fmc-about-us-540x300.jpg
#
# # ILSA vanity URL
# RedirectMatch (?i)^/ILSA([/]?)$ /policy-compliance/guidance/interstate-land-sales-registration/
#
# # Link from payday lending disclosures
# RedirectMatch (?i)^/payday([/]?)$ /askcfpb/search/?selected_facets=category_exact:payday-loans
#
# # Link from Meals on Wheels placemats
# RedirectMatch (?i)^/oa([/]?)$ /askcfpb/1935/how-can-i-protect-myself-and-others-i-care-about-from-fraud-and-scams.html
#
# # Auto Loans vanity URL
# RedirectMatch (?i)^/auto(\-?)loans([/]?)$ /consumer-tools/auto-loans/
