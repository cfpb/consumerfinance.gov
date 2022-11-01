const BASE_JS_PATH =
  '../../../../../cfgov/unprocessed/apps/filing-instruction-guide';
const HTML_SNIPPET = require('../fixtures/sample-fig-page');

let search;
let sections;

describe('The Filing Instruction Guide search functionality', () => {
  describe('The search data generator', () => {
    beforeEach(() => {
      // Load HTML fixture
      document.body.innerHTML = HTML_SNIPPET;
      search = require(`${BASE_JS_PATH}/js/fig-search.js`);
    });

    it('should build a list of search items', () => {
      sections = [...document.querySelectorAll('[data-search-section]')];
      expect(search.getSearchData(sections).length).toEqual(100);

      expect(search.getSearchData(sections)[0].title).toEqual(
        '1. What is the FIG?'
      );
      expect(search.getSearchData(sections)[0].contents).toContain(
        '1. What is the FIG?'
      );
      expect(search.getSearchData(sections)[0].contents).toContain(
        'Lorem Ipsum'
      );

      expect(search.getSearchData(sections)[10].title).toEqual(
        'Field 3: Application Method'
      );
      expect(search.getSearchData(sections)[10].contents).toContain(
        'Field 3: Application Method'
      );
      expect(search.getSearchData(sections)[10].contents).toContain(
        'means by which the applicant submitted the application'
      );
    });

    it('should handle a lack of search items', () => {
      sections = [...document.querySelectorAll('[foo]')];
      expect(search.getSearchData(sections).length).toEqual(0);

      sections = [];
      expect(search.getSearchData(sections).length).toEqual(0);

      sections = '';
      expect(search.getSearchData(sections).length).toEqual(0);
    });
  });
});
