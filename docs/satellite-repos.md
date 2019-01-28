# Satellite repos


Satellite repositories provide functionality or site content that is optionally included as part of the website, but not included in this repository. Some satellite repos exist to allow certain functionality to be run or tested without needing to set up the full website.

!!! note "Thinking about making a new satellite repo?"
    Satellite projects were originally built to be imported into the consumerfinance.gov website before we started using Wagtail to manage site content. We now prefer to build projects as apps inside the cfgov-refresh repo. For more info, refer to the "Setting up new project code for consumerfinance.gov" page on the CFGOV/platform wiki on GHE.

We have seven satellite repos that are maintained outside of the cfgov-refresh codebase:

- [ccdb5_api](https://github.com/cfpb/ccdb5-api)
- [ccdb5_ui](https://github.com/cfpb/ccdb5-ui)
- [college_costs](https://github.com/cfpb/college-costs)
- [comparisontool](https://github.com/cfpb/django-college-costs-comparison)
- [owning_a_home_api](https://github.com/cfpb/owning-a-home-api)
- [retirement](https://github.com/cfpb/retirement)
- [teachers_digital_platform](https://github.com/cfpb/teachers-digital-platform)


We import these satellite projects into cfgov-refresh by specifying wheel files for each in [`requirements/optional-public.txt`](https://github.com/cfpb/cfgov-refresh/blob/master/requirements/optional-public.txt).

## Local setup and usage

See ["Usage"](https://cfpb.github.io/cfgov-refresh/usage/#develop-satellite-apps) for local setup and usage instructions.
