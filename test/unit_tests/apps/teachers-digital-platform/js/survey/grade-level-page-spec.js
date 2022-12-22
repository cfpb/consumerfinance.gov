import { jest } from '@jest/globals';
import {
  ANSWERS_SESS_KEY,
  RESULT_COOKIE,
  SURVEY_COOKIE,
} from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config.js';

const HTML_SNIPPET = `
<div data-tdp-page="grade-level">
</div>
`;

describe('The TDP survey grade-level page', () => {
  let surveys;
  const remove = jest.fn();
  const init = jest.fn();

  beforeAll(async () => {
    jest.unstable_mockModule('js-cookie', () => ({
      default: {
        remove,
      },
    }));

    jest.unstable_mockModule(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals.js',
      () => ({
        init,
        close: jest.fn(),
      })
    );

    surveys = await import(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys.js'
    );

    document.body.innerHTML = HTML_SNIPPET;
  });

  it('should be recognized from HTML', () => {
    sessionStorage.setItem(ANSWERS_SESS_KEY, 'testItem');

    surveys.default.init();

    expect(remove.mock.calls[0][0]).toEqual(RESULT_COOKIE);
    expect(remove.mock.calls[1][0]).toEqual(SURVEY_COOKIE);
    expect(sessionStorage.getItem(ANSWERS_SESS_KEY)).toBeNull();
    expect(init).toHaveBeenCalled();
  });
});
