import { jest } from '@jest/globals';
import Cookies from 'js-cookie';
import {
  ANSWERS_SESS_KEY,
  RESULT_COOKIE,
  SCORES_UNSET_KEY,
} from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config.js';
import HTML_SNIPPET from '../../html/survey-page.js';

const $ = document.querySelector.bind(document);

describe('The TDP survey page', () => {
  const modalInit = jest.fn();
  const close = jest.fn();
  let scrollToEl, surveyPage, surveys;

  beforeAll(async () => {
    jest.unstable_mockModule(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals.js',
      () => ({
        init: modalInit,
        close,
      })
    );

    const surveyExports = await import(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/survey-page.js'
    );
    scrollToEl = surveyExports.scrollToEl;
    surveyPage = surveyExports.surveyPage;
    surveys = await import(
      '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys.js'
    );
  });

  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
  });

  it('should be recognized from HTML', () => {
    sessionStorage.clear();

    surveys.default.init();

    const answers = JSON.parse(sessionStorage.getItem(ANSWERS_SESS_KEY));
    expect(answers).toEqual({ 'p1-q6': '3' });
    expect(sessionStorage.getItem(SCORES_UNSET_KEY)).toEqual('1');
  });

  it('should update progress', () => {
    sessionStorage.clear();
    surveyPage();
    const label = $('label[for="id_p1-q1_0"]');
    label.click();

    const answers = JSON.parse(sessionStorage.getItem(ANSWERS_SESS_KEY));
    expect(answers).toEqual({ 'p1-q1': '0', 'p1-q6': '3' });
  });

  it('should set buttons from storage', () => {
    sessionStorage.clear();
    sessionStorage.setItem(
      ANSWERS_SESS_KEY,
      JSON.stringify({ 'p1-q1': '0', 'p1-q6': '3' })
    );

    surveyPage();

    const input = $('input[name="p1-q6"][value="3"]');
    expect(input.checked).toBeTruthy();
  });

  it('allows starting over', () => {
    const origLocation = location;
    delete window.location;
    window.location = {};
    const modal = $('#modal-restart [data-cancel="1"]');
    modal.click();
    expect(close).toHaveBeenCalled();

    $('#modal-restart [data-cancel=""]').click();

    expect(location.href).toEqual('../../../assess/survey/');

    window.location = origLocation;
  });

  it('decorates question layouts', () => {
    surveyPage();

    expect($('#id_p1-q3 .tdp-lines li:nth-child(3)')).toBeTruthy();
  });

  it('redirects if skipped ahead', () => {
    const origLocation = location;
    delete window.location;
    window.location = {};

    $('[data-page-idx]').setAttribute('data-page-idx', '3');
    surveyPage();

    expect(location.href).toEqual('../p1/');

    window.location = origLocation;
  });

  it('redirects if has results cookie', () => {
    const origLocation = location;
    delete window.location;
    window.location = {};
    Cookies.set(RESULT_COOKIE, 'any truthy value');

    surveyPage();

    expect(location.href).toEqual('../results/');

    window.location = origLocation;
  });

  it('scrollToEl tries fallbacks', () => {
    const el = $('h1');
    el.scrollIntoView = jest.fn();

    expect(scrollToEl(el)).toBe(true);

    expect(el.scrollIntoView.mock.calls[0][0]).toEqual({ behavior: 'smooth' });

    el.scrollIntoView.mockImplementation((arg) => {
      if (typeof arg === 'object') {
        throw new Error('No');
      }
    });

    expect(scrollToEl(el)).toBe(true);

    expect(el.scrollIntoView.mock.calls[1][0]).toEqual({ behavior: 'smooth' });
    expect(el.scrollIntoView.mock.calls[2]).toEqual([]);

    el.scrollIntoView.mockImplementation(() => {
      throw new Error('Nada');
    });

    expect(scrollToEl(el)).toBe(false);
  });
});
