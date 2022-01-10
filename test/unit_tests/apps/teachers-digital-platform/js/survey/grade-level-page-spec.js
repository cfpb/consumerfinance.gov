import surveys from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys';
import { Cookie } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/grade-level-page';
import { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';

const HTML_SNIPPET = `
<div data-tdp-page="grade-level">
</div>
`;

describe( 'The TDP survey grade-level page', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'should be recognized from HTML', () => {
    const cookieSpy = jest.spyOn( Cookie, 'remove' );
    const modalSpy = jest.spyOn( modals, 'init' );
    sessionStorage.setItem( ANSWERS_SESS_KEY, 'testItem' );

    surveys.init();

    expect( cookieSpy.mock.calls[0][0] ).toEqual( RESULT_COOKIE );
    expect( cookieSpy.mock.calls[1][0] ).toEqual( SURVEY_COOKIE );
    expect( sessionStorage.getItem( ANSWERS_SESS_KEY ) ).toBeNull();
    expect( modalSpy ).toHaveBeenCalled();

    cookieSpy.mockRestore();
    modalSpy.mockRestore();
  } );
} );
