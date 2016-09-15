# What’s new?

## Guiding principles
- Reverse the sprawl of technologies and repositories left by the last 5 years of consumerfinance.gov development. 
- Reduce risk by integrating earlier and implementing a single release cadence for the entire site.
- We don’t deploy code to coincide with announcements, and events. 
- Prefer using and/or extending the CMS and it’s primitives (page types, atomic design elements, etc) over the creation of “apps” that own a particular URL space.

## Benefits
- By centering most work on the cfgov-refresh, it becomes easier to understand what’s happening, easier to communicate about the state of the site, easier to develop on, and simpler to deploy.
- By working with the CMS, we empower editors to determine when a particular page or section goes live, and can provide a way to edit the incidental text on a page. 

## Practical impacts
- Any new work that will appear on consumerfinance.gov should be built with Django, and (subject to guidelines below) live in the primary code repo for the site (cfgov-refresh). 
- If a particular page, section, or feature can not go live before a particular date or time, then it must be hidden with feature flags or controlled via the CMS. Simply merging code (or updating a dependency) must not result in such things being revealed.


### New build approach

**For projects being developed outside of cfgov-refresh**, the relationship with the project (and particularly the ‘build’ server) is changing. Under the old system, we maintained a separate ‘requirements’ file for build, content, and production. The ‘build’ requirements generally grabbed the master branch of the app, and we would pin a particular version for content and production.

What we want to do now is quite a bit different. These apps will be treated like any other python dependency (ie, always pinned to a particular version). The ‘build’ server will reflect the master branch of cfgov-refresh, but for all other projects will only reflect the current pinned version reflected in requirements.txt, and changing that version requires a pull request. We then move complete releases of the site through the QA and deployment process described below under “release cadence”

In short: if your code is being maintained outside of cfgov-refresh, you will need to provide your own ‘build’ environment and CI pipeline. We are working with the delivery team to make this less painful than it sounds.
