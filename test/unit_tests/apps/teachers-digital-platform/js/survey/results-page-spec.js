import surveys from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys';
import { Cookie } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/result-page';
import { ANSWERS_SESS_KEY, SURVEY_COOKIE } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';
import * as initials from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/initials';
import HTML_SNIPPET from '../../html/results-page';

describe( 'The TDP survey results page', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'should be recognized from HTML', () => {
    const cookieSpy = jest.spyOn( Cookie, 'remove' );
    const modalSpy = jest.spyOn( modals, 'init' );
    const initialsSpy = jest.spyOn( initials, 'init' );
    sessionStorage.setItem( ANSWERS_SESS_KEY, 'testItem' );

    surveys.init();

    expect( modalSpy ).toHaveBeenCalled();
    expect( sessionStorage.getItem( ANSWERS_SESS_KEY ) ).toBeNull();
    expect( cookieSpy.mock.calls[0][0] ).toEqual( SURVEY_COOKIE );
    expect( initialsSpy ).toHaveBeenCalled();

    cookieSpy.mockRestore();
    modalSpy.mockRestore();
    initialsSpy.mockRestore();
  } );
} );
