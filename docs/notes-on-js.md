# Notes on JavaScript Philosophy

We develop simple modules that adhere to the CommonJS [spec](http://wiki.commonjs.org/wiki/Modules/1.0) and [FIRST](https://addyosmani.com/first/) principles.

Our decision to just rely upon vanilla JavaScript was born out our desire to be lightweight 
and performant. This decision has resulted in a better understanding of how to construct applications,
address cross browser issues, and performance tune on mobile.  I want to stress that we weren't ideologically opposed to using other frameworks or libraries. We just made a decision based on project complexity and skill of the team. 

## jQuery

jQuery plays such a prominent role within front-end web development that I wanted to address the pros / cons of using the library separately.

**Pros:**

- Easy to learn and great documentation.
- Great ecosystem and community support in the form plugins, Stackoverflow.com, and GitHub.com.  
- High level of availability through CDNS enables apps to take advantage of browser cache loading.  
- Many other frameworks/libraries are built upon jQuery allowing beginners to leverage their jQuery knowledge (i.e., Twitter Bootstrap, jQuery UI).
- jQuery plugin support is tremendous allowing teams to quickly add specific functionalities to their applications.


**Cons:**

- Obscures the underlying technologies that FEWDS should be learning 
  (JavaScript, DOM events, DOM manipulation).     
- Leads to application bloat if not loading off of a CDN (minimum 60KB).
- Requires you to load entire library just to use a single functionality.
  
- Overuse of jQuery paradigms leads to bad JS architecture 
  (i.e., Event callback hell; Function call chaining hell).
    
- Using native DOM methods results in superior performance.

## References

[Stop writing slow JavaScript](http://ilikekillnerds.com/2015/02/stop-writing-slow-javascript/)

[Advantages of using pure JavaScript over jQuery](http://programmers.stackexchange.com/questions/166273/advantages-of-using-pure-javascript-over-jquery)

