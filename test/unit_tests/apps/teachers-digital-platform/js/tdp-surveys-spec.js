import { jest } from '@jest/globals';
import surveys from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys.js';
import * as gradeLevelModule from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/grade-level-page.js';
import * as resultsModule from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/result-page.js';
import * as surveyModule from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/survey-page.js';

let glp;
let rp;
let sp;

xdescribe('The TDP survey router', () => {
  beforeEach(() => {
    glp = jest
      .spyOn(gradeLevelModule, 'gradeLevelPage')
      .mockImplementation(() => 1);
    rp = jest.spyOn(resultsModule, 'resultsPage').mockImplementation(() => 1);
    sp = jest.spyOn(surveyModule, 'surveyPage').mockImplementation(() => 1);
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('recognizes grade level page', () => {
    document.body.innerHTML = '<div data-tdp-page="grade-level"></div>';
    surveys.init();
    expect(glp).toHaveBeenCalled();
    expect(sp).not.toHaveBeenCalled();
    expect(rp).not.toHaveBeenCalled();
  });

  it('recognizes survey page', () => {
    document.body.innerHTML = '<div data-tdp-page="survey"></div>';
    surveys.init();
    expect(glp).not.toHaveBeenCalled();
    expect(sp).toHaveBeenCalled();
    expect(rp).not.toHaveBeenCalled();
  });

  it('recognizes results page', () => {
    document.body.innerHTML = '<div data-tdp-page="results"></div>';
    surveys.init();
    expect(glp).not.toHaveBeenCalled();
    expect(sp).not.toHaveBeenCalled();
    expect(rp).toHaveBeenCalled();
  });
});
