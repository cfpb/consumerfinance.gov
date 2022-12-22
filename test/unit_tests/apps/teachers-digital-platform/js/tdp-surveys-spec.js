import { jest } from '@jest/globals';

const gl =
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/grade-level-page.js';
const res =
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/result-page.js';
const sur =
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/survey-page.js';

let surveys, gradeLevelPage, resultsPage, surveyPage;

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
    gradeLevelPage = (await import(gl)).gradeLevelPage;
    resultsPage = (await import(res)).resultsPage;
    surveyPage = (await import(sur)).surveyPage;
  });

  it('recognizes grade level page', () => {
    document.body.innerHTML = '<div data-tdp-page="grade-level"></div>';
    surveys.init();
    expect(gradeLevelPage).toHaveBeenCalled();
    expect(resultsPage).not.toHaveBeenCalled();
    expect(surveyPage).not.toHaveBeenCalled();
  });

  it('recognizes survey page', () => {
    document.body.innerHTML = '<div data-tdp-page="survey"></div>';
    surveys.init();
    expect(gradeLevelPage.mock.calls.length).toBe(1);
    expect(surveyPage.mock.calls.length).toBe(1);
    expect(resultsPage).not.toHaveBeenCalled();
  });

  it('recognizes results page', () => {
    document.body.innerHTML = '<div data-tdp-page="results"></div>';
    surveys.init();
    expect(gradeLevelPage.mock.calls.length).toBe(1);
    expect(surveyPage.mock.calls.length).toBe(1);
    expect(resultsPage.mock.calls.length).toBe(1);
  });
});
