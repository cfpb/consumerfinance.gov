# Guidance on how to contribute

> All contributions to this project will be released under the CC0 public domain
> dedication. By submitting a pull request or filing a bug, issue, or 
> feature request, you are agreeing to comply with this waiver of copyright interest.
> Details can be found in our [TERMS](TERMS.md) and [LICENCE](LICENSE).


There are two primary ways to help: 
 - Using the issue tracker, and 
 - Changing the code-base.


## Using the issue tracker

Use the issue tracker to suggest feature requests, report bugs, and ask questions. 
This is also a great way to connect with the developers of the project as well
as others who are interested in this solution.  

Use the issue tracker to find ways to contribute. Find a bug or a feature, mention in
the issue that you will take on that effort, then follow the _Changing the code-base_ 
guidance below.


## Changing the code-base

Generally speaking, you should fork this repository, make changes in your
own fork, and then submit a pull-request. For timely code reviews,
please tag @cfpb/cfgov-backends and @cfpb/cfgov-frontends as appropriate
for your changes.

All new code should have associated unit tests and/or functional tests that 
validate implemented features and the presence or lack of defects. The
overall test coverage of the code-base should not decrease.

Python code is expected to follow 
[PEP8](https://www.python.org/dev/peps/pep-0008/) and 
[not commit atrocities](https://www.youtube.com/watch?v=wf-BqAjZb8M). 
JavaScript, CSS/Less, and markup should follow our 
[front-end standards](https://github.com/cfpb/front-end). 
When in doubt, mimic the styles and patterns in the existing code-base.
