# TDP Survey System

Three web-based surveys are implemented via dynamically-created Django forms and custom JavaScript.

* https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/survey/3-5/
* https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/survey/6-8/
* https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/survey/9-12/

The [django-formtools](https://django-formtools.readthedocs.io/en/latest/) library is used to allow each of the forms to be broken across multiple pages. While taking a survey, users can return to previous pages and all their responses are stored in their browser for the length of the session.

Each survey is created within the server as a Survey object ([surveys.py](./surveys.py)) which is populated with all the survey’s questions, answers, and the score value of each answer. Upon server startup, each Survey object is created--by reading comma-separated values files (Survey.factory)--and it supplies the view system with custom Django form classes for each logical page of questions. A SurveyWizard class ([views.py](./views.py)) binds all the survey’s form pages into a single logical form that operates like a Django TemplateView.

We also use a custom SurveyForm ([forms.py](./forms.py)) subclass of Django Form allowing needed customization of the label markup.

When a survey is completed (SurveyWizard.done), the response data is used to get a set of scores for each question in the survey.

## Results Page

When a user completes a survey, the scores for its three parts are obscured and packed into a text code and this code is temporarily stored in a session browser cookie. This allows the Results page to display custom content based on the user’s scores (and without students ending up with scoring URLs in their browsing history). The code is also cryptographically signed via Django’s Signer class so that students cannot tamper with it to change their scores.

The Results page (student_results in [views.py](./views.py)) is built with content based on the part scores using a Jinja2 template and data in a ResultsContent object. ResultsContent ([resultsContent.py](./resultsContent.py)) is populated from CSV data that determines how to place scores within six different segments.

## Sharing

When the user wants to share results ([result-page.js](../unprocessed/apps/teachers-digital-platform/js/survey/result-page.js)), the page similarly obscures the user’s initials into a code format and the two codes are embedded into a “shared URL”.

Note: The data holding the user’s PII is only placed in the hash portion of the URL so that it’s never sent to the CFPB server nor to Google Analytics servers.

Both the student scores code and the shared URL code are identical and validated by the Django form class SharedUrlForm, with the code either coming from the querystring (shared URLs) or a cookie (student results).

When the teacher accesses a shared URL, the user’s initials are decoded from the URL’s hash portion ([results-page.js](../unprocessed/apps/teachers-digital-platform/js/survey/result-page.js)) and the original Results page is constructed with minimal differences.

## Survey Features

If a user reloads the page or returns to a previous page before submitting the form, their answers are repopulated in the page. This is done by storing all selections in the browser’s sessionStorage API immediately upon making them ([ChoiceField.js](../unprocessed/apps/teachers-digital-platform/js/survey/ChoiceField.js)).

As each question is answered, a ProgressBar component ([ProgressBar.js](../unprocessed/apps/teachers-digital-platform/js/survey/ProgressBar.js)) tracks overall progress and provides events to draw a circular meter.

Although a user can jump multiple pages backwards via “edit” links, technical limitations require always moving forward via the “Next” submit buttons at the bottom of the screen.

If a page is submitted without all questions answered, the user is shown an error message with links to scroll back to all unanswered questions.

Progress through pages is tracked on a set of section buttons ([SectionLink.js](../unprocessed/apps/teachers-digital-platform/js/survey/SectionLink.js)) that have various features based on the current state:

1.  The current section is blue.
2.  Previous sections are green and can be navigated to.
3.  Completed sections ahead of the user are white.
4.  Unvisited sections are gray.
5.  All completed sections have a green check mark.

## Student Results Features

Below the results, students are given options to print and/or share their results page (result-page.js). Both buttons launch modal dialogs and ask for the user’s initials, which are placed in the heading of the page and encoded into the shared URL ([initials.js](../unprocessed/apps/teachers-digital-platform/js/survey/initials.js)). The student need only enter them once.

Once the Results page is displayed, the user’s original selections are cleared and the user cannot return to the survey.

## Modal Dialogs

Several features are presented inside modal dialogs ([modals.js](../unprocessed/apps/teachers-digital-platform/js/modals.js)). All modals can be “escaped” (taking no action) via an explicit “close” button, pressing the “Escape” key, or clicking outside the modal contents. All destructive operations are presented via red buttons.

In accordance with best accessibility practices:

* Modals are given appropriate markup ARIA attributes to denote a dialog.
* They “trap” keyboard focus within the dialog content.
* When closed, they return focus to the element that opened them.
