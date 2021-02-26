import
reviewGoalsView
  // eslint-disable-next-line max-len
  from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/review/goals';
import mockStore from '../../../../../mocks/store';
import {
  toArray
  // eslint-disable-next-line max-len
} from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';

const HTML = `
<div class="js-your-goals">
  <h3>Your long-term goal for getting to work</h3>

  <h4><b>Your long-term goal:</b></h4>
  <p class="js-review-goal" data-js-goal="longTermGoal"></p>

  <h4><b>Why this goal important to you:</b></h4>
  <p class="js-review-goal" data-js-goal="goalImportance"></p>

  <h4><b>You hope to reach your goal by:</b></h4>
  <p class="js-review-goal" data-js-goal="goalTimeline"></p>

  <h4><b>Steps you could take to reach your goal:</b></h4>
  <p class="js-review-goal" data-js-goal="goalSteps"></p>

  <div class="content_line"></div>
</div>
`;

describe( 'reviewGoalsView', () => {
  let store;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    store.mockState( {
      goals: {}
    } );
    view = reviewGoalsView(
      document.querySelector(
        `.${ reviewGoalsView.CLASSES.CONTAINER }`
      ),
      { store }
    );
    view.init();
  } );

  afterEach( () => {
    store.mockReset();
    view = null;
  } );

  it( 'subscribes to the store on init', () => {
    expect( store.subscribe.mock.calls.length ).toBe( 1 );
  } );

  it( 'updates the goals nodes with values from the store', () => {
    const prevState = {
      goals: {
        longTermGoal: '',
        goalImportance: '',
        goalSteps: '',
        goalTimeline: ''
      }
    };

    const state = {
      goals: {
        longTermGoal: 'goal',
        goalImportance: 'very',
        goalSteps: 'several',
        goalTimeline: '3 to 6 months'
      }
    };

    let els = toArray(
      document.querySelectorAll( `.${ reviewGoalsView.CLASSES.GOAL }` )
    );

    els.forEach( el => expect( el.textContent ).toBe( '' ) );

    store.subscriber()( prevState, state );

    els = toArray(
      document.querySelectorAll( `.${ reviewGoalsView.CLASSES.GOAL }` )
    );

    els.forEach( el => {
      const expected = state.goals[el.getAttribute( 'data-js-goal' )];
      expect( el.textContent ).toBe( expected );
    } );
  } );

  it( 'updates when prevState has not been populated', () => {
    const prevState = { goals: null };
    const state = {
      goals: {
        longTermGoal: 'goal',
        goalImportance: 'very',
        goalSteps: 'several',
        goalTimeline: '3 to 6 months'
      }
    };

    let els = toArray(
      document.querySelectorAll( `.${ reviewGoalsView.CLASSES.GOAL }` )
    );

    els.forEach( el => expect( el.textContent ).toBe( '' ) );

    store.subscriber()( prevState, state );

    els = toArray(
      document.querySelectorAll( `.${ reviewGoalsView.CLASSES.GOAL }` )
    );

    els.forEach( el => {
      const expected = state.goals[el.getAttribute( 'data-js-goal' )];
      expect( el.textContent ).toBe( expected );
    } );
  } );
} );
