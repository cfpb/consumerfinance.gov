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
        '1. What is the filing instructions guide?'
      );
      expect(getSearchData(sections)[0].contents).toContain(
        '1. What is the filing instructions guide?'
      );
      expect(getSearchData(sections)[0].contents).toContain(
        '1. What is the filing instructions guide? The 2024 filing instructions guide is a set of resources to help you file small business lending data with the Consumer Financial Protection Bureau (CFPB) in 2025 covering the period from October 1, 2024 to December 31, 2024. These resources are briefly described in this section and are further detailed throughout this web page in individual sections. These resources may be useful for employees in a variety of roles, for example: Staff who collect, prepare, and submit data Technology support staff Compliance officers The guide includes the following sections: Filing process overview Section 2 provides an overview of the process to file small business lending data with the CFPB. It describes the data submission platform (the platform), which is the system that filers will use to submit their data. It also describes the file format that will be required for submitting the data. Data points Section 3 provides instructions for what to enter into each data field in the small business lending application register (register). A machine-readable version of the data specification is provided. Data validation Section 4 lists the validation requirements that a register must meet before it can be filed with the CFPB. A machine-readable version of the validation specification is provided. Where to get help Section 5 provides a summary of resources available from the CFPB to assist with small business lending rule-related inquiries.'
      );

      expect(getSearchData(sections)[10].title).toEqual(
        'Field 3: Application method'
      );
      expect(getSearchData(sections)[10].contents).toContain(
        'Field 3: Application method'
      );
      expect(getSearchData(sections)[10].contents).toContain(
        'means by which the applicant submitted the application'
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
