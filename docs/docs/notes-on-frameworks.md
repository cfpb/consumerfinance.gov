# Notes on Frameworks

We opted not to use any frameworks; the application isn't a SPA (single page application) and we didn't think it's level of complexity warranted using one. This might be a mistake and it's worth revisiting this decision, now that we have migrated to Atomic design.

The pros / cons of that decision are as follows:

### Pros

- Smaller builds and minimal markup ( JS, CSS, HTML). Many frameworks are bloated and applications only use a small portion of their functionality / features.
- Learning curve is drastically reduced by not requiring people to learn a new framework.
- Easier for developers to architect / debug the application by requiring a better understanding of DOM, JS modules, and CSS.
- Some frameworks have ventured off the pure JS path, making them inadequate tools for new developers learning JS (React with Redux, Angular 2 via Typescript).

### Cons

- Development time is increased by not relying upon existing frameworks and components.
- Not having a standard way to build components can lead to confusion and non-uniform code.
- Forces developers to really understand DOM manipulation and it's impact on performance (reflows/repaints). React, Angular, and Amp all manage DOM interactions for you through virtual dom and buffering reads / writes. There are very, very few devs that are good at doing this without a framework or library.

# Should projects use frameworks?

The decision to use a framework should be made on a project-by-project basis. It should be driven by the team make-up, project goals, and scope. The only framework we would recommend avoiding at this time is Angular. The Angular project is in a state of flux and it would be better to wait until Angular 2 is a bit more mature.
