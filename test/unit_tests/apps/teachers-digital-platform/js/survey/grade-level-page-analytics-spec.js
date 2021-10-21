import * as modals from '../../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';

import { simulateEvent } from '../../../../../util/simulate-event.js';
const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/';
const tdpAnalytics = require(
  BASE_JS_PATH + 'teachers-digital-platform/js/tdp-analytics.js'
);
import HTML_SNIPPET from '../../html/grade-level-page-analytics';

const xhr = global.XMLHttpRequest;

describe( 'Custom analytics for the TDP survey grade-level page', () => {
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

  it( 'should send analytics event when switch grades link is clicked', () => {
    const target = document.querySelector( '.a-link__jump' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'Switch grades' );
    expect( spy.mock.calls[0][1] ).toEqual( 'Switch grades from 3-5' );
  } );

  it( 'should send analytics event when privacy modal link is clicked', () => {
    const target = document.querySelector( '[data-open-modal="modal-privacy"]' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( 'See how your privacy is protected.' );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5' );
  } );

  it( 'should send analytics event when lets do this link is clicked', () => {
    const target = document.querySelector( 'a.survey-entry-link' );
    const spy = jest.fn();

    tdpAnalytics.bindAnalytics( spy );

    simulateEvent( 'click', target );

    expect( spy.mock.calls[0][0] ).toEqual( "Let's do this" );
    expect( spy.mock.calls[0][1] ).toEqual( '3-5' );
  } );

} );
