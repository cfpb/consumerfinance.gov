import Cookies from 'js-cookie';
import { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } from './config.js';
import { init as modalsInit } from '../modals.js';

/**
 * Initialize a grade-level intro page
 */
function gradeLevelPage() {
  // Clear session to prepare for fresh entry
  Cookies.remove(RESULT_COOKIE);
  Cookies.remove(SURVEY_COOKIE);
  sessionStorage.removeItem(ANSWERS_SESS_KEY);

  modalsInit();
}

export { gradeLevelPage };
