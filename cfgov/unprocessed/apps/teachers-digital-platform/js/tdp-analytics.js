import Analytics from '../../../js/modules/Analytics.js';
import { SCORES_UNSET_KEY } from './survey/config.js';

/* eslint-disable consistent-return */

/**
 * Sends the user interaction to Analytics
 *
 * @param {string} action - The user's action
 * @param {string} label - The label associated with the action
 * @param {string} category - Optional category if it's not eRegs-related
 * @returns {object} Event data
 */
let sendEvent = (action, label, category) => {
  category = category || 'TDP Search Tool';
  const eventData = Analytics.getDataLayerOptions(action, label, category);
  Analytics.sendEvent(eventData);
  return eventData;
};

/**
 * Sends the user survey interaction to Analytics
 *
 * @param {string} action - The user's action
 * @param {string} label - The label associated with the action
 * @returns {object} Event data
 */
let sendSurveyEvent = (action, label) => {
  const category = 'Student Survey Interaction';
  const eventData = Analytics.getDataLayerOptions(action, label, category);
  Analytics.sendEvent(eventData);
  return eventData;
};

/**
 * getExpandable - Find the expandable the user clicked.
 *
 * @param {event} event - Click event
 * @returns {HTMLElement|null} The expandable or null if it's not an expandable
 */
const getExpandable = (event) => {
  let el = event.target.closest('.o-expandable_header');
  el = el ? el : event.target.closest('.o-expandable-facets_target');
  el = el ? el : event.target;

  if (
    el.classList.contains('o-expandable_header') ||
    el.classList.contains('o-expandable-facets_target')
  ) {
    return el;
  }
  return null;
};

/**
 * getExpandableState - Description
 *
 * @param {HTMLElement} expandable - Expandable's HTML element
 * @returns {string} Expandable's state, either `open` or `close`
 */
const getExpandableState = (expandable) => {
  let state = 'collapse';
  if (
    expandable.classList.contains('o-expandable_target__expanded') ||
    expandable.classList.contains('is-open')
  ) {
    state = 'expand';
  }
  return state;
};

/**
 * handleExpandableClick - Listen for clicks within a search page's content
 * and report to GA if they opened or closed an expandable.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleExpandableClick = (event) => {
  const expandable = getExpandable(event);
  if (!expandable) {
    return;
  }
  const action = `${getExpandableState(expandable)} filter`;
  let label = expandable.querySelector('span.o-expandable_label');
  label = label ? label : expandable.querySelector('span[aria-hidden=true]');
  if (!label) {
    return;
  }
  label = label.textContent.trim();

  return sendEvent(action, label);
};

/**
 * handleFilterClick - Listen for filter clicks and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleFilterClick = (event) => {
  const checkbox = event.target;
  if (!checkbox.classList.contains('a-checkbox')) {
    return;
  }
  const action = checkbox.checked ? 'filter' : 'remove filter';
  const label = checkbox.getAttribute('aria-label');

  return sendEvent(action, label);
};

/**
 * handleClearFilterClick - Listen for clear filter clicks and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleClearFilterClick = (event) => {
  // Continue only if the X icon was clicked and not the parent button
  let target = event.target.tagName.toLowerCase();
  if (target !== 'svg' && target !== 'path') {
    return;
  }
  target = event.target.closest('.a-tag[data-js-hook=behavior_clear-filter]');

  if (!target) {
    return;
  }
  const action = 'remove filter';
  const label = target.textContent.trim();

  return sendEvent(action, label);
};

/**
 * getPaginator - Find the paginator the user clicked.
 *
 * @param {event} event - Click event
 * @returns {HTMLElement|null} The checkbox div or null if it's not a checkbox
 */
const getPaginator = (event) => {
  const el = event.target.closest('.a-btn') || event.target;
  if (el.classList.contains('a-btn')) {
    return el;
  }
  return null;
};

