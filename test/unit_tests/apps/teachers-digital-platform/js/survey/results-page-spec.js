import { jest } from '@jest/globals';
import {
  ANSWERS_SESS_KEY,
  SURVEY_COOKIE,
} from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config.js';
import HTML_SNIPPET from '../../html/results-page.js';

const $ = document.querySelector.bind(document);

describe('The TDP survey results page', () => {
  let initials, surveys, resultsPage, obfuscation;
  const remove = jest.fn();
  const init = jest.fn();
  const close = jest.fn();
  const copy = jest.fn();

  beforeAll(async () => {
    jest.unstable_mockModule('js-cookie', () => ({
      default: {
        remove,
      },
    }));

    jest.unstable_mockModule('copy-to-clipboard', () => ({
      default: copy,
    }));

    jest.unstable_mockModule(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals.js',
      () => ({
        init,
        close,
      })
    );

    surveys = (
      await import(
        '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys.js'
      )
    ).default;

    resultsPage = (
      await import(
        '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/result-page.js'
      )
    ).resultsPage;

    initials = await import(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/initials.js'
    );

    obfuscation = await import(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/obfuscation.js'
    );
  });

  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
  });

  it('should be recognized from HTML', () => {
    sessionStorage.setItem(ANSWERS_SESS_KEY, 'testItem');

    surveys.init();

    expect(sessionStorage.getItem(ANSWERS_SESS_KEY)).toBeNull();
    expect(remove.mock.calls[0][0]).toEqual(SURVEY_COOKIE);
    expect(init).toHaveBeenCalled();
  });

  it('should read initials', () => {
    expect(initials.get()).toEqual('');
  });

  it('setting initials updates display', () => {
    resultsPage();
    window.print = () => 1;

    const input = $('#modal-print_desc .tdp-survey__initials');
    const set = $('#modal-print_desc .tdp-survey__initials-set');

    // Enter nothing
    set.click();
    expect(initials.get()).toEqual('');

    // Emulate manual entry with event
    input.value = 'cd5ef';
    input.dispatchEvent(new Event('input'));
    set.click();

    expect(initials.get()).toEqual('CD5E');
  });

  it('can reset/cancel by modal', () => {
    resultsPage();
    const origLocation = location;
    delete window.location;
    window.location = {};

    $('#modal-reset [data-cancel="1"]').click();

    expect(close).toHaveBeenCalled();

    $('#modal-reset [data-cancel=""]').click();

    expect(location.href).toEqual('../../assess/survey/');

    window.location = origLocation;
  });

  it('can share by modal', () => {
    resultsPage();

    const input = $('#modal-share-url_desc .tdp-survey__initials');
    const set = $('#modal-share-url_desc .tdp-survey__initials-set');

    input.value = 'defg';
    input.dispatchEvent(new Event('input'));

    const shared = $('.share-output a[href]');
    set.click();

    expect(initials.get()).toEqual('DEFG');
    expect(obfuscation.decodeNameFromUrl(shared.href)).toEqual('DEFG');

    input.value = 'EFGH';
    input.dispatchEvent(
      new KeyboardEvent('keyup', {
        key: 'Enter',
      })
    );

    expect(initials.get()).toEqual('EFGH');

    shared.click();

    expect(copy).toHaveBeenCalled();
    expect($('.share-output__copied').hidden).toBeFalsy();
  });
});
