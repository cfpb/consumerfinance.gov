# Atomic Design in Capital Framework

### TLDR

- Not easy to update bits and pieces (will require a full versioned release)
- A few components that haven't been converted by the v1 team yet (possibly workshop with entire D&D team):
    - Hero
    - Feature Content Module
    - Forms (partially done)
- Difficult to test how changes affect every project (we should set up a playground)
- Unclear how atomic changes will affect components
- Documentation is incomplete (working on that currently)
- Unclear how future changes will be updated in Wagtail (should platform own this?)

## Details

Now that v1 is out there, we've been getting a lot of interest about updating Capital Framework with the Atomic Design Principles to build better reusable and consistent design patterns. As we complete the documentation process, I've been collecting concerns, thoughts, and next steps we'll need to take to make that possible. Unfortunately, a large part of understanding Atomic Design happens when working with it yourself, but we can make that process easier by updating Capital Framework to utilize and document the patterns we've built.

#### It's not easy to update bits and pieces

While it'd be nice to update Capital Framework one module at a time, much like we did during the Design Surge, it's super complicated to mix atomic and non-atomic components. You end up with either duplication of code, or an entanglement between the components. Instead, it makes more sense to start an atomic release branch and port components there.

Components would be ported as time allows, then released as whole as the next major version (aka v4). Older, unsupported projects could stay on v3, but newer projects would be updated to v4. This means some duplication of work going forward, but similar to jQuery and other projects, we could set a sunset date for v3 and only provide critical updates past that date.

#### There are some missing and unfinished components

We covered quite a lot in v1, but there are a few components that haven't been converted and some that require further work. At the same time, one of the lessons we learned during the process is that it's difficult to understand all of the principles without working with them. While the Platform team will be taking on much of this work, there's no reason to lay it all on their shoulders, and spreading the work around will enable those outside v1 and Platform to become more comfortable with designing and building atomically.

So far I've received a good response to hosting a half-day workshop for both designers and developers at the July regroup to go over the principles and begin converting the Hero and FCM. A group event would allow us to pass along our knowledge and lessons learned in person, while also giving the rest of the team a chance to work with real designs and code, making it a lot easier to either pick up unfinished work or produce new components or changes based on project work.

#### It's difficult to test how changes will affect other projects

While working within v1 it was pretty easy to test if a change to a component had unintended consequences elsewhere because everything was contained within the project. Despite that, unintended changes did still happen here and there. Once the atomic components are distributed to other projects, the chances of unintended changes becomes a lot higher. While NPM installing your local version of Capital Framework does make it easier to test, standing up cfgov-refresh with all of it's sibling projects is still a burden on those not consistently working on it.

A playground that lives within Capital Framework (but not the documentation site) would make testing for edge cases and unintended issues far easier. As changes are proposed, we would have immediate feedback from live examples of our code base as it exists in production projects. The playground doesn't need to be a full blown live editor like CodePen, static examples that are copied from production to this playground should be more than enough to pass some gut checks.

#### It's unclear how atomic changes will affect current component organization

How will atoms, molecules, and organisms be arranged within a component? How will these changes affect other components that then import those pieces? What happens if a molecule needs to become an organism, or vice versa? These questions will probably need to be fleshed out as we complete the transition work, but it's good to keep them in mind as we go along.

#### It's unclear how component changes will be propagated to Wagtail

If a component's foundation changes (markup, options, etc) how will those changes be passed into the CMS? Will it be the responsibility of the FEWD to make them or will the work be passed to a Platform team BEWD. How will that affect their workload and how should we pass that task along? What will be a reasonable timeline?

For example, if we pass a task to the Platform team mid-sprint, but it couldn't be tackled for one or more sprints, it will create a delay in the release cycle of CF possibly leading to stale code. We will need to be more conscious and do some long term planning in situations where updates come from projects outside of Platform.

#### The documentation is incomplete

The v1 designers have been working on thorough documentation of the components we've created, but the Capital Framework documentation will need to be updated as well. To ensure it happens (I am at fault for this as much as anyone), documentation updates should be strictly enforced when component PRs are opened. If we don't stay on top of it, it'll be the thing that gets pushed off indefinitely.
