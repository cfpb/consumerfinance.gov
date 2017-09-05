# Setting up new projects

All new code should start in the [cfgov-refresh repository](https://github.com/cfpb/cfgov-refresh) unless the following is true:

- It does not require integration with CMS
- It is not expected to match the look and feel of the larger site (in fact "very different" is preferable to "almost the same")
- It must be pip installable like any other dependency. 

If a project meets this criteria, it is important to note that while the app itself is not necessarily tied to the cf.gov platform’s release cadence, its dependencies are. Such projects must also maintain it's own continuous integration pipeline and build server.

For everything else, all code in the master branch is subject to a regular release cadence. Features that must go live on a certain date should be hidden by feature flags. Deployments should not be timed to coincide with announcements, press releases, speeches, or other events. The code should be already deployed and waiting for the feature to be turned on by a site manager. See “Feature Flags”.

Rather than using “classic” Django views added to urls.py, when feasible an app should provide singleton Wagtail Page. See “Wagtail Pages”.

## Decision Matrix

Product | Content Pages | APIs | HTML5 API Clients ("single page apps") | Traditional Web Apps 
------- | ------------- | ---- | -------------------------------------- | --------------------
What to build | Wagtail page types and templates | Django app using Django REST Framework | The API (if needed) and Wagtail page type and template to host the client | A standard models / forms / views-based Django app. Often calling internal/external APIs
Where does the code live | cfgov-refresh | cfgov-refresh (see exceptions) | cfgov-refresh | cfgov-refresh (see exceptions)
How to start | Extend our existing library of page types and molecules | create a Django app in the "api's" namespace | Build the API first, then create a wagtail page to host the tool | Create a Django app at the top level of the repo. When feasible, consider providing Wagtail page-types instead of traditional views
How to ship | With release cycle | With release cycle | Consider getting APIs deployed well in advance | with release cycle | with release cycle
How to change | See below | With the release cycle | Use [API versioning](http://www.django-rest-framework.org/api-guide/versioning/) to avoid breaking existing code | See below | Generally with the release cycle. If using Wagtail, see guidelines below. If not, use feature flags to hide changes that must go live at a particular time/date.

## How to handle Wagtail changes

### Minor visual updates to a page

- make the changes as part of the release cadence

### Extensive visual changes to a page

- create a new template to reflect the new design
- edit the page type to allow for switching between old and new templates.
- on build and staging servers, feel free to switch back and forth between the designs

### Visual and minor data model changes

- make the data model changes in such a way that doesn't break the current template
- follow the "extensive visual changes to a page" guidance above to make the visual changes

### Major data model changes

- create a new page type, and the corresponding template
- Editors can then replace the old page with the new one, at will

## Front-end Resources

Front-end resources should conform to [CFPB development standards](https://github.com/cfpb/development) and should use atomic elements, organisms, existing structure and convention. When applicable, front-end components should be added to Capital Framework using atomic design principles.

Projects that will be part of cfgov but live in their own repositories should:

- follow file-naming conventions for their front-end resources to avoid collisions (eg, project_name.js rather than main.js) OR follow resource folder structure conventions
- where possible, follow front-end guidelines/templates for new projects, including build processes and testing setup
- where necessary, follow a suggested approach for sharing resources (JavaScript/CSS) that are internal to cfgov-refresh