/**
 * handlePaginationClick - Listen for pagination clicks and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handlePaginationClick = (event) => {
  const paginator = getPaginator(event);
  if (!paginator) {
    return;
  }

  const isNextButton = paginator.classList.contains('m-pagination_btn-next');
  const isPrevButton = paginator.classList.contains('m-pagination_btn-prev');
  const isDisabled = paginator.classList.contains('a-btn__disabled');

  if (!paginator.href || isDisabled || (!isNextButton && !isPrevButton)) {
    return;
  }

  const action = isNextButton ? 'next page' : 'previous page';
  let label = paginator.href.match(/\?.*page=(\d+)/);
  if (!label) {
    return;
  }
  label = isNextButton
    ? parseInt(label[1], 10) - 1
    : parseInt(label[1], 10) + 1;
  return sendEvent(action, label);
};

/**
 * getClearBtn - Find the clear all filters button.
 *
 * @param {event} event - Click event
 * @returns {HTMLElement|null} The checkbox div or null if it's not a checkbox
 */
const getClearBtn = (event) => {
  const el = event.target.closest('.results_filters-clear') || event.target;
  if (el.classList.contains('results_filters-clear')) {
    return el;
  }
  return null;
};

/**
 * handleClearAllClick - Listen for clear all filters clicks and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleClearAllClick = (event) => {
  const clearBtn = getClearBtn(event);
  if (!clearBtn) {
    return;
  }
  const tagsWrapper = clearBtn.parentElement;
  const tags = tagsWrapper.querySelectorAll('.a-tag');
  if (!tags || tags.length === 0) {
    return;
  }
  const tagNames = [];
  for (let i = 0; i < tags.length; i++) {
    if (tagsWrapper.contains(tags[i])) {
      tagNames.push(tags[i].textContent.trim());
    }
  }
  if (tagNames.length === 0) {
    return;
  }
  const action = 'clear all filters';
  const label = tagNames.join('|');
  return sendEvent(action, label);
};

/**
 * handleFetchSearchResults - Listen for AJAX fetchSearchResults
 * and report to GA.
 *
 * @param {string} searchTerm - string.
 */
const handleFetchSearchResults = (searchTerm) => {
  if (searchTerm.length === 0) {
    return;
  }

  // Send the keywords that return 0 results to Analytics.
  const resultsCountBlock = document.querySelector(
    '#tdp-search-facets-and-results .results_count'
  );
  if (resultsCountBlock) {
    const resultsCount = resultsCountBlock.getAttribute('data-results-count');

    // Check if result count is 0
    if (resultsCount === '0') {
      const action = 'noSearchResults';
      const label = searchTerm.toLowerCase() + ':0';

      sendEvent(action, label);
    }
  }

  // Send the keyword to Analytics.
  const action = 'search';
  const label = searchTerm.toLowerCase();
  sendEvent(action, label);
};

