describe('Page meta data', () => {
  beforeEach(() => {
    cy.visit('/');
  });
  it('should include correct template name path', () => {
    cy.get('head meta[name=template]').should(
      'have.attr',
      'content',
      'v1/home_page/home_page.html',
    );
  });
});
