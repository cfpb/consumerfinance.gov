const isInViewport = (_chai) => {
  /**
   * Check that a subject element is in the viewport.
   */
  function assertIsInViewport() {
    const subject = this._obj;

    const client = Cypress.$(cy.state('window'));
    const rect = subject[0].getBoundingClientRect();

    this.assert(
      Math.ceil(rect.top) >= 0 &&
        Math.ceil(rect.left) >= 0 &&
        Math.ceil(rect.bottom) <= client.height() &&
        Math.ceil(rect.right) <= client.width(),
      'expected #{this} to be in viewport',
      'expected #{this} to not be in viewport',
      this._obj,
    );
  }

  _chai.Assertion.addMethod('inViewport', assertIsInViewport);
};

chai.use(isInViewport);
