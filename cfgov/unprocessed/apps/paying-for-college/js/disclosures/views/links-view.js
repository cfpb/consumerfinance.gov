import formatURL from '../utils/format-url.js';
import constructScorecardSearch from '../utils/construct-scorecard-search.js';
import $ from '../../../../../js/modules/util/dollar-sign.js';

const linksView = {
  $gradLinkText: $('.graduation-link'),
  $defaultLinkText: $('.loan-default-link'),
  $schoolLinkText: $('.school-link'),
  $scorecardLink: $('.scorecard-link'),

  /**
   * Initializes (and updates) links in Step 3 to the school's website and to
   * a College Scorecard search of related schools
   * @param {object} values - Financial model values
   */
  updateLinks: function (values) {
    this.$gradLinkText = $('.graduation-link');
    this.$defaultLinkText = $('.loan-default-link');
    this.$schoolLinkText = $('.school-link');
    this.$scorecardLink = $('.scorecard-link');
    this.$scorecardSchoolLink = $('.scorecard-school');
    this.setGraduationLink(values);
    this.setLoanDefaultLink(values);
    this.setSchoolLink(values);
    this.setScorecardSearch(values);
    this.setCollegeScorecardLink(values);
  },

  /**
   * Creates a link in Step 2 to the school on the College Scorecard website
   * @param {object} values - Financial model values
   */
  setCollegeScorecardLink: function (values) {
    const scorecardURL =
      'https://collegescorecard.ed.gov/school/?' + values.schoolID;
    this.$scorecardSchoolLink.each((elem) => {
      elem.setAttribute('href', scorecardURL);
      elem.setAttribute('target', '_blank');
      elem.setAttribute('rel', 'noopener noreferrer');
    });
  },

  /**
   * Creates a link in Step 2 to the school's graduation metrics
   * on the College Scorecard website
   * @param {object} values - Financial model values
   */
  setGraduationLink: function (values) {
    const gradURL =
      'https://collegescorecard.ed.gov/school/?' +
      values.schoolID +
      '#graduation';
    this.$gradLinkText.each((elem) => {
      elem.setAttribute('href', gradURL);
      elem.setAttribute('target', '_blank');
      elem.setAttribute('rel', 'noopener noreferrer');
    });
  },

  /**
   * Creates a link in Step 2 to the school's loan default metrics
   * @param {object} values - Financial model values
   */
  setLoanDefaultLink: function (values) {
    const defaultURL =
      'https://nces.ed.gov/collegenavigator/?id=' +
      values.schoolID +
      '#fedloans';
    this.$defaultLinkText.each((elem) => {
      elem.setAttribute('href', defaultURL);
      elem.setAttribute('target', '_blank');
      elem.setAttribute('rel', 'noopener noreferrer');
    });
  },

  /**
   * Creates a link in Step 3 to the school's website if the school has provided
   * a URL in the College Scorecard data
   * @param {object} values - Financial model values
   */
  setSchoolLink: function (values) {
    const schoolURL = formatURL(values.url);
    this.$schoolLinkText.each((elem) => {
      elem.setAttribute('href', schoolURL);
      elem.setAttribute('target', '_blank');
      elem.setAttribute('rel', 'noopener noreferrer');
    });
  },

  /**
   * Modifies the College Scorecard link in step 3 to search for schools that
   * offer a given program near a given ZIP if program and ZIP are specified
   * @param {object} values - Financial model values
   */
  setScorecardSearch: function (values) {
    let pcip = '';
    let zip = '';
    // We're using a 50-mile radius, the most common Scorecard search
    const radius = '50';
    const scorecardURL = this.$scorecardLink.attr('href');

    if ({}.hasOwnProperty.call(values, 'cipCode')) {
      pcip = values.cipCode.slice(0, 2);
    }
    if ({}.hasOwnProperty.call(values, 'zip5')) {
      zip = values.zip5;
    }
    const scorecardQuery = constructScorecardSearch(pcip, zip, radius);
    this.$scorecardLink.attr('href', scorecardURL + scorecardQuery);
  },
};

export default linksView;
