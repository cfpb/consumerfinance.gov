import reviewDetailsView from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/review/details';
import mockStore from '../../../../../mocks/store';
import { toArray } from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';
import { PLAN_TYPES } from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data/todo-items';

const HTML = `
<div class="js-yes-plans-review">
  <h2>Your plan to get to work</h2>
  <h3>Your to-do list</h3>
  <ul>
    <li>Ask about bus passes, gas cards, rideshare credits, or other reduced-fare transit cards</li>
  </ul>
  <div class="block block__sub">
    <p><b>OPTION 1: <span class="js-option-1-type"></span></b></p>
    <ul class="js-review-todo"></ul>
  </div>
  <div class="block block__sub">
    <p><b>OPTION 2: <span class="js-option-2-type"></span></b></p>
    <ul class="js-review-todo"></ul>
  </div>
  <div class="block block__sub">
    <p class="h3">Your first choice is <span class="js-transportation-type"></span></p>
    <div class="js-route-incomplete">
      <div class="m-notification"></div>
    </div>
    <div class="yes-route-details"></div>
    <div class="content_line"></div>
  </div>
  <div class="block block__sub">
    <p class="h3">Another option you compared: <span class="js-transportation-type"></span></p>
    <small>Depending on whether this fits in your budget and schedule, this could be a backup plan if you’re in a bind and your first choice doesn’t work out.</small>
    <div class="yes-route-details"></div>
    <div class="content_line"></div>
  </div>
</div>
`;

describe( 'reviewDetailsView', () => {
  const initMock = jest.fn();
  const renderMock = jest.fn();
  const routeDetailsView = () => ( {
    init: initMock,
    render: renderMock
  } );
  let store;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    const el = document.querySelector( `.${ reviewDetailsView.CLASSES.CONTAINER }` );
    store = mockStore();
    view = reviewDetailsView( el, { store, routeDetailsView } );
    view.init();
  } );

  afterEach( () => {
    store.mockReset();
    initMock.mockReset();
    view = null;
  } );

  it( 'subscribes to the store on init', () => {
    expect( store.subscribe.mock.calls.length ).toBe( 1 );
  } );

  it( 'initializes its two routeDetails subviews on init', () => {
    expect( initMock.mock.calls.length ).toBe( 2 );
  } );

  describe( 'on state update', () => {
    const state = {
      budget: { earned: 1, spent: 1 },
      routes: {
        routes: [
          { transportation: 'Walk', actionPlanItems: [ PLAN_TYPES.MILES ]},
          { transportation: 'Drive' }
        ]
      }
    };
    it( 'renders the details views', () => {
      store.subscriber()( {}, state );

      expect( renderMock.mock.calls.length ).toBe( 2 );
    } );

    it( 'renders the todo lists', () => {
      store.subscriber()( {}, state );

      const todoLists = toArray(
        document.querySelectorAll( `.${ reviewDetailsView.CLASSES.TODO }` )
      );

      expect( todoLists[0].children.length ).toBe( 1 );
      expect( todoLists[1].children.length ).toBe( 0 );
    } );

    it( 'toggles the todo notification el when there are todo list items', () => {
      const notification = document.querySelector( '.m-notification' );

      expect( notification.classList.contains( 'm-notification__visible' ) ).toBeFalsy();

      store.subscriber()( {}, state );

      expect( notification.classList.contains( 'm-notification__visible' ) ).toBeTruthy();
    } );
  } );
} );
