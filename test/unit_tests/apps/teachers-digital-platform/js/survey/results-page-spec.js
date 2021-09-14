import surveys from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys';
import { Cookie, resultsPage } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/result-page';
import { ANSWERS_SESS_KEY, SURVEY_COOKIE } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';
import * as initials from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/initials';
import HTML_SNIPPET from '../../html/results-page';
import { encodeName } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/initials';
import clipboardCopy from 'copy-to-clipboard';

const $ = document.querySelector.bind( document );

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

  it( 'should read initials', () => {
    const spy = jest.spyOn( initials.encodeName, 'decodeNameFromUrl' )
      .mockImplementation( () => 'ACBDE' );

    resultsPage();

    expect( spy ).toHaveBeenCalled();
    expect( initials.get() ).toEqual( '' );

    spy.mockRestore();
  } );

  it( 'setting initials updates display', () => {
    resultsPage();
    window.print = () => 1;

    const input = $( '#modal-print_desc .tdp-survey__initials' );
    const set = $( '#modal-print_desc .tdp-survey__initials-set' );

    // Enter nothing
    set.click();
    expect( initials.get() ).toEqual( '' );

    // Emulate manual entry with event
    input.value = 'cd5ef';
    input.dispatchEvent( new Event( 'input') );
    set.click();

    expect( initials.get() ).toEqual( 'CD5E' );
  } );

  it( 'can reset/cancel by modal', () => {
    const modalsCloseSpy = jest.spyOn( modals, 'close' );
    resultsPage();
    const origLocation = location;
    delete window.location;
    window.location = {};

    $( '#modal-reset [data-cancel="1"]' ).click();

    expect( modalsCloseSpy ).toHaveBeenCalled();

    $( '#modal-reset [data-cancel=""]' ).click();

    expect( location.href ).toEqual( '../../assess/survey/' );

    window.location = origLocation;
  } );

  it( 'can share by modal', () => {
    resultsPage();

    const input = $( '#modal-share-url_desc .tdp-survey__initials' );
    const set = $( '#modal-share-url_desc .tdp-survey__initials-set' );

    input.value = 'defg';
    input.dispatchEvent( new Event( 'input' ) );

    const shared = $( '.share-output a[href]' );
    set.click();

    expect( initials.get() ).toEqual( 'DEFG' );
    expect( encodeName.decodeNameFromUrl( shared.href ) ).toEqual( 'DEFG' );

    input.value = 'EFGH';
    input.dispatchEvent( new KeyboardEvent( 'keyup', {
      key: 'Enter',
    } ) );

    expect( initials.get() ).toEqual( 'EFGH' );

    shared.click();

    expect( clipboardCopy ).toHaveBeenCalled();
    expect( $( '.share-output__copied' ).hidden ).toBeFalsy();
  } );

  it( 'share model open resets its contents', () => {
    resultsPage();

    $( '.tdp-survey__initials-error' ).classList.add( 'm-notification__visible' );
    $( '.share-output' ).hidden = false;
    $( '.share-output__copied' ).hidden = false;

    $( '[data-open-modal="modal-share-url"]' ).click();

    expect( $( '.tdp-survey__initials-error' ).classList.contains( 'm-notification__visible' ) )
      .toBeFalsy();
    expect( $( '.share-output' ).hidden ).toBeTruthy();
    expect(  $( '.share-output__copied' ).hidden ).toBeTruthy();
  } );
} );
