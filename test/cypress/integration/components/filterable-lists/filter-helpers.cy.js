export class Filter {
  apply() {
    return cy.get('form[action="."]').submit();
  }

  clear() {
    cy.get('.a-btn__warning').click({ force: true });
  }

  typeAheadLanguage(name) {
    return cy.get('#o-filterable-list-controls_language').type(name);
  }

  clickLanguage(name) {
    cy.get('#o-filterable-list-controls_language').click();
    return cy.get(`label.o-multiselect_label[for="language-${name}"]`).click();
  }

  formatOptionFromString(str) {
    return str
      .split('\n')
      .pop()
      .trim()
      .replace(/(?:and|[,'])+/g, '')
      .split(/ +/)
      .join('-')
      .toLowerCase();
  }

  getCategory() {
    // return the list of categories
    return cy
      .get('[data-cy=categories-heading]')
      .siblings()
      .find('[data-cy=multiselect-option]');
  }

  getCategoryLabel(name) {
    return cy.get(`[for="categories-${name}"]`);
  }

  clickCategory(option) {
    const sel = `[data-option=${option}`;
    cy.get('[data-cy=categories-heading]').click();
    return cy.get(sel).click();
  }

  typeAheadTopic(name) {
    return cy.get('#o-filterable-list-controls_topics').type(name);
  }

  getTopic() {
    return cy.get('[id^="topics-"]');
  }

  getTopicLabel(name) {
    return cy.get(`[for="topics-${name}"]`);
  }

  clickTopic(name) {
    const topic = name.split(' ').join('-').toLowerCase();
    cy.get('#o-filterable-list-controls_topics').click();
    return cy.get(`label.o-multiselect_label[for="topics-${topic}"]`).click();
  }

  expandable() {
    return cy.get('.o-expandable');
  }

  expandableCue(name) {
    return cy.get(`.o-expandable_cue .o-expandable_cue-${name}`);
  }

  expandableTarget() {
    return cy.get('.o-expandable_header');
  }

  search() {
    return this.expandableTarget();
  }

  open() {
    return this.expandableCue('open').click();
  }

  close() {
    return this.expandableCue('close').click();
  }

  show() {
    return this.expandableTarget().first().click();
  }

  hide() {
    return this.expandableTarget().last().click();
  }
}
