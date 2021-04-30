import { simulateEvent } from '../../../../../../util/simulate-event.js';
import goalsView from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/goals';
import {
  updateGoalAction,
  updateGoalImportanceAction,
  updateGoalStepsAction,
  updateGoalTimelineAction
} from '../../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/goal-reducer.js';

const HTML = `
  <form class="js-yes-goals">
    <input type="radio" name="goalTimeline" class="a-radio" value="3 to 6 months">
    <input type="radio" name="goalTimeline" class="a-radio">
    <input type="radio" name="goalTimeline" class="a-radio">
    <input type="radio" name="goalTimeline" class="a-radio">
    <textarea name="longTermGoal" class="js-long-term-goal"></textarea>
    <textarea name="goalImportance" class="js-goal-importance"></textarea>
    <textarea name="goalSteps" class="js-goal-steps"></textarea>
  </form>
`;

describe( 'goalsView', () => {
  const CLASSES = goalsView.CLASSES;
  const dispatch = jest.fn();
  const mockStore = () => ( {
    dispatch,
    subscribe() { return {}; }
  } );
  let view;
  let store;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    store = mockStore();
    view = goalsView( document.querySelector( `.${ CLASSES.CONTAINER }` ), { store } );
    view.init();
  } );

  afterEach( () => {
    dispatch.mockReset();
    view = null;
  } );

  it( 'dispatches the correct event when the long term goal field is blurred', () => {
    const ltgEl = document.querySelector( `.${ CLASSES.LONG_TERM_GOAL }` );
    const goal = 'my goal';
    const mock = store.dispatch.mock;

    ltgEl.value = goal;

    simulateEvent( 'blur', ltgEl );

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateGoalAction( goal )
    );
  } );

  it( 'dispatches the correct event when the goal importance field is blurred', () => {
    const importanceEl = document.querySelector( `.${ CLASSES.GOAL_IMPORTANCE }` );
    const goal = 'my goal';
    const mock = store.dispatch.mock;

    importanceEl.value = goal;

    simulateEvent( 'blur', importanceEl );

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateGoalImportanceAction( goal )
    );
  } );

  it( 'dispatches the correct event when the goal steps field is blurred', () => {
    const stepsEl = document.querySelector( `.${ CLASSES.GOAL_STEPS }` );
    const goal = 'my goal';
    const mock = store.dispatch.mock;

    stepsEl.value = goal;

    simulateEvent( 'blur', stepsEl );

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateGoalStepsAction( goal )
    );
  } );

  it( 'dispatches the correct event when a radio timeline button is selected', () => {
    const shortTimelineEl = document.querySelectorAll( '.a-radio' )[0];
    const mock = store.dispatch.mock;

    simulateEvent( 'click', shortTimelineEl );

    expect( mock.calls.length ).toBe( 1 );
    expect( mock.calls[0][0] ).toEqual(
      updateGoalTimelineAction( shortTimelineEl.value )
    );
  } );

  it( 'preserves spaces in the textarea', () => {
    const ltgEl = document.querySelector( `.${ CLASSES.LONG_TERM_GOAL }` );
    const goal = 'This is my goal\nIt is a good goal\nThe end!';
    const mock = store.dispatch.mock;

    ltgEl.value = goal;

    simulateEvent( 'blur', ltgEl );

    const expected = goal.replace( /\n/g, '<br />' );

    expect( mock.calls[0][0].data ).toEqual( expected );
  } );
} );
