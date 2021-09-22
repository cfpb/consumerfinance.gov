import surveys from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys';
import {
  Cookie,
  ChoiceField,
  scrollToEl,
  surveyPage,
  progressBar
} from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/survey-page';
import { ANSWERS_SESS_KEY, RESULT_COOKIE } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';
import HTML_SNIPPET from '../../html/survey-page';

const $ = document.querySelector.bind( document );

describe( 'The TDP survey page', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  it( 'should be recognized from HTML', () => {
    const modalSpy = jest.spyOn( modals, 'init' );
    const cf1Spy = jest.spyOn( ChoiceField, 'init' );
    const cf2Spy = jest.spyOn( ChoiceField, 'watchAndStore' );
    const cf3Spy = jest.spyOn( ChoiceField, 'restoreFromSession' );
    ChoiceField.cache = Object.create( null );
    sessionStorage.clear();
    expect( progressBar ).toBeUndefined();

    surveys.init();

    const answers = JSON.parse( sessionStorage.getItem( ANSWERS_SESS_KEY ) );
    expect( answers ).toEqual( { 'p1-q6': '3' } );
    expect( modalSpy ).toHaveBeenCalled();
    expect( cf1Spy ).toHaveBeenCalled();
    expect( cf2Spy ).toHaveBeenCalled();
    expect( cf3Spy ).toHaveBeenCalled();
    expect( progressBar.totalNum ).toEqual( 20 );

    modalSpy.mockRestore();
  } );

  it( 'should update progress', () => {
    ChoiceField.cache = Object.create( null );
    sessionStorage.clear();
    surveyPage();
    const label = $( 'label[for="id_p1-q1_0"]' );
    label.click();

    const answers = JSON.parse( sessionStorage.getItem( ANSWERS_SESS_KEY ) );
    expect( answers ).toEqual( { 'p1-q1': '0', 'p1-q6': '3' } );
    expect( progressBar.numDone ).toEqual( 2 );
    expect( ChoiceField.get( 'p1-q1' ) ).toBeInstanceOf( ChoiceField );
    expect( ChoiceField.get( 'p1-q1' ).value ).toEqual( '0' );
  } );

  it( 'should catch missing answers', () => {
    const clickNext = () => $( '.tdp-survey-page button[type="submit"]' ).click();

    ChoiceField.cache = Object.create( null );
    sessionStorage.clear();
    surveyPage();
    clickNext();

    expect( $( 'form > .m-notification__visible' ) ).not.toBeUndefined();

    // Missed first question
    let legend = $( 'legend + .a-form-alert' ).previousElementSibling;
    expect( legend.textContent ).toMatch( '1.' );
    const scrollLink = $( '.m-notification_explanation a' );
    expect( scrollLink.textContent ).toEqual( legend.textContent );

    scrollLink.click();

    $( 'label[for="id_p1-q1_0"]' ).click();

    clickNext();

    // Missed second
    legend = $( 'legend + .a-form-alert' ).previousElementSibling;
    expect( legend.textContent ).toMatch( '2.' );

    [ 1, 2, 3, 4, 5, 6 ].forEach( num => {
      $( `label[for="id_p1-q${ num }_0"]` ).click();
    } );

    const form = $( '.tdp-survey-page form' );
    let returnValue = false;
    form.addEventListener( 'submit', event => {
      returnValue = event.returnValue;
      event.preventDefault();
    } );

    clickNext();

    expect( returnValue ).toBeTruthy();
  } );

  it( 'should set buttons from storage', () => {
    ChoiceField.cache = Object.create( null );
    sessionStorage.clear();
    sessionStorage.setItem( ANSWERS_SESS_KEY, JSON.stringify(
      { 'p1-q1': '0', 'p1-q6': '3' }
    ) );

    surveyPage();

    const input = $( 'input[name="p1-q6"][value="3"]' );
    expect( input.checked ).toBeTruthy();
  } );

  it( 'allows starting over', () => {
    const origLocation = location;
    delete window.location;
    window.location = {};
    const closeSpy = jest.spyOn( modals, 'close' );
    $( '#modal-restart [data-cancel="1"]' ).click();

    expect( closeSpy ).toHaveBeenCalled();

    $( '#modal-restart [data-cancel=""]' ).click();

    expect( location.href ).toEqual( '../../../assess/survey/' );

    window.location = origLocation;
  } );

  it( 'decorates question layouts', () => {
    surveyPage();

    expect( $( '#id_p1-q3 .tdp-lines li:nth-child(3)' ) ).toBeTruthy();
  } );

  it( 'redirects if skipped ahead', () => {
    const origLocation = location;
    delete window.location;
    window.location = {};

    $( '[data-page-idx]' ).setAttribute( 'data-page-idx', '3' );
    surveyPage();

    expect( location.href ).toEqual( '../p1/' );

    window.location = origLocation;
  } );

  it( 'redirects if has results cookie', () => {
    const origLocation = location;
    delete window.location;
    window.location = {};
    Cookie.set( RESULT_COOKIE, 'any truthy value' );

    surveyPage();

    expect( location.href ).toEqual( '../results/' );

    window.location = origLocation;
  } );

  it( 'scrollToEl tries fallbacks', () => {
    const el = $( 'h1' );
    el.scrollIntoView = jest.fn();

    expect( scrollToEl( el ) ).toBe( true );

    expect( el.scrollIntoView.mock.calls[0][0] )
      .toEqual( { behavior: 'smooth' } );

    el.scrollIntoView.mockImplementation( arg => {
      if ( typeof arg === 'object' ) {
        throw new Error( 'No' );
      }
    } );

    expect( scrollToEl( el ) ).toBe( true );

    expect( el.scrollIntoView.mock.calls[1][0] )
      .toEqual( { behavior: 'smooth' } );
    expect( el.scrollIntoView.mock.calls[2] ).toEqual( [] );

    el.scrollIntoView.mockImplementation( () => {
      throw new Error( 'Nada' );
    } );

    expect( scrollToEl( el ) ).toBe( false );
  } );
} );
