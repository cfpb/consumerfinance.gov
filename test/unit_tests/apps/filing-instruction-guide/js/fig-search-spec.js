import { getSearchData } from '../../../../../cfgov/unprocessed/apps/filing-instruction-guide/js/fig-search.js';
import HTML_SNIPPET from '../fixtures/sample-fig-page.js';

let sections;

describe('The Filing Instruction Guide search functionality', () => {
  describe('The search data generator', () => {
    beforeEach(() => {
      // Load HTML fixture
      document.body.innerHTML = HTML_SNIPPET;
    });

    it('should build a list of search items', () => {
      sections = [...document.querySelectorAll('[data-search-section]')];
      expect(getSearchData(sections).length).toEqual(242);

      expect(getSearchData(sections)[0].title).toEqual(
        '1. What is the filing instructions guide?',
      );
      expect(getSearchData(sections)[0].contents).toContain(
        '1. What is the filing instructions guide?',
      );

      expect(getSearchData(sections)[10].title).toEqual(
        'Field 3: Application method',
      );
      expect(getSearchData(sections)[10].contents).toContain(
        'Field 3: Application method',
      );
      expect(getSearchData(sections)[10].contents).toContain(
        'means by which the applicant submitted the application',
      );
    });

    it('should handle a lack of search items', () => {
      sections = [...document.querySelectorAll('[foo]')];
      expect(getSearchData(sections).length).toEqual(0);

      sections = [];
      expect(getSearchData(sections).length).toEqual(0);

      sections = '';
      expect(getSearchData(sections).length).toEqual(0);
    });
  });
});
