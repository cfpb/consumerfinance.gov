import surveys from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys';
import { Cookie } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/grade-level-page';
import { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';

import { simulateEvent } from '../../../../../util/simulate-event.js';
const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/';
const tdpAnalytics = require(
  BASE_JS_PATH + 'teachers-digital-platform/js/tdp-analytics.js'
);
import HTML_SNIPPET from '../../html/survey-page-analytics';

const xhr = global.XMLHttpRequest;

describe( 'Custom analytics for the TDP survey form page', () => {
  beforeEach( () => {
    // Reset global XHR
    global.XMLHttpRequest = xhr;
    // Load HTML fixture
    document.body.innerHTML = HTML_SNIPPET;
    // Fire `load` event
    const event = document.createEvent( 'Event' );
    event.initEvent( 'load', true, true );
    window.dispatchEvent( event );

    const mockXHR = {
      open: jest.fn(),
      send: jest.fn(),
      readyState: 4,
      status: 200,
      onreadystatechange: jest.fn(),
      responseText: []
    };
    global.XMLHttpRequest = jest.fn( () => mockXHR );
  } );

  it( 'should send analytics event when a radio button is clicked', () => {
    const target = document.querySelector( 'input#id_p3-q10_0' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Radio Button Clicked' );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5: 10. Try not to spend all my money right away. (Very important)' );
    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should send analytics event when a radio button is clicked', () => {
    const target = document.querySelector( 'input#id_p3-q10_0' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Radio Button Clicked' );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5: 10. Try not to spend all my money right away. (Very important)' );
    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should send analytics event when error notification link is clicked', () => {
    const target = document.querySelector( '.m-notification__error a' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( "Anchor: Missed Question" );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5: Section 3 | 10. Try not to spend all my money right away.' );
    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should send analytics event when restart survey link is clicked', () => {
    const target = document.querySelector( '[data-open-modal="modal-restart"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( "Start Over" );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5: Section 3' );
    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should send analytics event when sidebar expandalbe link is clicked', () => {
    const target = document.querySelector( '.tdp-survey-sidebar__mobile-control .o-expandable_header' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( "Survey Progress Dropdown: Expand" );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5: Section 3' );
    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should send analytics event when sidebar section link is clicked', () => {
    const target = document.querySelector( '[data-editable="1"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( "Edit" );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5: Section 1' );
    expect( spy ).toHaveBeenCalled();
  } );

  it( 'should send analytics event when submit button is clicked', () => {
    document.body.innerHTML = `
      <div data-tdp_grade_level="3-5" class="wrapper content_wrapper tdp-survey tdp-survey-layout">
        <div class="tdp-survey-page content_main" data-tdp-page="survey" data-grade-select-url="/consumer-tools/educator-tools/youth-financial-education/assess/survey/" data-page-idx="4" data-questions-by-page="[6, 2, 7, 3, 2]" data-item-separator="&quot;\u2023&quot;">
          <button class="a-btn" type="submit">
              <span class="a-btn_text">Get my results</span>
              <span class="a-btn_icon a-btn_icon__on-right">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 19" class="cf-icon-svg">
                  <path d="M1.6 17.262a1.03 1.03 0 0 1-.728-1.757l6.073-6.073L.872 3.36a1.03 1.03 0 0 1 1.455-1.455l6.8 6.8a1.03 1.03 0 0 1 0 1.456l-6.8 6.8a1.025 1.025 0 0 1-.727.302z"></path>
                </svg>
              </span>
            </button>
        </div>
      </div>
    `

    const target = document.querySelector( 'button.a-btn[type="submit"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( "Get my results" );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5: Section 5' );
    expect( spy ).toHaveBeenCalled();
  } );

} );
