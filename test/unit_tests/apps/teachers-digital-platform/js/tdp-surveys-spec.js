import { jest } from '@jest/globals';

const gl =
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/grade-level-page.js';
const res =
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/result-page.js';
const sur =
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/survey-page.js';

let surveys, g, r, s;

describe('The TDP survey router', () => {
  beforeAll(async () => {
    jest.unstable_mockModule(gl, () => ({
      gradeLevelPage: jest.fn(),
    }));

    jest.unstable_mockModule(res, () => ({
      resultsPage: jest.fn(),
    }));

    jest.unstable_mockModule(sur, () => ({
      surveyPage: jest.fn(),
    }));

    surveys = await import(
      '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys.js'
    );
    surveys = surveys.default;
    g = await import(gl);
    r = await import(res);
    s = await import(sur);
  });

  it('recognizes grade level page', () => {
    document.body.innerHTML = '<div data-tdp-page="grade-level"></div>';
    surveys.init();
    expect(g.gradeLevelPage).toHaveBeenCalled();
    expect(r.resultsPage).not.toHaveBeenCalled();
    expect(s.surveyPage).not.toHaveBeenCalled();
  });

  it('recognizes survey page', () => {
    document.body.innerHTML = '<div data-tdp-page="survey"></div>';
    surveys.init();
    expect(g.gradeLevelPage.mock.calls.length).toBe(1);
    expect(s.surveyPage.mock.calls.length).toBe(1);
    expect(r.resultsPage).not.toHaveBeenCalled();
  });

  it('recognizes results page', () => {
    document.body.innerHTML = '<div data-tdp-page="results"></div>';
    surveys.init();
    expect(g.gradeLevelPage.mock.calls.length).toBe(1);
    expect(s.surveyPage.mock.calls.length).toBe(1);
    expect(r.resultsPage.mock.calls.length).toBe(1);
  });
});
