# Deployment

Everything that is part of cfgov-refresh and its dependencies are deployed as part of the cf.gov deployment jobs. For needs that are outside of the standard deployment process (perhaps relating to regular data loading or manipulation), additional jobs will need to be created.

Projects that are independent of cfgov-refresh will need to provide their own deployment process, and all jobs they require. They will not be automatically included in the cf.gov deployment process, and will not be on the cf.gov release cadence. 

All new deployment jobs, jobs that run in addition to the cf.gov deployment jobs, as well as independent jobs, must be implemented with [Jenkins-as-code](https://github.com/cfpb/jenkins-automation).

## Deployment QA

All code that gets merged into the cfgov-refresh master must have adequate tests, as appropriate for the nature of the code. 

This could potentially include unit tests, browser tests, and 508-compliance tests.

There should be no drop in test coverage for cfgov-refresh.

Regular releases of cf.gov on our release cadence are automated, presuming:

- All unit tests pass 
- All functional tests pass
- There is no reduction in test coverage from the last release tagging

## Current deployment process

The current cf.gov deployment process requires running the cf.gov-pipeline-build Jenkins pipeline job, with the release tag to deploy and the environment to which it should be deployed.

The pipeline will invoke the following jobs, in order:

- cf.gov-frontend-build, which builds the front-end assets for cfgov-refresh
- cf.gov-deploy-django, which takes the cfgov-refresh build, and uses [drama-free-django](https://github.com/cfpb/drama-free-django) to build a deployable artifact for all of cf.gov and its requirements, and then deploys the artifact to the appropriate servers for the selected environment.

Any back-end developer on the platform team should be able to assist with deployments. You may also contact the following individually:

- Ross Karchner
- Scott Cranfill
- Will Barton
- Bill Higgins
- Serghei Gorobet
- The Software Delivery team
