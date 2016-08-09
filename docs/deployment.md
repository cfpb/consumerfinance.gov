# Deployment

Everything that is part of cfgov-refresh and its dependencies are deployed as part of the cf.gov deployment jobs. For needs that are outside of the standard deployment process (perhaps relating to regular data loading or manipulation), additional jobs will need to be created.

Projects that are independent of cfgov-refresh will need to provide their own deployment process, and all jobs they require. They will not be automatically included in the cf.gov deployment process, and will not be on the cf.gov release cadence. 

All new deployment jobs, jobs that run in addition to the cf.gov depoyment jobs, as well as independent jobs, must be implemented with Jenkins-as-code.

## Deployment QA

All code that gets merged into the cfgov-refresh master must have adequate tests, as appropriate for the nature of the code. 

This could potentially include unit tests, browser tests, and 508-compliance tests.

There should be no drop in test coverage for cfgov-refresh.

Regular releases of cf.gov on our release cadence are automated, presuming:

- All unit tests pass 
- All functional tests pass
- There is no reduction in test coverage from the last release tagging

## Current deployment process

The current cf.gov deployment process requires running the following individual Jenkins jobs manually, in the following order:

- cf.gov-beta-frontend-build, build with the tag name of the latest release, i.e. 3.5.2.
- cf.gov-fab-deploy-django, build with DEPLOY_ENV Staging
- cf.gov-fab-deploy-django, build with DEPLOY_ENV ***PRODUCTION***

The following teams and individuals have the necessary access to deploy cf.gov releases:

- Ross Karchner
- Scott Cranfill
- Will Barton
- Bill Higgins
- Serghei Gorobet
- The Software Delivery team