/**
 * handleSurveySwitchGradeClick - Listen for Switch grades click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveySwitchGradeClick = (event) => {
  const link = event.target.closest('.a-link__jump') || event.target;
  if (!link.classList.contains('a-link__jump')) {
    return;
  }
  const action = link.textContent.trim();
  const gradeLevel = link.getAttribute('data-tdp_grade_level');
  const label = 'Switch grades from ' + gradeLevel;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyPrivacyModalClick - Listen for Privacy statement click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyPrivacyModalClick = (event) => {
  const link =
    event.target.closest('[data-open-modal="modal-privacy"]') || event.target;
  if (link.getAttribute('data-open-modal') !== 'modal-privacy') {
    return;
  }
  const action = link.textContent.trim();
  const gradeLevel = link.getAttribute('data-tdp_grade_level');
  const label = gradeLevel;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyLetsDoThisClick - Listen for Let's do this click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyLetsDoThisClick = (event) => {
  const link = event.target.closest('a.survey-entry-link') || event.target;
  if (!link.classList.contains('survey-entry-link')) {
    return;
  }
  const action = link.textContent.trim();
  const gradeLevel = link.getAttribute('data-tdp_grade_level');
  const label = gradeLevel;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyChoiceChange - Listen for radio button value change and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyChoiceChange = (event) => {
  const radio = event.target.closest('input.tdp-survey__choice-question');
  if (!radio || !radio.checked) {
    return;
  }
  const action = 'Radio Button Clicked';
  const wrapper = radio.closest('div.wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const parentFieldset = radio.closest('fieldset');
  const question = parentFieldset.querySelector('legend.tdp-question-legend');
  const answer = radio.parentElement.querySelector('label');
  const label =
    gradeLevel +
    ': ' +
    question.textContent.trim() +
    ' (' +
    answer.textContent.trim() +
    ')';
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyErrorNoticeClick - Listen for error notification click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyErrorNoticeClick = (event) => {
  const link =
    event.target.closest('.m-notification__error a') || event.target;
  if (link.getAttribute('href') !== '#') {
    return;
  }
  const action = 'Anchor: Missed Question';
  const wrapper = link.closest('div.wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const section =
    Number(
      wrapper.querySelector('div[data-page-idx]').getAttribute('data-page-idx')
    ) + 1;
  const question = link.textContent.trim();
  const label = gradeLevel + ': Section ' + section + ' | ' + question;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyRestartModalClick - Listen for Restart survey click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyRestartModalClick = (event) => {
  const selector =
    '[data-open-modal="modal-restart"],[data-open-modal="modal-reset"]';
  const link = event.target.closest(selector);
  let label = '';
  if (link && link.getAttribute('data-open-modal') === 'modal-restart') {
    const wrapper = link.closest('div.wrapper.tdp-survey');
    const section =
      Number(
        wrapper
          .querySelector('div[data-page-idx]')
          .getAttribute('data-page-idx')
      ) + 1;
    const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
    label = gradeLevel + ': Section ' + section;
  } else if (link && link.getAttribute('data-open-modal') === 'modal-reset') {
    const wrapper = link.closest('div.content_wrapper.tdp-survey');
    const section = 'Results page';
    const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
    label = gradeLevel + ': ' + section;
  } else {
    return;
  }
  const action = 'Start Over';
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyExpandableClick - Listen for opening or closing of an expandable and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyExpandableClick = (event) => {
  const selector = '.tdp-survey-sidebar__mobile-control .o-expandable_header';
  const expandable = event.target.closest(selector);
  if (!expandable || !expandable.classList.contains('o-expandable_header')) {
    return;
  }
  const state =
    getExpandableState(expandable) === 'expand' ? 'Expand' : 'Collapse';
  const action = `Survey Progress Dropdown: ${state}`;
  const wrapper = expandable.closest('div.wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const section =
    Number(
      wrapper.querySelector('div[data-page-idx]').getAttribute('data-page-idx')
    ) + 1;
  const label = gradeLevel + ': Section ' + section;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveySectionClick - Listen for Edit Section click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveySectionClick = (event) => {
  const link = event.target.closest('[data-editable="1"]') || event.target;
  if (
    !link.classList.contains('tdp-survey-section') ||
    link.getAttribute('data-editable') !== '1'
  ) {
    return;
  }
  const action = 'Edit';
  const wrapper = link.closest('div.wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const section = link
    .querySelector('.tdp-survey-section__title')
    .textContent.replace('(complete)', '')
    .trim();
  const label = gradeLevel + ': ' + section;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveySubmitClick - Listen for Submit click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveySubmitClick = (event) => {
  const link =
    event.target.closest('button.a-btn[type="submit"]') || event.target;
  const action = link.textContent.trim();
  if (
    !link.classList.contains('a-btn') ||
    link.getAttribute('type') !== 'submit' ||
    action !== 'Get my results'
  ) {
    return;
  }
  const wrapper = link.closest('div.wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const section =
    Number(
      wrapper.querySelector('div[data-page-idx]').getAttribute('data-page-idx')
    ) + 1;
  const label = gradeLevel + ': Section ' + section;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyResultsExpandableClick - Listen for opening or closing of an expandable and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyResultsExpandableClick = (event) => {
  const selector = '.tdp-survey-results .o-expandable_target';
  const expandable = event.target.closest(selector);
  if (!expandable || !expandable.classList.contains('o-expandable_target')) {
    return;
  }
  const state =
    getExpandableState(expandable) === 'expand' ? 'Expand' : 'Collapse';
  const wrapper = expandable.closest('div.content_wrapper.tdp-survey');
  const pageType = wrapper.closest('.tdp-survey-results--shared')
    ? 'View'
    : 'Results';
  const action = `${pageType} Dropdown: ${state}`;
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const text = expandable
    .querySelector('.o-expandable_label')
    .textContent.trim();
  const label = gradeLevel + ': ' + text;

  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyDownloadClick - Listen for Download link click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyDownloadClick = (event) => {
  const link = event.target.closest('.a-link__icon') || event.target;
  if (!link.classList.contains('a-link__icon')) {
    return;
  }
  const action = 'Download';
  const label = link.getAttribute('href');
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyResultsModalClick - Listen for Results page Modal click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyResultsModalClick = (event) => {
  const selector =
    '[data-open-modal="modal-print"],[data-open-modal="modal-share-url"]';
  const link = event.target.closest(selector);
  if (!link || !link.getAttribute('data-open-modal')) {
    return;
  }
  const modalId = link.getAttribute('data-open-modal');
  const action = modalId === 'modal-print' ? 'Results Print' : 'Results Share';
  const wrapper = link.closest('div.content_wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const label = gradeLevel;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyResultsModalClose -
 * Listen for Results page Modal click and report to GA.
 *
 * @param {HTMLElement} modal - element
 * @returns {object} Event data
 */
