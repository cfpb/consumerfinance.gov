import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';
import { SCORES_UNSET_KEY } from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/survey/config';
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
  } );

  it( 'should send analytics event when an download link is clicked', () => {
    const target = document.querySelector( '.a-link__icon' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Download' );
    expect( spy.mock.calls[0][1] ).toEqual( 'https://files.consumerfinance.gov/f/documents/cfpb_building_block_activities_high-school-assessment-student-worksheet.pdf' );
  } );

  it( 'should send analytics event when the print link is clicked', () => {
    const target = document.querySelector( '[data-open-modal="modal-print"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Results Print' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12' );
  } );

  it( 'should send analytics events when the share link is clicked and modal closed', () => {
    modals.init();

    const target = document.querySelector( '[data-open-modal="modal-share-url"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Results Share' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12' );

    modals.close();

    expect( spy.mock.calls[1][0] ).toEqual( 'Share: Close' );
    expect( spy.mock.calls[1][1] ).toEqual( '9-12' );
  } );

  it( 'should send analytics event when the pdf how to link is clicked', () => {
    const target = document.querySelector( 'a.a-btn[href="/consumer-tools/save-as-pdf-instructions/"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Results Save PDF' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12' );
  } );

  it( 'should send analytics events when the shared link is generated and copied', () => {
    let target = document.querySelector( '#modal-share-url .tdp-survey__initials-set' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );
    expect( spy.mock.calls[0][0] ).toEqual( 'Share: Get Link' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12: No initials' );

    target = document.querySelector( '#modal-share-url .share-output button.a-btn' );
    simulateEvent( 'click', target );

    expect( spy.mock.calls[1][0] ).toEqual( 'Share: Copy Link' );
    expect( spy.mock.calls[1][1] ).toEqual( '9-12' );
  } );

  it( 'should send analytics event when the print button is clicked', () => {
    const target = document.querySelector( '#modal-print .tdp-survey__initials-set' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Print: Get Link' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12: No initials' );
  } );

  it( 'should send analytics event when the reset modal is opened', () => {
    modals.init();
    const target = document.querySelector( '[data-open-modal="modal-reset"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Start Over' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12: Results page' );
  } );

  it( 'should send analytics event when loading the results page', () => {
    sessionStorage.removeItem( SCORES_UNSET_KEY );

    let spy = jest.fn();
    tdpAnalytics.bindAnalytics( spy );

    expect( spy.mock.calls.length ).toEqual( 0 );

    sessionStorage.setItem( SCORES_UNSET_KEY, '1' );

    spy = jest.fn();
    tdpAnalytics.bindAnalytics( spy );

    expect( spy.mock.calls.length ).toEqual( 4 );
    expect( spy.mock.calls[0][0] ).toEqual( 'Results: 9-12' );
    expect( spy.mock.calls[1][0] ).toEqual( 'Results: 9-12' );
    expect( spy.mock.calls[2][0] ).toEqual( 'Results: 9-12' );
    expect( spy.mock.calls[3][0] ).toEqual( 'Results: 9-12' );
    expect( spy.mock.calls[0][1] ).toEqual( 'Part 1 total: 25' );
    expect( spy.mock.calls[1][1] ).toEqual( 'Part 2 total: 35' );
    expect( spy.mock.calls[2][1] ).toEqual( 'Part 3 total: 45' );
    expect( spy.mock.calls[3][1] ).toEqual( 'Overall score: 90' );

    expect( sessionStorage.getItem( SCORES_UNSET_KEY ) ).toEqual( null );
  } );

} );
