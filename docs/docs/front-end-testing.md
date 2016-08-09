# Front-End Testing

Extol the [testing pyramid](https://docs.google.com/presentation/d/1NFjgq5SbQ4crNi06SplyqZQ-K9o5RX966AoRVEB38Yg/pub?start=false&loop=false&delayms=3000&slide=id.g18ef6d797_047).

[![Testing pyramid](http://i.imgur.com/1hQdxod.png)](https://docs.google.com/presentation/d/1NFjgq5SbQ4crNi06SplyqZQ-K9o5RX966AoRVEB38Yg/pub?start=false&loop=false&delayms=3000&slide=id.g18ef6d797_047)

## Unit tests

If your code has logic, it should have unit tests. As seen in the pyramid, unit tests should comprise the majority of your tests. Why? Unit tests can be executed quickly, they can be easily automated, they're maintainable and they promote good practices by requiring your code to be written in concise, modular chunks.

A unit test verifies that a single discrete piece of your codebase works as expected. That "piece" could be a JavaScript function, a CommonJS/AMD module or some other unit of functionality. It's vaguely defined but don't let that scare you. Start by choosing one of the test frameworks below and writing tests for individual JavaScript methods. There are many guides about [writing](https://github.com/nelsonic/learn-mocha) [JavaScript](http://alistapart.com/article/writing-testable-javascript) [unit](http://www.smashingmagazine.com/2012/06/27/introduction-to-javascript-unit-testing/) [tests](http://www.htmlgoodies.com/beyond/javascript/testing-javascript-using-the-jasmine-framework.html) that serve as great introductions. At CFPB we like to separate our JavaScript into discrete [npm modules](https://github.com/cfpb/front-end/blob/master/npm.md). This makes testing easier because each module includes self-contained tests.

### Test frameworks
- [Mocha](http://mochajs.org) is a slick, simple testing framework for Node and browser JavaScript with asynchronous support and a [slew of reporters](http://mochajs.org/#reporters), including [TAP](http://en.wikipedia.org/wiki/Test_Anything_Protocol) output.
- [Jasmine](https://github.com/jasmine/jasmine) shares basic semantics with [Mocha](http://mochajs.org), but also includes lots of nice assertion helpers, object [spies](http://jasmine.github.io/2.2/introduction.html#section-Spies), and async support.
- [Tape](https://www.npmjs.com/package/tape) is a [TAP](http://en.wikipedia.org/wiki/Test_Anything_Protocol)-producing test harness for Node with great asynchronous support. Check out the [Testling tape guide](https://ci.testling.com/guide/tape).

Check out 18f's excellent [testing cookbook](https://pages.18f.gov/testing-cookbook/) for more best practices.

## Code coverage

The goal is to have all of your code covered by unit tests. Tools known as code coverage reporters will tell you what percentage of your codebase is covered by tests. Owning A Home uses [grunt-mocha-istanbul](https://github.com/pocesar/grunt-mocha-istanbul) to [integrate istanbul with their Mocha tests](https://github.com/cfpb/owning-a-home/blob/3192922393461295edf9803eec677512704b75dc/Gruntfile.js#L388-L401). When OAH tests are run using `grunt test`, [Istanbul](https://gotwarlost.github.io/istanbul/) prints the coverage % to the command line and generates an interactive HTML code coverage report in `test/coverage`.

![Istanbul report](http://i.imgur.com/2lsQluA.png)

![Istanbul report](http://i.imgur.com/oJYfZCN.png)

## Integration tests

Integration tests test the points at which your front-end JavaScript communicates with your project's back-end. These tests run slower than unit tests because they interact with an external environment. When building single page applications, integration tests usually come in the form of API tests.

Owning A Home uses Selenium and Behave to execute [feature files](https://github.com/cfpb/owning-a-home/tree/556c33e090ed5fe3cfe72cb7262312d5914d41ff/test/api_testing/features) that verify their API is working as expected. If the OAH API starts returning data in a format unexpected by the front-end, these integration tests will immediately start failing, alerting developers to the problem. Integration tests are also useful for detecting down or slow communication channels.

## Browser tests

When building browser-based applications, systems tests are browser (otherwise known as GUI) tests. They verify that the front-end code operates as expected in environments similar to the end-users'. They are slow and expensive to write and maintain. They break easily when the GUI is modified. But they are an incredibly important method of ensuring your application is operating correctly.

They are often written in languages that can be understood by non-developers, traditionally business analysts. Owning A Home's [browser tests](https://github.com/cfpb/owning-a-home/tree/556c33e090ed5fe3cfe72cb7262312d5914d41ff/test/browser_testing) are written in [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin). Most CFPB projects use [behave](http://pythonhosted.org/behave/) for browser testing. After [installing](http://pythonhosted.org/behave/install.html) it, check out their [tutorial](http://pythonhosted.org/behave/tutorial.html) to learn how to use it. Check out OAH's browser tests for a comprehensive example.
