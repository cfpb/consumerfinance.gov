describe('Page meta data', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  // This test should be paused or altered while our homepage is redirecting
  xit('should include correct template name path', () => {
    cy.get('head meta[name=template]').should(
      'have.attr',
      'content',
      'v1/home_page/home_page.html',
    );
  });
});
