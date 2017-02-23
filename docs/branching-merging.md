# Branching and merging

Branches should be named descriptively, preferably in some way that indicates whether they are short-lived feature branches or longer-lived development branches. Short-lived feature branches should be deleted once they are merged into master. 

All pull requests to merge into master must be reviewed by at least one member of the cf.gov platform team. The cf.gov platform team will ensure that these reviews happen in a timely manner. To ensure timely code reviews, please tag all PRs to master with @cfpb/cfgov-backends and @cfpb/cfgov-frontends as appropriate.

When reviewing pull requests, it is important to distinguish between explicit blockers and things that can be addressed in the future or would be nice to have. The latter two can be indicated with 'TODO'. This is best as a simple top-level post after review to summarize the review.

The cfgov-refresh repository makes use of automated testing and linting to ensure the quality, consistency, and readability of the codebase. All pull requests to master must pass all automated tests and must not reduce the code coverage of the codebase. It is the responsibility of the submitter to ensure that the tests pass.

Pull requests that are *not* to master must use GitHub labels in such a way that individuals who are responsible for reviewing those pull requests can easily find them. Pull requests that are works-in-progress must be clearly labeled as such.

Generally, teams working on cf.gov projects should create and collaborate on feature branches, with frequent merges back to master. Teams are responsible for governing their own branches and forks, these guidelines apply to master. 
