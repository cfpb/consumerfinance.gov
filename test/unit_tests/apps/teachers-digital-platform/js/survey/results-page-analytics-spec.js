import surveys from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/tdp-surveys';
import { Cookie } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/grade-level-page';
import { ANSWERS_SESS_KEY, RESULT_COOKIE, SURVEY_COOKIE } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';

import { simulateEvent } from '../../../../../util/simulate-event.js';
const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/';
const tdpAnalytics = require(
  BASE_JS_PATH + 'teachers-digital-platform/js/tdp-analytics.js'
);
import HTML_SNIPPET from '../../html/results-page-analytics';

const xhr = global.XMLHttpRequest;

describe( 'Custom analytics for the TDP survey results page', () => {
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

  it( 'should send analytics event when an expandable is clicked', () => {
    const target = document.querySelector( '.tdp-survey-results .o-expandable_target' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Results Dropdown: Collapse' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12: Planning and self-control' );
    expect( spy ).toHaveBeenCalled();

  } );

  it( 'should send analytics event when an download link is clicked', () => {
    const target = document.querySelector( '.a-link__icon' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Download' );
    expect( spy.mock.calls[0][1] ).toEqual( 'https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_high-school-assessment-student-worksheet.pdf' );
    expect( spy ).toHaveBeenCalled();

  } );

  it( 'should send analytics event when the print link is clicked', () => {
    const target = document.querySelector( '[data-open-modal="modal-print"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Results Print' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12' );
    expect( spy ).toHaveBeenCalled();

  } );

  it( 'should send analytics event when the share link is clicked', () => {
    const target = document.querySelector( '[data-open-modal="modal-share-url"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Results Share' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12' );
    expect( spy ).toHaveBeenCalled();

  } );

  it( 'should send analytics event when the pdf how to link is clicked', () => {
    const target = document.querySelector( 'a.a-btn[href="/consumer-tools/save-as-pdf-instructions/"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Results Save PDF' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12' );
    expect( spy ).toHaveBeenCalled();

  } );

  it( 'should send analytics event when the get link button is clicked', () => {
    const target = document.querySelector( '#modal-share-url .tdp-survey__initials-set' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Share: Get Link' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12: No initials' );
    expect( spy ).toHaveBeenCalled();

  } );

  it( 'should send analytics event when the print button is clicked', () => {
    const target = document.querySelector( '#modal-print .tdp-survey__initials-set' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Print: Get Link' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12: No initials' );
    expect( spy ).toHaveBeenCalled();

  } );

} );
