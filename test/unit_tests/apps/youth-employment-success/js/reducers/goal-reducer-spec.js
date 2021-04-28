import {
  goalReducer,
  GOAL_TIMELINES,
  initialState,
  updateGoalAction,
  updateGoalImportanceAction,
  updateGoalStepsAction,
  updateGoalTimelineAction
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/reducers/goal-reducer';

let UNDEFINED;

describe( 'goalReducer', () => {
  it( 'returns an initial state when it recevives an unsupported action type', () => {
    const state = goalReducer( UNDEFINED, { type: null } );

    expect( state ).toEqual( initialState );
  } );

  it( 'reduces the UPDATE_LONG_TERM_GOAL action ', () => {
    const text = 'some text';
    const state = goalReducer( UNDEFINED, updateGoalAction( text ) );

    expect( state.longTermGoal ).toBe( text );
  } );

  it( 'reduces the UPDATE_GOAL_IMPORTANCE action ', () => {
    const text = 'some text';
    const state = goalReducer( UNDEFINED, updateGoalImportanceAction( text ) );

    expect( state.goalImportance ).toBe( text );
  } );

  it( 'reduces the UPDATE_GOAL_STEPS action ', () => {
    const text = 'some text';
    const state = goalReducer( UNDEFINED, updateGoalStepsAction( text ) );

    expect( state.goalSteps ).toBe( text );
  } );

  it( 'reduces the UPDATE_GOAL_TIMELINE action ', () => {
    const value = '3 to 6 months';
    const state = goalReducer( UNDEFINED, updateGoalTimelineAction( value ) );

    expect( state.goalTimeline ).toBe( value );
  } );

  it( 'reduces the goalTimeline property to an empty string when invalid data is received', () => {
    GOAL_TIMELINES.forEach( value => {
      expect(
        goalReducer( UNDEFINED, updateGoalTimelineAction( value ) ).goalTimeline
      ).toBe( value );
    } );

    expect(
      goalReducer( UNDEFINED, updateGoalTimelineAction( 1 ) ).goalTimeline
    ).toBe( initialState.goalTimeline );
    expect(
      goalReducer( UNDEFINED, updateGoalTimelineAction( 'Text value' ) ).goalTimeline
    ).toBe( initialState.goalTimeline );
  } );
} );
