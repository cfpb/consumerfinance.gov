import { simulateEvent } from '../../../../../util/simulate-event.js';
const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/';
const tdpAnalytics = require(
  BASE_JS_PATH + 'teachers-digital-platform/js/tdp-analytics.js'
);
import HTML_SNIPPET from '../../html/shared-results-page-analytics';

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

    expect( spy.mock.calls[0][0] ).toEqual( 'View Dropdown: Expand' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12: Planning and self-control' );
    expect( spy ).toHaveBeenCalled();

  } );

  it( 'should send analytics event when the print button is clicked', () => {
    const target = document.querySelector( '.tdp-survey-results--shared button[onclick="window.print()"]' );
    const spy = jest.fn();
    window.print = () => true;

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'View Print' );
    expect( spy.mock.calls[0][1] ).toEqual( '9-12' );
    expect( spy ).toHaveBeenCalled();

  } );

} );
