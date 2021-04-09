import reviewChoiceView from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/review/choice';
import mockStore from '../../../../../mocks/store';
import { simulateEvent } from '../../../../../../util/simulate-event';
import { toArray } from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';
import {
  updateRouteChoiceAction
} from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/choice-reducer';
import transportationMap from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data-types/transportation-map';

const CLASSES = reviewChoiceView.CLASSES;

const HTML = `
<div class="${ CLASSES.CONTAINER }">
  <div class="${ CLASSES.CHOICE }">
    <label>-</label>
    <input type="radio" name="choice" value="0">
  </div>
  <div class="${ CLASSES.CHOICE }">
    <label>-</label>
    <input type="radio" name="choice" value="1">
  </div>
  <div class="${ CLASSES.CHOICE }">
    <label>-</label>
    <input type="radio" name="choice" value="wait">
  </div>
  <button class="${ CLASSES.BUTTON }" disabled></button>
  <div class="${ CLASSES.REVIEW_PLAN }"></div>
</div>
`;

describe( 'reviewChoiceGoal', () => {
  let dom;
  let choiceInputs;
  let choiceWrappers;
  let store;
  let view;
  const onChooseMock = jest.fn();

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    dom = document.querySelector( `.${ CLASSES.CONTAINER }` );
    view = reviewChoiceView( dom, { store, onShowReviewPlan: onChooseMock } );
    view.init();
    choiceWrappers = toArray(
      dom.querySelectorAll( `.${ CLASSES.CHOICE }` )
    );
    choiceInputs = choiceWrappers.map( el => el.querySelector( 'input' ) );
  } );

  afterEach( () => {
    store.mockReset();
    onChooseMock.mockReset();
    view = null;
    choiceInputs.length = 0;
  } );

  describe( 'on init', () => {
    it( 'subscribes to the store', () => {
      expect( store.subscribe.mock.calls.length ).toBe( 1 );
    } );

    it( 'hides the final plan review section', () => {
      expect(
        dom.querySelector( `.${ CLASSES.REVIEW_PLAN }` )
          .classList.contains( 'u-hidden' )
      ).toBeTruthy();
    } );

    it( 'disables the form controls', () => {
      const button = dom.querySelector( `.${ CLASSES.BUTTON }` );

      choiceInputs.forEach(
        input => expect( input.getAttribute( 'disabled' ) ).toBe( 'disabled' )
      );
      expect( button.getAttribute( 'disabled' ) ).toBe( '' );
    } );
  } );

  it( 'dispatches the .updateRouteChoiceAction on radio input click', () => {
    const dispatch = store.dispatch.mock;
    simulateEvent( 'click', choiceInputs[0] );

    expect( dispatch.calls.length ).toBe( 1 );
    expect( dispatch.calls[0][0] ).toEqual(
      updateRouteChoiceAction( '0' )
    );
  } );

  it( 'enables the radio buttons when tansportation modes are selected', () => {
    const state = {
      routes: {
        routes: [
          { transportation: 'Walk' }, { transportation: 'Drive' }
        ]
      }
    };

    store.subscriber()( {}, state );

    choiceInputs.forEach( input => {
      expect( input.getAttribute( 'disabled' ) ).toBeFalsy();
    } );
  } );

  it( 'displays the transportation type in the button labels when modes are selected', () => {
    const state = {
      routes: {
        routes: [
          { transportation: 'Walk' }, { transportation: 'Drive' }
        ]
      }
    };

    store.subscriber()( {}, state );

    choiceWrappers.forEach( ( wrapper, i ) => {
      const route = state.routes.routes[i];

      if ( route ) {
        expect(
          wrapper.querySelector( 'label' )
            .textContent.indexOf(
              transportationMap[route.transportation]
            ) !== -1
        ).toBeTruthy();
      }
    } );
  } );

  it( 'enables the review choice button once a route choice is made', () => {
    const state = {
      routes: {
        routes: [
          { transportation: 'Walk' }, { transportation: 'Drive' }
        ]
      },
      routeChoice: '0'
    };

    store.subscriber()( {}, state );

    expect(
      dom.querySelector( `.${ CLASSES.BUTTON }` ).getAttribute( 'disabled' )
    ).toBeFalsy();
  } );

  it( 'shows the rest of the review section when the review choice button is clicked', () => {
    const state = {
      routes: {
        routes: [
          { transportation: 'Walk' }, { transportation: 'Drive' }
        ]
      },
      routeChoice: '0'
    };

    store.subscriber()( {}, state );

    simulateEvent( 'click', dom.querySelector( `.${ CLASSES.BUTTON }` ) );

    expect(
      dom.querySelector( `.${ CLASSES.REVIEW_PLAN }` )
        .classList.contains( 'u-hidden' )
    ).toBeFalsy();
  } );

  it( 'does not enable the radio buttons if no transportation options are specified', () => {
    const state = {
      routes: {
        routes: [
          { miles: '12' }, { miles: '5' }
        ]
      }
    };

    store.subscriber()( {}, state );

    choiceInputs.forEach(
      input => expect(
        input.getAttribute( 'disabled' )
      ).toBeTruthy()
    );
  } );

  it( 'calls its hook fn after showing the review plans', () => {
    simulateEvent( 'click', dom.querySelector( `.${ CLASSES.BUTTON }` ) );
    expect( onChooseMock ).toHaveBeenCalled();
  } );
} );