const handleSurveyResultsModalClose = (modal) => {
  const modalId = modal.getAttribute('id');
  const wrapper = modal.closest('div.content_wrapper.tdp-survey');
  const valid_ids = ['modal-print', 'modal-share-url'];
  if (!valid_ids.includes(modalId) || !wrapper) {
    return;
  }
  const action = modalId === 'modal-print' ? 'Print: Close' : 'Share: Close';

  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const label = gradeLevel;

  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyResultsSavePdfClick - Listen for save as PDF click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyResultsSavePdfClick = (event) => {
  const selector = 'a.a-btn[href="/consumer-tools/save-as-pdf-instructions/"]';
  const link = event.target.closest(selector);
  if (!link) {
    return;
  }
  const wrapper = link.closest('div.content_wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const pageType = wrapper.querySelector('.tdp-survey-results--shared')
    ? 'View'
    : 'Results';
  const action = `${pageType} Save PDF`;
  const label = gradeLevel;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyResultsGetLinkClick - Listen for Results page Modal Get link click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyResultsGetLinkClick = (event) => {
  const link = event.target.closest(
    '#modal-share-url .tdp-survey__initials-set'
  );

  if (!link || !link.classList.contains('a-btn')) {
    return;
  }
  const textField = document.querySelector(
    '#modal-share-url input#modal-share-url-initials-input'
  );
  const action = 'Share: Get Link';
  const wrapper = link.closest('div.content_wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const initials = textField.value ? 'With initials' : 'No initials';
  const label = gradeLevel + ': ' + initials;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyResultsGetLinkClick - Listen for Results page Modal Copy link click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyResultsCopyLinkClick = (event) => {
  const link = event.target.closest(
    '#modal-share-url .share-output a, #modal-share-url .share-output button.a-btn'
  );
  if (!link) {
    return;
  }

  const action = 'Share: Copy Link';
  const wrapper = link.closest('div.content_wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const label = gradeLevel;
  return sendSurveyEvent(action, label);
};

/**
 * handleSurveyResultsPrintClick - Listen for Results page Modal Print click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyResultsPrintClick = (event) => {
  const link = event.target.closest('#modal-print .tdp-survey__initials-set');

  if (!link || !link.classList.contains('a-btn')) {
    return;
  }
  const textField = document.querySelector(
    '#modal-print input#modal-print-initials-input'
  );
  const action = 'Print: Get Link';
  const wrapper = link.closest('div.content_wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const initials = textField.value ? 'With initials' : 'No initials';
  const label = gradeLevel + ': ' + initials;
  return sendSurveyEvent(action, label);
};

/**
 * surveyResultsPageLoad - Report to GA on survey results page load.
 */
const surveyResultsPageLoad = () => {
  const el = document.querySelector('[data-tdp-page="results"]');
  if (!el || !sessionStorage.getItem(SCORES_UNSET_KEY)) {
    return;
  }

  const score = Number(el.dataset.score);
  const subtotals = JSON.parse(el.dataset.subtotals);

  const wrapper = el.closest('div.content_wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');

  const queue = subtotals.map((total, idx) => [
    `Results: ${gradeLevel}`,
    `Part ${idx + 1} total: ${total}`,
  ]);
  queue.push([`Results: ${gradeLevel}`, `Overall score: ${score}`]);

  queue.forEach((args) => sendSurveyEvent(args[0], args[1]));

  sessionStorage.removeItem(SCORES_UNSET_KEY);
};

/**
 * handleSurveyViewPrintClick - Listen for Results page Modal Print click and report to GA.
 *
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleSurveyViewPrintClick = (event) => {
  const link = event.target.closest(
    '.tdp-survey-results--shared button[onclick="window.print()"]'
  );

  if (!link || !link.classList.contains('a-btn')) {
    return;
  }

  const action = 'View Print';
  const wrapper = link.closest('div.content_wrapper.tdp-survey');
  const gradeLevel = wrapper.getAttribute('data-tdp_grade_level');
  const label = gradeLevel;
  return sendSurveyEvent(action, label);
};

/**
 * bindAnalytics - Set up analytics reporting.
 *
 * @param {Function} spyMethod - optional spy method.
 */
const bindAnalytics = (spyMethod) => {
  if (spyMethod) {
    sendEvent = spyMethod;
    sendSurveyEvent = spyMethod;
  }

  const searchContent = document.querySelector(
    '#tdp-search-facets-and-results'
  );
  if (searchContent) {
    searchContent.addEventListener('click', (event) => {
      handleExpandableClick(event);
      handleFilterClick(event);
      handleClearFilterClick(event);
      handlePaginationClick(event);
    });
  }
  // Survey section event listeners.
  const surveyContent = document.querySelector('.tdp-survey');
  if (surveyContent) {
    surveyContent.addEventListener('click', (event) => {
      handleSurveySwitchGradeClick(event);
      handleSurveyPrivacyModalClick(event);
      handleSurveyLetsDoThisClick(event);
      handleSurveyErrorNoticeClick(event);
      handleSurveyRestartModalClick(event);
      handleSurveyExpandableClick(event);
      handleSurveySectionClick(event);
      handleSurveySubmitClick(event);
      handleSurveyResultsExpandableClick(event);
      handleSurveyDownloadClick(event);
      handleSurveyResultsModalClick(event);
      handleSurveyResultsSavePdfClick(event);
      handleSurveyResultsGetLinkClick(event);
      handleSurveyResultsCopyLinkClick(event);
      handleSurveyResultsPrintClick(event);
      handleSurveyViewPrintClick(event);
    });

    surveyContent.addEventListener('change', (event) => {
      handleSurveyChoiceChange(event);
    });

    surveyResultsPageLoad();
  }
};

export {
  handleClearAllClick,
  handleFetchSearchResults,
  handleSurveyResultsModalClose,
  bindAnalytics,
};
